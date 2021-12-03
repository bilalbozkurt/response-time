import sys
import requests
from requests.models import MissingSchema, ReadTimeoutError
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError

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
        print('{:12d}{:10f}{:10}'.format(
            i+1, response.elapsed.total_seconds(), ' s'))

    except IndexError:
        print('Usage: latency.py URL Number_Of_Attempts')
        exit(0)
    except requests.exceptions.ReadTimeout:
        print('{:12d}{:10}'.format(i+1, '  Timeout'))
        pass
    except requests.exceptions.ConnectTimeout:
        print('{:12d}{:10}'.format(i+1, '  Timeout'))
        pass
    except MaxRetryError:
        print('{:12d}{:10}'.format(i+1, '  Timeout'))
        pass
    except MissingSchema:
        print('Do not forget http:// or https://.')
        exit(0)
    except KeyboardInterrupt:
        break
    
print('{:10}'.format(
    'Results'))
print('{:10}{:10f}{:10}'.format(
    'Min', min_time, ' s'))
print('{:10}{:10f}{:10}'.format(
    'Max', max_time, ' s'))
print('{:10}{:10f}{:10}'.format(
    'Average', total_time/attempts, ' s'))
