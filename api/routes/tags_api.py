from fastapi import APIRouter

# Definición de tags para las tablas del sistema
tags = [
    {"name": "Users", "description": "Manage users, authentication, and permissions."},
    {"name": "Clients", "description": "Manage clients"},
    {"name": "Articles", "description": "Manage articles."},
    {"name": "Orders", "description": "Manage Orders."},

]
# Inicialización del enrutador
api = APIRouter()
