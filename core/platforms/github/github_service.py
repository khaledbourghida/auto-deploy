from data.repositories.account_repo import AccountRepository
from data.repositories.token_repo import TokenRepository
from data.repositories.platform_repo import PlatformRepository
from core.platforms.github.github_platform import GithubPlatform
from core.general_service import GeneralService
from data.models import Token , Account
from core.security import Security
from core.http.errors import (
    ApiError, 
    AuthenticationError, 
    AuthorizationError, 
    ValidationError, 
    TokenExpiredError
)
from datetime import datetime, timezone
import re

class GitHubService:
    def __init__(self , account : Account , navigator , page):
        self.navigator = navigator
        self.page = page
        self.platform = GithubPlatform()
        self.account_repo = AccountRepository()
        self.token_repo = TokenRepository()
        self.platform_repo = PlatformRepository()
        self.general_service = GeneralService()
        self.security = Security()
        self.account = account
        self.token = self.general_service.get_token(self.account.id)
        
    def create_repo(self, name: str, description: str = "", private: bool = False):    
        if not name:
            raise ValidationError("Repository name is required.")

        if not re.match(r"^[a-zA-Z0-9._-]+$", name):
            raise ValidationError("Invalid name. Use only letters, numbers, hyphens, and underscores.")

        if not self.token:
             raise AuthenticationError("No access token found. Please sign in again.")

        if self.token.expires_at:
            date_format = "%Y-%m-%dT%H:%M:%S"
            try:
                expires_at = datetime.strptime(self.token.expires_at, date_format)
                if datetime.now() > expires_at:
                    raise TokenExpiredError("Access token has expired.")
            except ValueError:
                pass # Ignore date parsing errors, let API decide

        # --- 3. REQUEST PREPARATION ---
        # Prepare pure data for the platform client
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True 
        }

        # --- 4. HTTP EXECUTION (via Platform) ---
        try:
            # Platform client just sends the raw request
            response = self.platform.create_repo(payload, self.token.token_encrypted)
        except Exception as e:
            # Handle network-level failures
            raise ApiError(f"Network connection failed: {str(e)}", 500)

        # --- 5. RESPONSE HANDLING ---
        # Success (201 Created)
        if response.status_code == 201:
            return response.json()
        
        # Map specific HTTP codes to Domain Errors
        if response.status_code == 401:
            raise AuthenticationError("Session invalid or expired.")
        
        if response.status_code == 403:
            raise AuthorizationError("Access denied. You may be rate-limited.")

        if response.status_code == 422:
            raise ValidationError("Repository name already exists or is unavailable.")

        if response.status_code >= 500:
            raise ApiError("GitHub server error. Please try again later.", 500)

        # Catch-all for other non-success codes
        raise ApiError(f"Unexpected error ({response.status_code})", response.status_code)

    def create_account(self, raw_token: str):
        response = self.platform.get_account_info(raw_token)

        if response.status_code == 401:
            raise AuthenticationError()
        
        if response.status_code == 403 :
            raise AuthorizationError()

        if not f"{response.status_code}".startswith('2') :
            raise ApiError(
                message="GitHub API error",
                status_code=response.status_code
            )

        data = response.json()
        
        platform_id = self.platform_repo.get_id_by_name("github")

        self.account_repo.deactivate_all(platform_id=platform_id)

        account = Account(
            id=None,
            platform_id=platform_id,
            username=data["login"],
            email=data.get("email"),
            avatar_url=data["avatar_url"],
            is_active=1,
            created_at=datetime.now(timezone.utc).isoformat()
        )

        account_id = self.account_repo.create(account)

        encrypted_token = self.security.encrypt_token(raw_token)

        token = Token(
            id=None,
            account_id=account_id,
            token_encrypted=encrypted_token,
            token_type="personal_access_token",
            expires_at=None,
            scopes=None,
            created_at=datetime.now(timezone.utc).isoformat()
        )

        self.token_repo.save(token)

        return {
            "username": account.username,
            "avatar": account.avatar_url,
            "email": account.email,
            "platform": "GitHub"
        }
        
    def get_active(self) :
        platform_id = self.platform_repo.get_id_by_name("github")
        data = self.account_repo.get_active(platform_id)
        
        return data
    
    def get_rate_limit(self):
        """
        Fetches rate limits for the connected account.
        Returns: Dict containing 'limit', 'used', 'remaining', 'reset'
        Raises: ApiError if something goes wrong.
        """
        # 1. Validation: Ensure we actually have a token before making a request
        if not self.token:
            # Try to fetch it again in case it was just added
            self.token = self.general_service.get_token(self.account.id)
            if not self.token:
                raise AuthorizationError("No access token found for this account. Please reconnect.")

        # 2. Execution: Call the platform layer
        try:
            response = self.platform.get_rate_limit(self.token.token_encrypted)
        except Exception as e:
            # Handle network level failures (DNS, timeout, etc.)
            raise ApiError(f"Network error: {str(e)}", 500)

        # 3. Error Handling: Check Status Codes
        if response.status_code == 401:
            raise AuthenticationError("Token expired or revoked by GitHub.")
        
        if response.status_code == 403:
            raise AuthorizationError("Access denied (403). Rate limit likely exceeded.")

        if response.status_code != 200:
             raise ApiError(f"GitHub API Error: {response.status_code}", response.status_code)

        # 4. Data Parsing: Safely parse the JSON
        try:
            data = response.json()
            core = data.get("resources", {}).get("core", {})
            return {
                "limit": core.get("limit", 0),
                "remaining": core.get("remaining", 0),
                "used": core.get("used", 0), # GitHub sometimes sends 'used', otherwise calc it
                "reset": core.get("reset", 0),
                "status": "ok"
            }
        except Exception as e:
            raise ApiError(f"Failed to parse GitHub response: {str(e)}", 500)
        
        