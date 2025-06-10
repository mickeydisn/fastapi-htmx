# -------------------
# Start the service App
from fastapi_htmx.services.service_app import app


"""
from fastapi_htmx.core.connector.dremioConnector import DremioExplorer
de = DremioExplorer()
print( de.catalogs() )
"""

"""
from fastapi_htmx.datahub.dremio_api.server import Dremio
import urllib3
import warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)


dremio: Dremio = Dremio()
tree = dremio.crawl_tree(recursive=False)
print(tree)

"""
