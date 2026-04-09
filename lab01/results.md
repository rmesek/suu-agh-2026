# Lab: Managing Containers (I)

**Name:** Robert Mesek  
**Lab:** 1  
**Date:** April 9, 2026

---

## Task 0 – Managing Containers

```bash
$ kubectl get nodes
NAME                            STATUS   ROLES    AGE   VERSION
ip-172-31-18-112.ec2.internal   Ready    <none>   16m   v1.35.2-eks-f69f56f
ip-172-31-84-28.ec2.internal    Ready    <none>   16m   v1.35.2-eks-f69f56f
ip-172-31-85-88.ec2.internal    Ready    <none>   16m   v1.35.2-eks-f69f56f
```

```bash
$ kubectl --namespace kube-system get pods
NAME                              READY   STATUS    RESTARTS   AGE
aws-node-fksk4                    2/2     Running   0          16m
aws-node-rq5bx                    2/2     Running   0          16m
aws-node-rxhrv                    2/2     Running   0          16m
coredns-cd49f47f8-2rd5h           1/1     Running   0          23m
coredns-cd49f47f8-wr628           1/1     Running   0          23m
eks-node-monitoring-agent-2szc4   1/1     Running   0          16m
eks-node-monitoring-agent-h2c94   1/1     Running   0          16m
eks-node-monitoring-agent-s7jhr   1/1     Running   0          16m
eks-pod-identity-agent-9sdpb      1/1     Running   0          16m
eks-pod-identity-agent-b2gtb      1/1     Running   0          16m
eks-pod-identity-agent-lhnvt      1/1     Running   0          16m
kube-proxy-cztrn                  1/1     Running   0          16m
kube-proxy-hnx76                  1/1     Running   0          16m
kube-proxy-mtkc9                  1/1     Running   0          16m
metrics-server-68dd5c6f99-77gxc   1/1     Running   0          23m
metrics-server-68dd5c6f99-mlnjs   1/1     Running   0          23m
```

```bash
$ kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
kuard   1/1     Running   0          14m
```

```bash
$ kubectl describe pod kuard
Name:             kuard
Namespace:        default
Priority:         0
Service Account:  default
Node:             ip-172-31-84-28.ec2.internal/172.31.84.28
Start Time:       Thu, 09 Apr 2026 12:40:38 +0200
Labels:           run=kuard
                  topology.kubernetes.io/region=us-east-1
                  topology.kubernetes.io/zone=us-east-1a
Annotations:      <none>
Status:           Running
IP:               172.31.95.81
IPs:
  IP:  172.31.95.81
Containers:
  kuard:
    Container ID:   containerd://e5cbbfdf4c732c43be899227b610b1141fe329c57be5568f2382f20d2b7c58e6
    Image:          jmutai/kuard-amd64:blue
    Image ID:       docker.io/jmutai/kuard-amd64@sha256:4b8b063706ecd9ea3855db6440d727f8c155887627c0da02e1b6f06819a444f7
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Thu, 09 Apr 2026 12:40:39 +0200
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-57rsh (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       True 
  ContainersReady             True 
  PodScheduled                True 
Volumes:
  kube-api-access-57rsh:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  15m   default-scheduler  Successfully assigned default/kuard to ip-172-31-84-28.ec2.internal
  Normal  Pulling    15m   kubelet            Pulling image "jmutai/kuard-amd64:blue"
  Normal  Pulled     15m   kubelet            Successfully pulled image "jmutai/kuard-amd64:blue" in 729ms (729ms including waiting). Image size: 11812099 bytes.
  Normal  Created    15m   kubelet            Container created
  Normal  Started    15m   kubelet            Container started
```

