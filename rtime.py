import sys
from time import time
import requests
from requests.models import MissingSchema, ReadTimeoutError
from HostInformation import HostInformation
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError
from collections import Counter

from math import sin, cos, sqrt, atan2, radians


def CalculateDistance(latitude1, longitude1, latitude2, longitude2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


try:
    verifySslStatus = False  # edit if you want to.
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
    remoteHostInformation = HostInformation(url, timeout)
    if remoteHostInformation.SetHostInformation() == -1:
        exit(0)
    localHostInformation = HostInformation(None, timeout)
    if localHostInformation.SetHostInformation() == -1:
        exit(0)

    print(f'Connected to {remoteHostInformation.Host} at {remoteHostInformation.IPAddress}:{remoteHostInformation.Port}\n')

    print(f'Remote Host Details')
    print(f'{"Country":{13}}: {remoteHostInformation.Country:{30}}')
    print(f'{"City":{13}}: {remoteHostInformation.City:{30}}')
    print(f'{"Timezone":{13}}: {remoteHostInformation.Timezone:{30}}')
    print(f'{"ISP":{13}}: {remoteHostInformation.ISP:{30}}')
    print(f'{"Organization":{13}}: {remoteHostInformation.Organization:{30}}')
    print(f'{"Latitude":{13}}: {remoteHostInformation.Latitude:<{30}}')
    print(f'{"Longitude":{13}}: {remoteHostInformation.Longitude:<{30}}\n')

    print(f'Local Host Details')
    print(f'{"Country":{13}}: {localHostInformation.Country:{30}}')
    print(f'{"City":{13}}: {localHostInformation.City:{30}}')
    print(f'{"Timezone":{13}}: {localHostInformation.Timezone:{30}}')
    print(f'{"ISP":{13}}: {localHostInformation.ISP:{30}}')
    print(f'{"Organization":{13}}: {localHostInformation.Organization:{30}}')
    print(f'{"Latitude":{13}}: {localHostInformation.Latitude:<{30}}')
    print(f'{"Longitude":{13}}: {localHostInformation.Longitude:<{30}}\n')

    distance = CalculateDistance(remoteHostInformation.Latitude, remoteHostInformation.Longitude, localHostInformation.Latitude, localHostInformation.Longitude)
    print(f'Distance between two hostes is approximately {distance:.1f} km.\n')

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

    print(f'\n{"Results":{10}}')
    print(f'{"Min":>{10}}  {minTime:<{8.4}} {"s":{3}}')
    print(f'{"Max":>{10}}  {maxTime:<{8.4}} {"s":{3}}')
    print(f'{"Average":>{10}}  {totalTime / attempts:<{8.4}} {"s":{3}}\n')
    countedStatusCodeList = Counter(statusCodesList)
    for statusCode in countedStatusCodeList.keys():
        print(f'Status {statusCode} occured {countedStatusCodeList[statusCode]} times.')


except IndexError:
    print('Usage: latency.py URL Number_Of_Attempts')
    exit(0)
except ValueError:
    print("Value error")
    exit(0)
