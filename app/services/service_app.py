
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from app.services.htmx_demo.router import router as routerDemo
from app.services.htmx_template.router import router as routerTemplate

# -------------------
# Starting an App Api 
app = FastAPI()

# -------------------
# The Api Service App start with a Static File Rooteur ,
# Web GET can get access to all file in /app/core/service/static/
# TODO : static directory must be move in env

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR / "htmlStatic")
app.mount("/static", StaticFiles(directory=BASE_DIR / "htmlStatic"), name="static")


routerStatic = APIRouter()

@routerStatic.get("/", response_class=HTMLResponse)
async def index():
    file_path = BASE_DIR / "htmlStatic" / "index.html"
    return FileResponse(file_path, media_type="text/html")

app.include_router(routerStatic)

# -------------------
# Service Must be include in this file. All router function will be added application  
app.include_router(routerDemo)
app.include_router(routerTemplate)


# -------------------
# Other Service router must be include hear 
# TODO : Add your service router . 





