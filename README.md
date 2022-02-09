# response-time
Measure Web Server Response Time (Latency)

### Usage
`python latency.py [URL] [NUMBER_OF_ATTEMPTS]`

### Output
```
$ python latency.py github.com 5

Given host address: https://github.com

Connected to https://github.com at 140.82.121.4:443

Host Details
Country      : Germany
City         : Hesse
Timezone     : Europe/Berlin
ISP          : GitHub, Inc.
Organization : GitHub, Inc.
Latitude     : 50.1109
Longitude    : 8.68213

         1  0.2117   s [200]
         2  0.205    s [200]
         3  0.2166   s [200]
         4  0.2378   s [200]
         5  0.2176   s [200]

Results
       Min  0.205    s
       Max  0.2378   s
   Average  0.2177   s

Status 200 occured 5 times.
```

### FAQ
- What is time unit?
  - Seconds. `response.elapsed.total_seconds()` 
- Can I measure latency for http:// hosts?
  - Yes. Just specify it. If you do **NOT** specify, this script will assume it is **https://**.
    - ```$ python latency.py stackoverflow.com 10``` -> Will try connect **https**.
    - ```$ python latency.py https://stackoverflow.com 10``` -> Will try connect **https**.
    - ```$ python latency.py http://stackoverflow.com 10``` -> Will try to connect **http**.

  