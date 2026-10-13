from data.repositories.account_repo import AccountRepository
from data.repositories.token_repo import TokenRepository
from data.repositories.platform_repo import PlatformRepository
from core.platforms.github.github_platform import GithubPlatform
from data.models import Token , Account
from core.security import Security
from core.http.errors import AuthorizationError, ApiError, AuthenticationError
from datetime import datetime

class PlatformsService :
    def __init__(self):
        self.platform_repo = PlatformRepository()
        
    def get_all_platforms(self) :
        platforms = self.platform_repo.get_all()