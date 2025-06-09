import json
from datetime import datetime
from typing import Any

import app.config.constants as constants


class DASJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(constants.ISO_8601_DATETIME_FORMAT)
        return json.JSONEncoder.default(self, obj)


def dumps(content: Any, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(content, indent=4, cls=DASJSONEncoder)
    else:
        return json.dumps(content, cls=DASJSONEncoder)
