from fastapi_htmx.core.service.menu.menu_article import htmlMenuH1_List
from fastapi_htmx.core.service.menu.menu_article import htmlMenuH1_Group
from fastapi_htmx.core.service.menu.menu_article import htmlMenuH1_Tree

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlHtmxExmple_menu_group():

    return """

        <article
            hx-get="/htmx_exemple/menu/group"
            hx-trigger="load"
            hx-swap="outerHTML">
            <label><h4> Load Me: Group Component </h4</label>
        </article>

        <article
            class="hover-active"
            hx-get="/htmx_exemple/menu/tree"
            hx-trigger="click"
            hx-swap="outerHTML">
            <label><h4> Load Me </h4</label>
        </article>

    """


def htmlHtmxExmple_menu():
    groupItem = {
        "Into": [
            {
                "name": "Exemple 1 : Starting with your App",
                "url": "/htmx_exemple/content_h1",
            },
            {
                "name": "Exemple 2 : Article content components",
                "url": "/htmx_exemple/content_h2",
            },
            {"name": "Exemple 3 - Sub Section", "url": "/htmx_exemple/content_h3"},
        ],
        "Component": [
            {"name": "Component MD", "url": "/htmx_exemple/component_md"},
            {"name": "Component Chart", "url": "/htmx_exemple/component_chart"},
            {
                "name": "Component Panda Chart",
                "url": "/htmx_exemple/component_panda_chart",
            },
        ],
    }
    return htmlMenuH1_Group("GroupMenu", groupItem, True)


def htmlHtmxExmple_menu_tree():
    groupItem = {
        "Group A": [
            {"name": "ItemA", "url": "/htmx_exemple/content_h1"},
            {"name": "ItemA", "url": "/htmx_exemple/content_h1"},
        ],
        "Group B": [
            {"name": "ItemA", "url": "/htmx_exemple/content_h1"},
            {"name": "ItemA", "url": "/htmx_exemple/content_h1"},
        ],
    }
    treeItem = {
        "Tree1": groupItem,
        "Tree2": groupItem,
    }
    return htmlMenuH1_Tree("TreeMenu", treeItem, True)
