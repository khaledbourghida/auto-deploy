import flet as ft
PLATFORMS = [
    {
        "title" : "Github",
        "subtitle" : "Version Control",
        "bgColor" : "#1f2a38",
        "icons" : ft.Icons.CODE,
        "desc" : "Automate repository management, issues, pull requests, and deployment.",
        "is_connected" : True,
    },
    {
        "title" : "Netlify",
        "subtitle" : "Web Hosting",
        "bgColor" : "#0d9489",
        "icons" : ft.Icons.NETWORK_CELL,
        "desc" : "Deploy and manage your web applications with automated builds and deployments.",
        "is_connected" : False,
    },
    {
        "title" : "Render",
        "subtitle" : "Cloud Platform",
        "bgColor" : "#9234eb",
        "icons" : ft.Icons.LAYERS,
        "desc" : "Manage cloud services, databases, and auto-scaling infrastructure.",
        "is_connected" : False,
    },
    {
        "title" : "Firebase",
        "subtitle" : "Backend Services",
        "bgColor" : "#ea580c",
        "icons" : ft.Icons.FIRE_EXTINGUISHER,
        "desc" : "Automate database operations, authentication, and cloud functions.",
        "is_connected" : True,
    },
    {
        "title" : "Docker Hub",
        "subtitle" : "Container Registry",
        "bgColor" : "#2664eb",
        "icons" : ft.Icons.DOCK_ROUNDED,
        "desc" : "Manage container images, automated builds, and deployment piplines.",
        "is_connected" : False,
    },
    
    {
        "title" : "MongoDB",
        "subtitle" : "Database",
        "bgColor" : "#15a349",
        "icons" : ft.Icons.LEAVE_BAGS_AT_HOME,
        "desc" : "Automate database operations, backups, and cluster management.",
        "is_connected" : True,
    },
]