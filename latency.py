import sys
import requests
from requests.models import MissingSchema, ReadTimeoutError
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError

try:

    url = sys.argv[1]
    attempts = int(sys.argv[2])
    timeout = 1
    total_time = 0
    max_time = -1
    min_time = sys.maxsize
    for i in range(0, attempts):
        try:
            response = requests.get(url, timeout=timeout)
            total_time += response.elapsed.total_seconds()
            if (response.elapsed.total_seconds() < min_time):
                min_time = response.elapsed.total_seconds()
            if (response.elapsed.total_seconds() > max_time):
                max_time = response.elapsed.total_seconds()
            print(f'{i+1:{12}} {response.elapsed.total_seconds():>{10.4}} s')

        except requests.exceptions.ReadTimeout:
            print(f'{i+1:{12}} {"timeout":{10}}')
            pass
        except requests.exceptions.ConnectTimeout:
            print(f'{i+1:{12}} {"timeout":{10}}')
            pass
        except MaxRetryError:
            print(f'{i+1:{12}} {"timeout":{10}}')
            pass
        except MissingSchema:
            print('Do not forget http:// or https://.')
            exit(0)
        except KeyboardInterrupt:
            break

    # print('{:10}'.format('Results'))
    print(f'{"Results":{10}}')
    print(f'{"Min":{10}} {min_time:{10.4}} {"s":{3}}')
    print(f'{"Max":{10}} {max_time:{10.4}} {"s":{3}}')
    print(f'{"Average":{10}} {total_time / attempts:{10.4}} {"s":{3}}')

except IndexError:
    print('Usage: latency.py URL Number_Of_Attempts')
    exit(0)
