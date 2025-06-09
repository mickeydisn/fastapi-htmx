
# -------------------
# Start the service App
from app.services.service_app import app



"""
from app.core.connector.dremioConnector import DremioExplorer
de = DremioExplorer()
print( de.catalogs() )
"""

"""
from app.datahub.dremio_api.server import Dremio
import urllib3
import warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)


dremio: Dremio = Dremio()
tree = dremio.crawl_tree(recursive=False)
print(tree)

"""

