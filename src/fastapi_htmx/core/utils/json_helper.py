import json
from datetime import datetime
from typing import Any


class DASJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d")
        return json.JSONEncoder.default(self, obj)


def dumps(content: Any, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(content, indent=4, cls=DASJSONEncoder)
    else:
        return json.dumps(content, cls=DASJSONEncoder)
