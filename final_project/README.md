# Appplication Information
1) What does this application do?  
  This application provides a sentiment score as either positive or negative based on a fine tuned distilbert model. To build the application in Azure, use `kubectl apply -k .k8s/overlays/prod`

2) The K6 load test results and grafana dashboard screenshots can be seen below
  ![alt text](https://github.com/UCB-W255/spring23-sshahbuddin/blob/master/final_project/k6_load_results.png?raw=true)  
  ![alt text](https://github.com/UCB-W255/spring23-sshahbuddin/blob/master/final_project/Istio_svc_dashboard.png?raw=true)  


### Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant A as API
    participant M as Model

    U ->> A: POST JSON payload
    break Input payload does not satisfy pydantic schema
        A ->> U: Return Error
    end
    A ->>+ M: Input values to model
    M ->>- A: Store returned values

    A ->> U: Return Values as<br>output data model
```
