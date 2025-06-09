
from app.core.service.article import htmlArticleMain
from app.core.service.article import htmlArticleH2
from app.core.service.article import htmlArticleH3
from app.core.service.content.makedown import htmlContentMD

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------




def htmlH1_Exemple1():
    
    md = """

# Step 1: Create a Router in the Service Project

```python
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from core.service.htmx_core import htmlMenuH1_List, htmlArticleMain

router = APIRouter()

@router.get("/htmx_example/menu/template", response_class=HTMLResponse)
async def get_menu_template():
    return htmlMenuH1_List("MenuTest", [
        {"name": "Get an article and load it in the content", "url": "/htmx_example/article/template"}
    ], isOpen=True)

@router.get("/htmx_example/article/template", response_class=HTMLResponse)
async def get_article_template():
    return htmlArticleMain("MenuTest", "<p>Hello World</p>", isOpen=True)
````

> You can use any building component from `core.service.htmx_core` to build menus and articles. Feel free to be creative with custom HTML and CSS as well.

---

# Step 2: Register the Router in the Main Service App

In your main FastAPI application file (`core.service.service_app.py`), register the router:

```python
from app.services.NAME.router import router as routerNAME

app.include_router(routerNAME)
```

> Your app is now ready to handle REST GET requests. For more examples, check out `core.service.htmx_example.template.router.py`.

---

# Step 3: Use the Route in the Frontend Application

The app uses **HTMX** to handle API requests and update the DOM dynamically, making it easy to extend the interface.

## Example: Add a Menu in the App

In your `index.html`, inside the `#nav-left` `<div>`, add an element that uses HTMX to request the menu:

```html
<article 
    hx-get="/htmx_example/menu/template" 
    hx-trigger="click" 
    hx-swap="outerHTML">
    <label><h2>My Template</h2></label>
</article>
```

> Clicking this article will load the menu template into the DOM using HTMX.

## What are the HTMX Attributes

- hx-get: Specifies the URL to fetch content from via an HTTP GET request when triggered.
- hx-trigger: Defines the event that triggers the request (here, a click on the <article> element).
- hx-swap: Controls how the returned HTML replaces existing content. outerHTML means the entire <article> element is replaced by the response.

Together, these attributes enable dynamic content loading and DOM updates without writing JavaScript, making the app more interactive and responsive.

"""

    return f"""
        {htmlArticleMain('Exemple 1 : Starting with your App', htmlContentMD(md), isOpen=True)}
    """

