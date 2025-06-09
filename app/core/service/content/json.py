import uuid
import json

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlContentJson(mjson):
    return f"""
    <div class="markdown">
```json
{json.dumps(mjson, indent=2)}
```
</div>
    """
