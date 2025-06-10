import uuid
import json


from fastapi_htmx.core.service.menu.menu_label import htmlMenuLabelItem_ClickOnLabel
from fastapi_htmx.core.service.menu.menu_label import htmlMenuLabelItem_ClickOnIcon

# -----------------------------------------------------------------------------


def htmlMenu(H: str, titel: str, innerSection: str, isOpen: bool = False):
    uid = uuid.uuid4()
    return f"""
        <article class="toggle">
            <input type="checkbox" id="toggleDetail{uid}" class="toggleDetail" {"checked" if isOpen else ""}>
            <label for="toggleDetail{uid}" class="hover">
                <H{H}>{titel}</H{H}>
            </label>
            <section class="toggleContent">
                {innerSection}
            </section>
        </article>
    """


def htmlMenuH1(titel: str, innerSection: str, isOpen: bool = False):
    return htmlMenu("1", titel, innerSection, isOpen)


def htmlMenuH2(titel: str, innerSection: str, isOpen: bool = False):
    return htmlMenu("2", titel, innerSection, isOpen)


def htmlMenuH3(titel: str, innerSection: str, isOpen: bool = False):
    return htmlMenu("3", titel, innerSection, isOpen)


# -----------------------------------------------------------------------------


def htmlMenuH1_List(title: str, listItem: list, isOpen: bool = False):
    """
    listItem = [
        {'name': 'Simple Clicable Item', 'url': '/htmx/exemple/1'},
        {'name': 'Icone Clicable Item 1', 'url': '/htmx/exemple/1'},
        {'name': 'Icone Clicable Item 2', 'url': '/htmx/exemple/1'},
    ]
    """
    arrayOfHtlmLabel = [htmlMenuLabelItem_ClickOnIcon(**it) for it in listItem]
    htmlLabels = "".join(arrayOfHtlmLabel)
    html = htmlMenuH1(title, htmlLabels, isOpen)
    return html


def htmlMenuH1_Group(title, groups, isOpen: bool = False):
    htmlSectionGroup = ""
    for keyGroup in groups.keys():
        arrayOfHtlmLabel = [
            htmlMenuLabelItem_ClickOnIcon(**item) for item in groups[keyGroup]
        ]
        htmlLabelList = "".join(arrayOfHtlmLabel)
        htmlSectionGroup += htmlMenuH2(keyGroup, htmlLabelList, isOpen=False)
    return htmlMenuH1(title, htmlSectionGroup, isOpen)


def htmlMenuH1_Tree(title, tree, isOpen: bool = False):

    htmlSectionTree = ""
    for keyTree in tree.keys():
        groups = tree[keyTree]
        htmlSectionGroup = ""
        for keyGroup in groups.keys():
            arrayOfHtlmLabel = [
                htmlMenuLabelItem_ClickOnIcon(**item) for item in groups[keyGroup]
            ]
            htmlLabelList = "".join(arrayOfHtlmLabel)
            htmlSectionGroup += htmlMenuH3(keyGroup, htmlLabelList, isOpen=False)
        htmlSectionTree += htmlMenuH2(keyTree, htmlSectionGroup, isOpen=False)

    return htmlMenuH1(title, htmlSectionTree, isOpen)
