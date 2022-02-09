import sys
import requests
from requests.models import MissingSchema, ReadTimeoutError
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError
from requests.packages.urllib3.connectionpool import HTTPConnectionPool
from urllib3.exceptions import InsecureRequestWarning
import json


def _make_request(self, conn, method, url, **kwargs):
    response = self._old_make_request(conn, method, url, **kwargs)
    sock = getattr(conn, 'sock', False)
    if sock:
        setattr(response, 'peer', sock.getpeername())
    else:
        setattr(response, 'peer', None)
    return response


HTTPConnectionPool._old_make_request = HTTPConnectionPool._make_request
HTTPConnectionPool._make_request = _make_request
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class HostInformation():
    def __init__(self, host, timeout):
        self.Host = host
        self.Timeout = timeout
        self.IPAddress = ""
        self.Port = 0
        self.Country = ""
        self.City = ""
        self.Timezone = ""
        self.ISP = ""
        self.Organization = ""
        self.Latitude = ""
        self.Longitude = ""

    def MakeRequest(self, host):
        try:
            response = requests.get(host, timeout=self.Timeout, verify=False)
        except requests.exceptions.ReadTimeout:
            print("[ERROR] ReadTimeout")
            return None
        except requests.exceptions.ConnectTimeout:
            print("[ERROR] ConnectTimeout")
            return None
        except MaxRetryError:
            print("[ERROR] MaxRetryError")
            return None
        except MissingSchema:
            print("[ERROR] MissingSchema")
            return None
        except requests.exceptions.ConnectionError:
            print("[ERROR] ConnectionError")
            return None
        return response

    def SetHostInformation(self):
        if self.Host != None:
            response = self.MakeRequest(self.Host)
            if response == None:
                return -1
            else:
                self.IPAddress = response.raw._original_response.peer[0]
                self.Port = response.raw._original_response.peer[1]

        geoInfoResponse = self.MakeRequest("http://ip-api.com/json/" + self.IPAddress)  # has no relation with owner of this code. Please implement this line as your own responsibility
        if geoInfoResponse == None:
            return -1
        jsonResponse = json.loads(geoInfoResponse.text)
        self.Country = jsonResponse["country"]
        self.City = jsonResponse["regionName"]
        self.Timezone = jsonResponse["timezone"]
        self.Latitude = jsonResponse["lat"]
        self.Longitude = jsonResponse["lon"]
        self.ISP = jsonResponse["isp"]
        self.Organization = jsonResponse["org"]
        return 1
    
    
