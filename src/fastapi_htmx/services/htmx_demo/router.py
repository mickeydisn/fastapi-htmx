from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from fastapi_htmx.services.htmx_demo.menu.menu import htmlHtmxExmple_menu
from fastapi_htmx.services.htmx_demo.menu.menu import htmlHtmxExmple_menu_group
from fastapi_htmx.services.htmx_demo.menu.menu import htmlHtmxExmple_menu_tree

from fastapi_htmx.services.htmx_demo.article.exemple1 import htmlH1_Exemple1
from fastapi_htmx.services.htmx_demo.article.exemple2 import htmlH1_Exemple2
from fastapi_htmx.services.htmx_demo.article.exemple3 import htmlH1_Exemple3

from fastapi_htmx.services.htmx_demo.article.exemple_component import (
    htmlHtmxExmple_component_md,
)
from fastapi_htmx.services.htmx_demo.article.exemple_component import (
    htmlHtmxExmple_component_chat,
)
from fastapi_htmx.services.htmx_demo.article.exemple_component import (
    htmlHtmxExmple_component_panda_chat,
)

# --------------------
# Menu

router = APIRouter()


@router.get("/htmx_exemple/menu", response_class=HTMLResponse)
async def get_menu():
    return htmlHtmxExmple_menu()


@router.get("/htmx_exemple/menu/group", response_class=HTMLResponse)
async def get_menu_group():
    return htmlHtmxExmple_menu_group()


# --------------------
# Article Exemple


@router.get("/htmx_exemple/content_h1", response_class=HTMLResponse)
async def get_content_h1():
    return htmlH1_Exemple1()


@router.get("/htmx_exemple/content_h2", response_class=HTMLResponse)
async def get_content_h2():
    return htmlH1_Exemple2()


@router.get("/htmx_exemple/content_h3", response_class=HTMLResponse)
async def get_content_h3():
    return htmlH1_Exemple3()


@router.get("/htmx_exemple/component_md", response_class=HTMLResponse)
async def get_component_md():
    return htmlHtmxExmple_component_md()


@router.get("/htmx_exemple/component_chart", response_class=HTMLResponse)
async def get_component_chart():
    return htmlHtmxExmple_component_chat()


@router.get("/htmx_exemple/component_panda_chart", response_class=HTMLResponse)
async def get_component_panda_chart():
    return htmlHtmxExmple_component_panda_chat()


# Fake in-memory DB
items = [
    {"id": 1, "name": "Item One"},
    {"id": 2, "name": "Item Two"},
]


@router.post("/api/items")
async def create_item(item: dict):
    item["id"] = len(items) + 1
    items.append(item)
    return {"message": "Item added", "item": item}
