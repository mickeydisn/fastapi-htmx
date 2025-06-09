
from app.core.service.article import htmlArticleMain
from app.core.service.article import htmlArticleH1
from app.core.service.article import htmlArticleH2
from app.core.service.article import htmlArticleH3
from app.core.service.article import htmlArticleH4
from app.core.service.content.makedown import htmlContentMDJson
from app.core.service.content.makedown import htmlContentMD
from app.core.service.content.makedown import htmlContentMDPyFunction

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def _content_P():
    return  """
        <p>Be simple ! you can use a paragraph to display a text</p>
        <div>No Space, No Color </div>
        <div>
            <p style="border:1px solid #000">Hello </p>
            <p style="border:1px solid #000">Hello</p>
        </div>
    """

def _content_Custom():
    return """
    <div>
        <div style="    
            background: #dede00;
            color:#DEDEFF;
            padding: 1em;
            display: grid;
            grid-template-columns: 1fr 1fr 2fr;
            "
        >
            <span>Custom</span><span>Custom</span><span>Custom</span>
        </div>
    <div>
    """

def _content_Label():
    return """
    <H1> H1 Hello Word - Outside Content div  </H1>
    <H2> H2 Hello Word - Outside Content div  </H2>
    <H3> H3 Hello Word - Outside Content div  </H3>
    <H4> H4 Hello Word - Outside Content div  </H4>
    <hr>
    <div>
        <H1> H1 Hello Word - inside a Content </H1>
        <H2> H2 Hello Word - inside a Content </H2>
        <H3> H3 Hello Word - inside a Content </H3>
        <H4> H4 Hello Word - inside a Content </H4>
    </div>
    """

def _content_Article():
    subcontent = '<div> Content of the article </div>'
    subcontent1 = '<div> Content of the article </div>'
    return htmlArticleH2("Sub Article Title", [
        subcontent, 
        subcontent1
    ], isOpen=True)

def _content_Article2():
    art1_content_into = '<div> Article 1 Intoducton, </div>'
    art1_1_1_content = '<div> Content of the article </div>'

    return  htmlArticleH2("Article 1", isOpen=True, innerSection=[
        art1_content_into,
        htmlArticleH3("Article 1_1", isOpen=True, innerSection=[
            htmlArticleH4("Article 1_1_1", isOpen=True, innerSection=[
                art1_1_1_content
            ])
        ])
    ])


def htmlH1_Exemple2():
    content = []

    fns = [
        _content_P,
        _content_Custom,
        _content_Label,
        _content_Article,
        _content_Article2,
    ]

    for f in fns:
        article = htmlArticleH2(
            f.__name__, [
                htmlContentMDPyFunction(f),
                f() ],
            isOpen=False )
        content.append(article)

    return htmlArticleMain(
        'Exemple 2 : Article content components', 
        content,
        isOpen=True)


