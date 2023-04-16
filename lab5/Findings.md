# Lab 5 Findings - Shehzad

- [Lab 5 Findings - Shehzad](#lab-5-findings---your-name)
  - [Introduction](#introduction)
  - [Findings](#findings)
    - [Finding 1](#finding-1)
    - [Finding 2](#finding-2)
    - [Finding N](#finding-n)
  - [Conclusion](#conclusion)

---

## Introduction

In this lab, I looked at the performance of the prediction application under load stress from the k6 load.js script. I specifically examined 3 different caching scenarios - 10%, 50%, and 90% cache hit rates. Within those three scenarios, I explored starting with 90% caching, then moving to 10%, then 50% and back to 90% within the same 30 minute period. I then looked at starting with 50% caching to explore the difference in how the pods autoscaled to handle the load. 

## Findings

When the load begin to ramp up, the application takes ~1 minute to scale up to handle the load with a 90% cache hit rate target. During this time, the application response time slows down to  ~250ms for the P99 response. While P50 stays relatively constant, the P90+ sees a dramatic increase in response time. Even after the pods begin scaling out to handle the load, the P99 response stays at ~100 ms until the cluster is able to fully scale out to meet capacity which takes ~1-1.5 additional minutes. Responses then return to ~ 10ms levels once fully scaled out. 

The image below illustrates this Finding. Notice the spike and the gradual decrease once the pods are scaled out.

![alt text](https://github.com/sshahbuddin/UCB-W255/spring23-sshahbuddin/lab5/master/cache_90_workload.png?raw=true)


### Finding 1

While 90% cache hit rates settle at nearly 10ms P99, lowering the cache hit rate drops performance as would be expected when the backend is forced to calculate the response rather than responding directly from cache. 

Examining the 10% cache hit, the P90 is 10ms and the P99 hovers around 20ms. The 50% cache hit rate performs slightly better at sub 20ms for P99.

As expected, higher cache hit rates allow the application to perform better. 

### Finding 2

Once already scaled out, the application is able to maintain performance as the cluster no longer needs to begin provisioning and adding additional pods. Once the capacity hits the target for 10 pods, the application manages load for all subsequent requests. So long as the application continues to receive requests before scaling down, the application is resilient across all cache hit rates. 

### Finding 3

Comparing a cold start on the pods at 90% cache hit rate vs 50% cache hit rate, the P99 of the 50% cache hit rate stays above 200ms for far longer than the 90% cache hit rate. While the 90% begins to peform slightly better after 1 minute while the 50% cache hit rate takes the full ~2 minutes until the full pods scale all the way out to begin performing. 

## Conclusion

In conclusion, leveraging Kubernetes for autoscaling and Redis for caching helps ensure a robust resilient application in the face of increased load. The higher the cache hit rate, the less stress the backend API faces as the model does not need to actively compute the request prediction. While Kubernetes helps ensure the application scales out, there is a lag time for the pods to spin up. Therefore, while autoscaling can be leaned on for dynamic scalability in the event of unforseen load, any anticipated load event should be properly scaled out for before the event to ensure high performance without any degredation. 