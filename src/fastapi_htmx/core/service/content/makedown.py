import uuid
import json
import inspect

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlContentMD(markdown):
    def escape_html(text):
        return (
            text.replace("&", "&amp;")  # Must come first
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    md = escape_html(markdown)
    return f"""<div class="markdown">{md}</div>"""


def htmlContentMDPython(mstr):
    return htmlContentMD(f"```python\n{mstr}\n```")


def htmlContentMDPyFunction(mfunction):
    f = inspect.getsource(mfunction)
    return htmlContentMD(f"```python\n{f}\n```")


def htmlContentMDHtml(str):
    return htmlContentMD(f"```htlm\n{str}\n```")


def htmlContentMDJson(mjson):
    return htmlContentMD(f"```htlm\n{json.dumps(mjson, indent=2)}\n```")


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def htmlContentMD_exemple():
    md = """
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

    return htmlContentMD(md)
