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
