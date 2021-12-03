import sys
import requests
from requests.models import ReadTimeoutError

try:
    url = sys.argv[1]
    tries = int(sys.argv[2])
    timeout = 50
    total_time = 0
    max_time = -1
    min_time = sys.maxsize
    for i in range(0, tries):
        response = requests.get(url, timeout=timeout)
        total_time += response.elapsed.total_seconds()
        if response.elapsed.total_seconds() < min_time:
            min_time = response.elapsed.total_seconds()
        if response.elapsed.total_seconds() > max_time:
            max_time = response.elapsed.total_seconds()
        print('{:10d}{:10f}{:10}'.format(
            i+1, response.elapsed.total_seconds(), ' s'))
    print('{:10}'.format(
        'Results'))
    print('{:10}{:10f}{:10}'.format(
        'Min', min_time, ' s'))
    print('{:10}{:10f}{:10}'.format(
        'Max', max_time, ' s'))
    print('{:10}{:10f}{:10}'.format(
        'Average', total_time/tries, ' s'))
except IndexError:
    print('Usage: latency.py URL Number_Of_Tries')
    exit(0)
