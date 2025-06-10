from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from fastapi_htmx.core.service.menu.menu_article import htmlMenuH1_List
from fastapi_htmx.core.service.article import htmlArticleMain


router = APIRouter()


@router.get("/htmx_exemple/menu/template", response_class=HTMLResponse)
async def get_menu_template():
    return htmlMenuH1_List(
        "Starting Template",
        [
            {
                "name": "Get an article an load in the content",
                "url": "/htmx_exemple/article/template",
            }
        ],
        isOpen=True,
    )


@router.get("/htmx_exemple/article/template", response_class=HTMLResponse)
async def get_article_template():
    return htmlArticleMain("Starting Template", "<p>Hello Work</p>", isOpen=True)


# ------------------