```bash
$ kubectl logs kuard kuard
2026/04/09 10:40:39 Starting kuard version: v0.10.0-blue
2026/04/09 10:40:39 **********************************************************************
2026/04/09 10:40:39 * WARNING: This server may expose sensitive
2026/04/09 10:40:39 * and secret information. Be careful.
2026/04/09 10:40:39 **********************************************************************
2026/04/09 10:40:39 Config: 
{
  "address": ":8080",
  "debug": false,
  "debug-sitedata-dir": "./sitedata",
  "keygen": {
    "enable": false,
    "exit-code": 0,
    "exit-on-complete": false,
    "memq-queue": "",
    "memq-server": "",
    "num-to-gen": 0,
    "time-to-run": 0
  },
  "liveness": {
    "fail-next": 0
  },
  "readiness": {
    "fail-next": 0
  },
  "tls-address": ":8443",
  "tls-dir": "/tls"
}
2026/04/09 10:40:39 Could not find certificates to serve TLS
2026/04/09 10:40:39 Serving on HTTP on :8080
2026/04/09 10:44:37 127.0.0.1:55932 GET /
2026/04/09 10:44:37 Loading template for index.html
2026/04/09 10:48:32 127.0.0.1:57262 GET /
2026/04/09 10:51:04 127.0.0.1:49088 HEAD /
2026/04/09 10:53:25 127.0.0.1:52552 GET /
2026/04/09 10:53:25 127.0.0.1:52552 GET /static/css/bootstrap.min.css
2026/04/09 10:53:25 127.0.0.1:52566 GET /static/css/styles.css
2026/04/09 10:53:25 127.0.0.1:52558 GET /built/bundle.js
2026/04/09 10:53:26 127.0.0.1:52558 GET /favicon.ico
2026/04/09 10:53:47 127.0.0.1:52558 GET /
```

## Task 1 – Managing sets of pods

```bash
$ kubectl describe rs kuard
Name:           kuard-8ddf548cb
Namespace:      default
Selector:       app=kuard,pod-template-hash=8ddf548cb
Labels:         app=kuard
                pod-template-hash=8ddf548cb
Annotations:    deployment.kubernetes.io/desired-replicas: 5
                deployment.kubernetes.io/max-replicas: 7
                deployment.kubernetes.io/revision: 1
Controlled By:  Deployment/kuard
Replicas:       5 current / 5 desired
Pods Status:    0 Running / 5 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=kuard
           pod-template-hash=8ddf548cb
  Containers:
   kuard-amd64:
    Image:         gcr.io/kuar-demo/kuard-amd64:1
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  45s   replicaset-controller  Created pod: kuard-8ddf548cb-2s9fg
  Normal  SuccessfulCreate  45s   replicaset-controller  Created pod: kuard-8ddf548cb-5fmf8
  Normal  SuccessfulCreate  45s   replicaset-controller  Created pod: kuard-8ddf548cb-j8xrh
  Normal  SuccessfulCreate  45s   replicaset-controller  Created pod: kuard-8ddf548cb-m9jqw
  Normal  SuccessfulCreate  45s   replicaset-controller  Created pod: kuard-8ddf548cb-pgpk7
```

```bash
$ kubectl describe rs kuard
Name:           kuard-8ddf548cb
Namespace:      default
Selector:       app=kuard,pod-template-hash=8ddf548cb
Labels:         app=kuard
                pod-template-hash=8ddf548cb
Annotations:    deployment.kubernetes.io/desired-replicas: 5
                deployment.kubernetes.io/max-replicas: 7
                deployment.kubernetes.io/revision: 1
Controlled By:  Deployment/kuard
Replicas:       5 current / 5 desired
Pods Status:    0 Running / 5 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=kuard
           pod-template-hash=8ddf548cb
  Containers:
   kuard-amd64:
    Image:         gcr.io/kuar-demo/kuard-amd64:1
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Events:
  Type    Reason            Age    From                   Message
  ----    ------            ----   ----                   -------
  Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: kuard-8ddf548cb-2s9fg
  Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: kuard-8ddf548cb-5fmf8
  Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: kuard-8ddf548cb-j8xrh
  Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: kuard-8ddf548cb-m9jqw
  Normal  SuccessfulCreate  2m25s  replicaset-controller  Created pod: kuard-8ddf548cb-pgpk7
  Normal  SuccessfulCreate  27s    replicaset-controller  Created pod: kuard-8ddf548cb-fv5pd
```