from core.http.client import HttpClient
from typing import Dict

class GithubPlatform :
    def __init__(self):
        self.http_client = HttpClient()
        self.base_url = "https://api.github.com"

    def get_account_info(self, token : str) :
        url = f"{self.base_url}/user"
        headers = {
            'Authorization' : f'Bearer {token}',
            'Accept' : 'application/vnd.github+json',
            'Content-Type' : 'application/json'
        }
        
        response = self.http_client.get(
            url = url,
            headers = headers,
        )
        
        return response
    
    def create_repo(self, data : Dict, token : str):
        url = f"{self.base_url}/user/repos"
        headers = {
            'Authorization' : f'Bearer {token}',
            'Accept' : 'application/vnd.github+json',
            'Content-Type' : 'application/json'
        }
        
        response = self.http_client.post(
            url,
            headers ,
            data
        )
        
        return response
    
    def get_rate_limit(self, token: str):
        url = f"{self.base_url}/rate_limit"
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
                
        return self.http_client.get(url, headers=headers)
        
    def list_repositories(self, token) :
        pass
    
    def get_repository_details(self, full_name) :
        pass
    
    def get_repository_languages(self, token, full_name) :
        pass
    
    def get_recent_activity(self, token) :
        pass