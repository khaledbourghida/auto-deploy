# data/seed/platforms_seed.py
from data.repositories.platform_repo import PlatformRepository
from data.repositories.account_repo import AccountRepository
from data.models import Platform , Account

def seed_platforms():
    repo = PlatformRepository()
    account = AccountRepository()
    
    github = Platform.github()
    netlify = Platform.netlify()
    render = Platform.render()
    dockerhub = Platform.docker_hub()
    
    testacc = Account.testAccount()
    
    platforms = [github , netlify , render , dockerhub]
    

    for platform in platforms :
        if not repo.exists(platform.name):
            repo.create(platform)
            print(f"✅ {platform.display_name} platform seeded")
        else:
            print(f"ℹ️ {platform.display_name} platform already exists")
    
    # id = account.create(testacc)
        
