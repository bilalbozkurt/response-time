# response-time
Measure Web Server Response Time (Latency)

### Usage
`python latency.py [URL] [NUMBER_OF_ATTEMPTS]`

### Output
```
$ python latency.py stackoverflow.com 10
Given host address: https://stackoverflow.com
Host: https://stackoverflow.com
Connected to host at 151.101.65.69:443
           1     0.4353 s [200]
           2     0.3629 s [200]
           3     0.3397 s [200]
           4     0.3371 s [200]
           5     0.3436 s [200]
           6      0.351 s [200]
           7     0.3358 s [200]
           8     0.3328 s [200]
           9     0.3376 s [200]
          10     0.3472 s [200]
Results
Min            0.3328 s
Max            0.4353 s
Average        0.3523 s
```

### FAQ
- What is time unit?
  - Seconds. `response.elapsed.total_seconds()` 
- Can I measure latency for http:// hosts?
  - Yes. Just specify it. If you do **NOT** specify, this script will assume it is **https://**.
    - ```$ python latency.py stackoverflow.com 10``` -> Will try connect **https**.
    - ```$ python latency.py https://stackoverflow.com 10``` -> Will try connect **https**.
    - ```$ python latency.py http://stackoverflow.com 10``` -> Will try to connect **http**.

  