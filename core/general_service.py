from data.repositories.account_repo import AccountRepository
from data.repositories.token_repo import TokenRepository
from data.repositories.platform_repo import PlatformRepository
from core.platforms.github.github_platform import GithubPlatform
from data.models import Token , Account
from core.security import Security
from core.http.errors import AuthorizationError, ApiError, AuthenticationError
from datetime import datetime

class GeneralService :
    def __init__(self):
        self.platform_repo = PlatformRepository()
        self.account_repo = AccountRepository()
        self.token_repo = TokenRepository()
        self.security = Security()
        self.platforms = self.platform_repo.get_all()
        
    def get_all_data(self) :
        data = []
        num_accounts = 0
        for platfrom in self.platforms :
            accounts = self.account_repo.get_by_platform(platfrom.id)
            data.append({
                "platform" : platfrom,
                "accounts" : accounts,
            })
            num_accounts = num_accounts + len(accounts)
                    
        return (data , num_accounts)
    
    def get_all_active_accounts(self) :
        data = []
        for platform in self.platforms :
            account = self.get_active_account(platform.id)
            if account :
                token = self.get_token(account.id)
                data.append((platform , account , token))
        
        return data

    def activate_account(self, account_id , platform_id) :
        print("activate account")
        self.account_repo.deactivate_all(platform_id)
        self.account_repo.set_active(account_id)
    
    def deactivate_account(self, platform_id) :
        print("deactivate account")
        self.account_repo.deactivate_all(platform_id)
        
    def delete_account(self , account : Account) :
        print("delete account")
        self.account_repo.delete(account.id)
        token = self.get_token(account.id)
        if token :
            self.delete_token(account.id)
        if account.is_active :
            self.platform_repo.make_unconnected(account.platform_id)
        
    def create_account(self, account, platform_id , activate_platform) :
        if activate_platform :
            self.account_repo.deactivate_all(platform_id)
            self.platform_repo.make_connected(platform_id)
        self.account_repo.create(account)
    
    def connect_platform(self, id):
        self.platform_repo.make_connected(id)        
        
    def get_accounts(self, platform_id) :
        return self.account_repo.get_by_platform(platform_id)
    
    def get_active_account(self, platform_id) :
        return self.account_repo.get_active(platform_id)
    
    def get_platform(self, id) :
        return self.platform_repo.get_by_id(id)
    
    def get_token(self, account_id) :
        token = self.token_repo.get_by_account(account_id)
        if token :
            token.token_encrypted = self.security.decrypt_token(token.token_encrypted)
            return token
        else :
            return None
    
    def create_token(self, token : Token) :
        encrypted_token = self.security.encrypt_token(token.token_encrypted)
        token.token_encrypted = encrypted_token
        self.token_repo.save(token)
        
    def delete_token(self, id) :
        self.token_repo.delete(id)
        
    def get_all_tokens_info(self):
        data = []
        for platform in self.platforms:
            accounts = self.account_repo.get_by_platform(platform.id)
            for account in accounts:
                token = self.get_token(account.id) # get_token automatically decrypts
                if token:
                    data.append((platform, account, token))
        return data

    def update_token(self, token: Token):
        encrypted_token = self.security.encrypt_token(token.token_encrypted)
        token.token_encrypted = encrypted_token
        self.token_repo.update(token)