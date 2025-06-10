import uuid
import json

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlArticle(
    H: str,  # 1, 2, 3, 4
    titel: str,
    innerSection: str | list,
    isOpen: bool = False,
    isClosable: bool = False,
    articleId="defaultArticle",
    removeCloneId=False,
):
    uid = uuid.uuid4()
    if isinstance(innerSection, list):
        innerSection = "".join(innerSection)

    if isClosable:
        closable = """<div class="icone hover-active button" onclick="this.closest('article').remove()">❌</div>"""
    else:
        closable = ""

    mclass = 'class="toggle"'
    id = ""
    if removeCloneId != "":
        mclass = 'class="toggle removeClone"'
        id = f'id="{removeCloneId}"'
        pass

    return f"""
    <article {mclass} {id}>
        <input type="checkbox" id="toggleDetail{uid}" class="toggleDetail" {"checked" if isOpen else ""}>
        <label for="toggleDetail{uid}" class="hover">
            <H{H}>
                <span>{titel}</span>
                {closable}
            </H{H}>
            
        </label>
        <section  class="toggleContent">
            {innerSection}
        </section>
    </article>
    """


def htmlArticleMain(
    titel: str,
    innerSection: str,
    isOpen: bool = False,
    isClosable=True,
    articleId="articleId",
    removeCloneId="defaultArticle",
):
    return htmlArticle(
        "1",
        titel,
        innerSection,
        isOpen,
        isClosable=isClosable,
        articleId=articleId,
        removeCloneId=removeCloneId,
    )


def htmlArticleH1(
    titel: str, innerSection: str, isOpen: bool = False, isClosable=True, articleId=""
):
    return htmlArticle(
        "1", titel, innerSection, isOpen, isClosable=isClosable, articleId=articleId
    )


def htmlArticleH2(
    titel: str, innerSection: str, isOpen: bool = False, isClosable=False, articleId=""
):
    return htmlArticle(
        "2", titel, innerSection, isOpen, isClosable=isClosable, articleId=articleId
    )


def htmlArticleH3(
    titel: str, innerSection: str, isOpen: bool = False, isClosable=False, articleId=""
):
    return htmlArticle(
        "3", titel, innerSection, isOpen, isClosable=isClosable, articleId=articleId
    )


def htmlArticleH4(
    titel: str, innerSection: str, isOpen: bool = False, isClosable=False, articleId=""
):
    return htmlArticle(
        "4", titel, innerSection, isOpen, isClosable=isClosable, articleId=articleId
    )


# -----------------------------------------------------------------------------
