import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    # Configuration
    DREMIO_SERVER= "datahub.preprod.internal.dpdgroup.com"
    DREMIO_PORT= "443"
    DREMIO_HOST = "https://" + DREMIO_SERVER + "" # + ":" + DREMIO_PORT
    USERNAME = "jschluth"
    PASSWORD = "Xo@ELh8D0f!Mfjozdj_ODR"
"""
from fastapi_htmx.config.configClass import DAConfig

DREMIO_SERVER= DAConfig.DREMIO_SERVER
DREMIO_PORT= DAConfig.DREMIO_PORT
DREMIO_HOST = "https://" + DAConfig.DREMIO_SERVER + "" 
USERNAME = DAConfig.DREMIO_USER
PASSWORD = DAConfig.DREMIO_PASSWORD


class DremioHelper:
    def __init__(self):
        self.authenticate()
        pass

    def authenticate(self):
        url = f"{DREMIO_HOST}/apiv2/login"
        payload = {"userName": USERNAME, "password": PASSWORD}
        print (url)
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload, verify=False)
        print (response.status_code)
        response.raise_for_status()
        self.token = response.json()["token"]


    def _build_url (self, path) -> str : 
        return  f"{DREMIO_HOST}{path}"

    def _augment_headers(self) -> dict: 
        return {
            "Content-Type": "application/json",
            "Authorization": f"_dremio{self.token}"
        }

    def _handel_json_array_reponce(self, response): 
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def get(
        self, path: str
    ) -> requests.Response:
        url = self._build_url(path)
        response = requests.get(url, headers=self._augment_headers(), verify=False)
        return response

    def getJson(
        self, 
        path: str
    ) -> list[dict[str,any]]:
        return self._handel_json_array_reponce(self.get(path))

    def post(
        self,
        path: str,
        data: dict[str, any] = None,
    ) -> requests.Response:
        url = self._build_url(path)
        response = requests.post(url, headers=self._augment_headers(), data=data, verify=False)
        print ('======================')
        print (response)
        print ('======================')
        return response
    
    def postJson(
        self, 
        path: str,
        data: dict[str, any] = None,
    ) -> list[dict[str,any]]:
        return self._handel_json_array_reponce(self.post(path, data))
    



class DremioExplorer(DremioHelper) : 
    def __init__(self):
        super().__init__()

    def catalogs(self):
        catalogs = self.getJson("/api/v3/catalog")   
        return catalogs    


