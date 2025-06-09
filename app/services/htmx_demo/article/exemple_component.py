import inspect

from app.core.service.article import htmlArticleH2
from app.core.service.article import htmlArticleMain
from app.core.service.content.makedown import htmlContentMD
from app.core.service.content.makedown import htmlContentMDJson

from app.core.service.content.makedown import htmlContentMDPyFunction

from app.core.service.content.chart import htmlContentChart_exemple
from app.core.service.content.panda_chart import htmlContentPandaChartTimeSerie_exemple


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlH2_Exemple_Component_MarkDown():
    
    md =  f"""
# Hello Work
## Hello Work
### Hello Work
#### Hello Work

> i'm fine thanks,

_Cool_ : 

 - What ? 
 - *How ?*  
 - **How ?**  
 - ***How ?***  
 - _Better_ ?_
 - __Better__ ?
 - ___Better___ ?
 - code :  `and inlin code`  ?
 - ~~The world is flat.~~
 
Check ? 
 - [x] Write the press release
 - [ ] Update the website
 - [ ] Contact the media


 
-----

```
and multiline inlin 
code
is possible ?
```

-----

| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |


| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |

-----


```json
{{
    "Home": "Is Home",
    "Space": "Is Empty"
}}
```
-----

</div>"""

    return htmlArticleH2(
        'Componenet Markdown', 
        htmlContentMD(md), 
        isOpen=False
    )



def htmlH2_Exemple_Component_json():
    doc = f'''
### Exemple Usage - in python inside a article : 

```python
{htmlArticleH2.__code__}
```

### Exemple Usage - direct used in html : 

```html
    <div class="markdonw">
{"```json\nHello\n```"}
    </div>
```
    '''
    
    data = {"Hello": "World", "World": "Hello"}
    return htmlArticleH2(
        'Componenet JSON', "".join([
            htmlContentMD(doc),
            htmlContentJson(data)
        ]), 
        isOpen=False
    )


def htmlH2_Exemple_Component_chart():
    return htmlArticleH2('Componenet Chart', "".join([
            htmlContentMD("htmlContentChart_exemple.__code__"),
            htmlContentChart_exemple()
        ]), 
        isOpen=False
    )

def htmlH2_Exemple_Component_pandaChart():
    return htmlArticleH2('Componenet PandaChart', "".join([
            htmlContentMDPyFunction(htmlContentPandaChartTimeSerie_exemple),
            htmlContentPandaChartTimeSerie_exemple()
        ]), 
        isOpen=True
    )


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def htmlH1_Exemple_Component():
    h2Articles = [
        # htmlH2_Exemple_Component_MarkDown(),
        # htmlH2_Exemple_Component_json(),
        # htmlH2_Exemple_Component_chart(),
        htmlH2_Exemple_Component_pandaChart(),
    ]

    return htmlArticleMain(
        'Componenet Demo', "".join(h2Articles), isOpen=True)
        