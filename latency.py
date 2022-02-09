import sys
import requests
from requests.models import MissingSchema, ReadTimeoutError
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError
from requests.packages.urllib3.connectionpool import HTTPConnectionPool


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

try:
    url = sys.argv[1]
    attempts = int(sys.argv[2])
    timeout = 3
    totalTime = 0
    maxTime = -1
    minTime = sys.maxsize
    printHostInfo = True
    if url[:7] != "http://" and url[:8] != "https://":        
        url = "https://" + url
        
    print(f"Given host address: {url}")
    
    for i in range(0, attempts):
        try:
            response = requests.get(url, timeout=timeout)
            if printHostInfo:
                print(f'Host: {url}')
                print(f'Connected to host at {response.raw._original_response.peer[0]}:{response.raw._original_response.peer[1]}')
                printHostInfo = False

            totalTime += response.elapsed.total_seconds()
            if (response.elapsed.total_seconds() < minTime):
                minTime = response.elapsed.total_seconds()

            if (response.elapsed.total_seconds() > maxTime):
                maxTime = response.elapsed.total_seconds()

            print(f'{i+1:{12}} {response.elapsed.total_seconds():>{10.4}} s [{response.status_code}]')

        except requests.exceptions.ReadTimeout:
            print(f'{i+1:{12}} {"timeout":{10}} [ReadTimeout]')
            pass
        except requests.exceptions.ConnectTimeout:
            print(f'{i+1:{12}} {"timeout":{10}} [ConnectTimeout] (If host address is correct try to switch between http:// and https://)')
            pass
        except MaxRetryError:
            print(f'{i+1:{12}} {"timeout":{10}} [MaxRetryError]')
            pass
        except MissingSchema:
            print('Do not forget http:// or https://.')
            exit(0)
        except requests.exceptions.ConnectionError:
            print('Could not find the host.')
            exit(0)
        except KeyboardInterrupt:
            break

    # print('{:10}'.format('Results'))
    print(f'{"Results":{10}}')
    print(f'{"Min":{10}} {minTime:{10.4}} {"s":{3}}')
    print(f'{"Max":{10}} {maxTime:{10.4}} {"s":{3}}')
    print(f'{"Average":{10}} {totalTime / attempts:{10.4}} {"s":{3}}')

except IndexError:
    print('Usage: latency.py URL Number_Of_Attempts')
    exit(0)
except ValueError:
    print("Value error")
    exit(0)
