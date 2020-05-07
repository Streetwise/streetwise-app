# Profiling Streetwise

## Enabling the profiler
The application can be run with profile enabled as follows:
```shell
manage.py profile
```

## Running the perf test
The performance tests are designed to hit the APIs using the [Vegeta utility](https://github.com/tsenart/vegeta)

The [requests](./requests) file contains the APIs that would be hit as part of the performance test. The headers and body parameters can also be configured in here. The parameters if any can be configured in different files. For instance the [vote.json](./vote.json) contains the body params used for making the `/api/vote/` request.

The perf test itself can be run as follows:
```
cat requests | vegeta attack -duration=20s -rate=1 > results
```
This will run the perf test at the break neck speed of 1 request per second for 20 seconds.

## Creating Graphs / Metrics out of resultset
### metrics
```
vegeta report -type=json results > metrics.json
```
### graphs
cat results | vegeta plot > latency.html
```
