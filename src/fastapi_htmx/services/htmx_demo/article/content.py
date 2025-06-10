
from fastapi_htmx.core.service.article import htmlArticleMain
from fastapi_htmx.core.service.article import htmlArticleH2
from fastapi_htmx.core.service.article import htmlArticleH3

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlH1_Exemple2():
    articleContent = ""
    articleContent += """
        <label><h1>Bonjour H1</h1></label>
            <p>Bonjour H1</p>
        <label><h2>Bonjour H2</h2></label>
            <p>Bonjour H2</p>
        <label><h3>Bonjour H3</h3></label>
            <p>Bonjour H3</p>
        <label><h4>Bonjour H4</h4></label>
            <p>Bonjour H4</p>
    """
    return f"""
        {htmlArticleMain('Exemple of Content', articleContent, isOpen=True)}
    """


def htmlH1_Exemple3():
    articleContent = ""

    htmlGroup3 = htmlArticleH3("SousSous", '<div class="text"> ContentH3 in ContentH2 </div>', isOpen=False)
    articleContent += htmlArticleH2("H2 -> H3", htmlGroup3, isOpen=True)

    htmlGroup2 = htmlArticleH2("SousSous", '<div class="text"> ContentH3 in ContentH2 </div>', isOpen=False)
    articleContent += htmlArticleH3("H3 -> H2", htmlGroup2, isOpen=True)

    return f"""
        {htmlArticleMain('Exemple of Content', articleContent, isOpen=True)}
    """
