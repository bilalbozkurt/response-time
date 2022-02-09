# response-time
**Measure Web Server Response Time (Latency)**
response-time measures latency of a web server with your own connection. It also includes distance in km of you and remote host.
### Use Cases
- Checking web applications latency.
- Checking API's response time.
- etc.

### Usage
`python latency.py [URL] [NUMBER_OF_ATTEMPTS]`

### Output
```
$ python latency.py github.com 5

Given host address: https://github.com

Connected to https://github.com at 140.82.121.3:443

Remote Host Details
Country      : Germany
City         : Hesse
Timezone     : Europe/Berlin
ISP          : GitHub, Inc.
Organization : GitHub, Inc.
Latitude     : 50.1109
Longitude    : 8.68213

Local Host Details
Country      : Turkey
City         : ***
Timezone     : Europe/Istanbul
ISP          : ***
Organization : ***
Latitude     : ***
Longitude    : ***

Distance between two hostes is approximately 2553.3 km.

         1  0.2121   s [200]
         2  0.1873   s [200]
         3  0.1925   s [200]
         4  0.1911   s [200]
         5  0.1936   s [200]

Results
       Min  0.1873   s
       Max  0.2121   s
   Average  0.1953   s

Status 200 occured 5 times.
```

### FAQ
- What is measurement unit?
    - Seconds. `response.elapsed.total_seconds()` 
- Can I measure latency for http:// hosts?
  - Yes. Just specify it. If you do **NOT** specify, this script will assume it is **https://**.
    - ```$ python latency.py github.com 10``` -> Will try connect **https**.
    - ```$ python latency.py https://github.com 10``` -> Will try connect **https**.
    - ```$ python latency.py http://github.com 10``` -> Will try to connect **http**.
- What are local host details?
  - They are your local connection details such as ISP, country, city etc.
- What is ```http://ip-api.com/json/```?
  - Actually I have **not** done a deep research about it but it basically returns geo informations of given ip address.
- How does this script know my own IP address?
  - It does **not**. ```http://ip-api.com/json/``` returns your own geo details if no IP address is given.

  