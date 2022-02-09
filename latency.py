import sys
from time import time
import requests
from requests.models import MissingSchema, ReadTimeoutError
from HostInformation import HostInformation
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError
from collections import Counter

try:
    verifySslStatus = False #edit if you want to.
    url = sys.argv[1]
    attempts = int(sys.argv[2])
    timeout = 5
    totalTime = 0
    maxTime = -1
    minTime = sys.maxsize
    printHostInfo = True
    statusCodesList = []
    if url[:7] != "http://" and url[:8] != "https://":
        url = "https://" + url

    print(f"\nGiven host address: {url}\n")
    hostInformation = HostInformation(url, timeout)
    if hostInformation.SetHostInformation() == -1:
        exit(0)

    print(f'Connected to {hostInformation.Host} at {hostInformation.IPAddress}:{hostInformation.Port}\n')

    print(f'Host Details')
    print(f'{"Country":{13}}: {hostInformation.Country:{30}}')
    print(f'{"City":{13}}: {hostInformation.City:{30}}')
    print(f'{"Timezone":{13}}: {hostInformation.Timezone:{30}}')
    print(f'{"ISP":{13}}: {hostInformation.ISP:{30}}')
    print(f'{"Organization":{13}}: {hostInformation.Organization:{30}}')
    print(f'{"Latitude":{13}}: {hostInformation.Latitude:<{30}}')
    print(f'{"Longitude":{13}}: {hostInformation.Longitude:<{30}}\n')

    for i in range(0, attempts):
        try:
            response = requests.get(url, timeout=timeout, verify=verifySslStatus)

            totalTime += response.elapsed.total_seconds()
            if (response.elapsed.total_seconds() < minTime):
                minTime = response.elapsed.total_seconds()

            if (response.elapsed.total_seconds() > maxTime):
                maxTime = response.elapsed.total_seconds()

            print(f'{i+1:>{10}}  {response.elapsed.total_seconds():<{8.4}} s [{response.status_code:>}]')
            statusCodesList.append(response.status_code)

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
            print('You may set verifySslStatus to False.')
            exit(0)
        except KeyboardInterrupt:
            break

    # print('{:10}'.format('Results'))
    print(f'\n{"Results":{10}}')
    print(f'{"Min":>{10}}  {minTime:<{8.4}} {"s":{3}}')
    print(f'{"Max":>{10}}  {maxTime:<{8.4}} {"s":{3}}')
    print(f'{"Average":>{10}}  {totalTime / attempts:<{8.4}} {"s":{3}}\n')
    countedStatusCodeList = Counter(statusCodesList)
    for statusCode in countedStatusCodeList.keys():
        print(f'{statusCode} occured {countedStatusCodeList[statusCode]} times.')


except IndexError:
    print('Usage: latency.py URL Number_Of_Attempts')
    exit(0)
except ValueError:
    print("Value error")
    exit(0)
