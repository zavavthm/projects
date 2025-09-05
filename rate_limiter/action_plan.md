# Action Plan
## Implementation of a rate limiter:
1. Build a sample Flask API that I'll hit to test my rate_limiter service
2. Build an end client service that will replicate an end customer and make requests to the API
3. Build the Rate limiter service that will sit between the client and the API
4. Since it's a POC, host the API on localhost and test the rate limiter service
5. Different rate limiter algorithms to be implemented:
    1. Token Bucket Algorithm
    2. Leaky Bucket Algorithm
    3. Fixed Window
    4. Sliding Window

## Edge Cases to Cover:
1. Handling bursts and spikes

## Designing a Rate Limiter Service
1. HLD - components of rate limiting service
2. LLD - Data Model and the OOPS Code Structure to implement the service

## Supporting Docs:
1. https://www.geeksforgeeks.org/system-design/rate-limiting-algorithms-system-design/