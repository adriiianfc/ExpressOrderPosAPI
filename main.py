import logging
from typing import Optional

from fastapi import FastAPI, Depends, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware

from api.routes.users_api import api as users_api
from api.routes.auth_api import api as auth_api
from api.routes.orders_api import api as orders_api
from api.routes.clients_api import api as clients_api
from api.routes.articles_api import api as articles_api
from api.routes.tags_api import tags
from utils.gen_token import  get_authorization_header

logging.basicConfig(level=logging.INFO, format='[%(asctime)-15s][%(funcName)s:%(lineno)d] %(message)s')

# Dependencia para validar token desde encabezados

app = FastAPI(
    title="PDV API",
    openapi_tags=tags
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permitir todos los dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


app.include_router(auth_api, tags=["Auth"], prefix="/auth")
app.include_router(users_api, tags=["Users"], prefix="/users", dependencies=[Depends(get_authorization_header)])
app.include_router(orders_api, tags=["Orders"], prefix="/orders", dependencies=[Depends(get_authorization_header)])
app.include_router(clients_api, tags=["Clients"], prefix="/clients", dependencies=[Depends(get_authorization_header)])
app.include_router(articles_api, tags=["Articles"], prefix="/articles", dependencies=[Depends(get_authorization_header)])



# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)