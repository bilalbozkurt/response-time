# response-time
Measure Web Server Response Time (Latency)

### Usage
`python latency.py [URL] [NUMBER_OF_TRIES]`

### Output

```$ python latency.py https://github.com 10
         1  0.294950 s        
         2  0.210936 s        
         3  0.200345 s        
         4  0.225527 s        
         5  0.228740 s        
         6  0.231548 s        
         7  0.199812 s        
         8  0.196749 s        
         9  0.206949 s        
        10  0.208530 s        
Results   
Min         0.196749 s
Max         0.294950 s
Average     0.220409 s
```

### FAQ
- What is time unit?
  - Seconds. `response.elapsed.total_seconds()` 
- What happens if timeout occur?
  - Throws an exception and exit. Timeout exception is not added yet.
