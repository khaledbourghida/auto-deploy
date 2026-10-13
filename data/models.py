from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Platform :
    id : int
    name : str
    display_name : str
    subtitle : str
    bgcolor : str
    icon : str
    desc : str
    base_url : str
    is_connected : int
    created_at : str
    
    @classmethod
    def from_row(cls , row) :
        return cls(
            id = row["id"],
            name = row["name"],
            display_name = row["display_name"],
            subtitle = row["subtitle"],
            bgcolor = row["bgcolor"],
            icon = row["icon"],
            desc = row["desc"],
            base_url = row["base_url"],
            is_connected = row["is_connected"],
            created_at = row["created_at"]
        )
    
    @classmethod
    def github(cls):
        return cls(
            id=None,
            name="github",
            display_name="GitHub",
            subtitle="Version Control",
            bgcolor="#1f2a38",
            icon="assets/icons/github",
            desc="Automate repository management, issues, pull requests, and deployment.",
            base_url="https://api.github.com",
            is_connected=0,
            created_at=datetime.now(timezone.utc).isoformat()
        )
    
    @classmethod
    def netlify(cls) :
        return cls(
            id=None,
            name="netlify",
            display_name="Netlify",
            subtitle="Web Hosting",
            bgcolor="#0d9489",
            icon="assets/icons/netlify",
            desc="Deploy and manage your web applications with automated builds and deployments.",
            base_url="https://api.netlify.com/api/v1",
            is_connected=0,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
    
    @classmethod
    def render(cls) :
        return cls(
            id=None,
            name="render",
            display_name="Render",
            subtitle="Cloud Platform",
            bgcolor="#9234eb",
            icon="assets/icons/render",
            desc="Manage cloud services, databases, and auto-scaling infrastructure.",
            base_url="https://api.render.com/v1",
            is_connected=0,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        
    @classmethod
    def docker_hub(cls):
        return cls(
            id=None,
            name="docker hub",
            display_name="Docker Hub",
            subtitle="Container Registry",
            bgcolor="#2664eb",
            icon="assets/icons/dockerhub",
            desc="Manage container images, automated builds, and deployment piplines.",
            base_url="https://hub.docker.com",
            is_connected=0,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        
    def to_insert_tuple(self) :
        return (
            self.name , 
            self.display_name ,
            self.subtitle,
            self.bgcolor, 
            self.icon , 
            self.desc,
            self.base_url ,
            self.is_connected, 
            self.created_at,
        )
            
@dataclass
class Account:
    id: int | None
    platform_id: int
    username: str
    email: str | None
    avatar_url: str | None
    is_active: int
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            platform_id=row["platform_id"],
            username=row["username"],
            email=row["email"],
            avatar_url=row["avatar_url"],
            is_active=row["is_active"],
            created_at=row["created_at"],
        )
    
    @classmethod
    def testAccount(cls) :
        return cls(
            id=None,
            platform_id=3,
            username="khaled",
            email="khaledbourghida@gmail.com",
            avatar_url="nn",
            is_active=1,
            created_at=datetime.now(timezone.utc).isoformat()
        )

    def to_insert_tuple(self):
        return (
            self.platform_id,
            self.username,
            self.email,
            self.avatar_url,
            self.is_active,
            self.created_at,
        )

@dataclass
class Token :
    id : int
    account_id : int
    token_encrypted : str
    token_type : str
    expires_at : str
    scopes : str
    created_at : str
    
    @classmethod
    def from_row(cls , row) :
        return cls(
            id = row["id"],
            account_id = row["account_id"],
            token_encrypted = row["token_encrypted"],
            token_type = row["token_type"],
            expires_at = row["expires_at"],
            scopes = row["scopes"],
            created_at = row["created_at"]
        )
        
    def to_insert_tuple(self) :
        return (self.account_id , self.token_encrypted , self.token_type , self.expires_at , self.scopes , self.created_at)
            
@dataclass
class Repository :
    id : int
    account_id : int
    repo_id : str
    name : str
    full_name : str
    is_private : int
    main_language : str
    updated_at : str
    
    @classmethod
    def from_row(cls , row) :
        return cls(
            id = row["id"],
            account_id = row["account_id"],
            repo_id = row["repo_id"],
            name = row["name"],
            full_name = row["full_name"],
            is_private = row["is_private"],
            main_language = row["main_language"],
            updated_at = row["updated_at"]
        )
    
    def to_insert_tuple(self) :
        return (self.account_id , self.repo_id , self.name , self.full_name , self.is_private , self.main_language , self.updated_at)
    
@dataclass
class Activity:
    id : int #INTEGER PK
    account_id : int #INTEGER FK
    entity_type : str #TEXT
    entity_id : str #TEXT
    action : str #TEXT
    created_at : str #TEXT
    
@dataclass
class Setting :
    key : str #TEXT PK
    value : str #TEXT