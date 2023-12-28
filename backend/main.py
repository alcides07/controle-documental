from fastapi.responses import RedirectResponse
from database import engine, Base
from fastapi import FastAPI
from routers import user, auth, arquivo
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "nord"})
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(arquivo.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url="/docs")
    return response
