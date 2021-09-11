# Python Async HTTP Requests

Given a list of urls and payloads, perform async requests against each entry.

Includes request metrics such as datetime when request made, response latency and response size.

Reuses single session for connection pooling, along with using AsyncIO Semaphores to cap the number of requests being executed within a time window, as a basic form of rate limiting.
Note: this rate limiting only works if the response is relatively quick, otherwise we will end up waiting for the window period even though it may have already elapsed in the delay waiting for the request to complete.
TODO: add logic to wait following request end for period remaining within desired window period (window - request latency).

Responses are tested against an implementation of http://httpbin.org/#/.
