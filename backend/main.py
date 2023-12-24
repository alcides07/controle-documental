from fastapi.responses import RedirectResponse
from database import engine, Base
from fastapi import FastAPI
from routers import user, auth

Base.metadata.create_all(bind=engine)


app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "nord"})
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url="/docs")
    return response
