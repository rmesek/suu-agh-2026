# Lab: Managing Containers (II)

**Name:** Robert Mesek  
**Lab:** 2  
**Date:** April 16, 2026

---

## Task -1 - Prepare and Verify your environment

Task -1.1
```zsh
Used $0 of $50
```

Task -1.2
```zsh
% kubectl get nodes
% kubectl get nodes
NAME                            STATUS   ROLES    AGE   VERSION
ip-172-31-17-152.ec2.internal   Ready    <none>   57s   v1.35.3-eks-bbe087e
ip-172-31-83-121.ec2.internal   Ready    <none>   53s   v1.35.3-eks-bbe087e
ip-172-31-87-173.ec2.internal   Ready    <none>   47s   v1.35.3-eks-bbe087e
```

```zsh
% kubectl --namespace kube-system get pods
NAME                              READY   STATUS    RESTARTS   AGE
coredns-cd49f47f8-7pkkq           0/1     Pending   0          71s
coredns-cd49f47f8-l292v           0/1     Pending   0          71s
metrics-server-68dd5c6f99-82cpl   0/1     Pending   0          71s
metrics-server-68dd5c6f99-8vxv5   0/1     Pending   0          71s
```

## Task 0 - Create sample application

Task 0
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kuard-dep
  namespace: suu
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kuard
  template:
    metadata:
      labels:
        app: kuard
    spec:
      containers:
        - name: kuard
          image: jmutai/kuard-amd64:blue
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: kuard-srv
  namespace: suu
spec:
  type: LoadBalancer
  selector:
    app: kuard
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

## Task 1 - Readiness and Liveness endpoints

Task 1
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kuard-dep
  namespace: suu
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kuard
  template:
    metadata:
      labels:
        app: kuard
    spec:
      containers:
        - name: kuard
          image: jmutai/kuard-amd64:blue
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /healthy
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: kuard-srv
  namespace: suu
spec:
  type: LoadBalancer
  selector:
    app: kuard
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

## Task 2 - Adding jobs

Task 2
```zsh
% kubectl describe job -n suu
Name:             kuard-job
Namespace:        suu
Selector:         batch.kubernetes.io/controller-uid=8b0a2d2e-0986-495e-b047-4bd472d10eaf
Labels:           batch.kubernetes.io/controller-uid=8b0a2d2e-0986-495e-b047-4bd472d10eaf
                  batch.kubernetes.io/job-name=kuard-job
                  controller-uid=8b0a2d2e-0986-495e-b047-4bd472d10eaf
                  job-name=kuard-job
Annotations:      <none>
Parallelism:      1
Completions:      1
Completion Mode:  NonIndexed
Suspend:          false
Backoff Limit:    6
Start Time:       Thu, 16 Apr 2026 12:36:28 +0200
Completed At:     Thu, 16 Apr 2026 12:36:38 +0200
Duration:         10s
Pods Statuses:    0 Active (0 Ready) / 1 Succeeded / 0 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=8b0a2d2e-0986-495e-b047-4bd472d10eaf
           batch.kubernetes.io/job-name=kuard-job
           controller-uid=8b0a2d2e-0986-495e-b047-4bd472d10eaf
           job-name=kuard-job
  Containers:
   query-client:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      for i in 1 2 3 4 5; do wget -qO- http://kuard-srv; sleep 1; done
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  90s   job-controller  Created pod: kuard-job-hpqtg
  Normal  Completed         80s   job-controller  Job completed
```

```zsh
% kubectl logs job/kuard-job -n suu
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>KUAR Demo</title>

  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/styles.css">

  <script>
var pageContext = {"urlBase":"","hostname":"kuard-dep-79bb6d7789-vtnwj","addrs":["172.31.88.93"],"version":"v0.10.0-blue","versionColor":"hsl(339,100%,50%)","requestDump":"GET / HTTP/1.1\r\nHost: kuard-srv\r\nConnection: close\r\nConnection: close\r\nUser-Agent: Wget","requestProto":"HTTP/1.1","requestAddr":"172.31.89.207:38530"}
  </script>
</head>


<svg style="position: absolute; width: 0; height: 0; overflow: hidden;" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<symbol id="icon-power" viewBox="0 0 32 32">
<title>power</title>
<path class="path1" d="M12 0l-12 16h12l-8 16 28-20h-16l12-12z"></path>
</symbol>
<symbol id="icon-notification" viewBox="0 0 32 32">
<title>notification</title>
<path class="path1" d="M16 3c-3.472 0-6.737 1.352-9.192 3.808s-3.808 5.72-3.808 9.192c0 3.472 1.352 6.737 3.808 9.192s5.72 3.808 9.192 3.808c3.472 0 6.737-1.352 9.192-3.808s3.808-5.72 3.808-9.192c0-3.472-1.352-6.737-3.808-9.192s-5.72-3.808-9.192-3.808zM16 0v0c8.837 0 16 7.163 16 16s-7.163 16-16 16c-8.837 0-16-7.163-16-16s7.163-16 16-16zM14 22h4v4h-4zM14 6h4v12h-4z"></path>
</symbol>
</defs>
</svg>

<body>
  <div id="root"></div>
  <script src="/built/bundle.js" type="text/javascript"></script>
</body>
</html>
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>KUAR Demo</title>

  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/styles.css">

  <script>
var pageContext = {"urlBase":"","hostname":"kuard-dep-79bb6d7789-7rspn","addrs":["172.31.18.178"],"version":"v0.10.0-blue","versionColor":"hsl(339,100%,50%)","requestDump":"GET / HTTP/1.1\r\nHost: kuard-srv\r\nConnection: close\r\nConnection: close\r\nUser-Agent: Wget","requestProto":"HTTP/1.1","requestAddr":"172.31.89.207:38540"}
  </script>
</head>


<svg style="position: absolute; width: 0; height: 0; overflow: hidden;" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<symbol id="icon-power" viewBox="0 0 32 32">
<title>power</title>
<path class="path1" d="M12 0l-12 16h12l-8 16 28-20h-16l12-12z"></path>
</symbol>
<symbol id="icon-notification" viewBox="0 0 32 32">
<title>notification</title>
<path class="path1" d="M16 3c-3.472 0-6.737 1.352-9.192 3.808s-3.808 5.72-3.808 9.192c0 3.472 1.352 6.737 3.808 9.192s5.72 3.808 9.192 3.808c3.472 0 6.737-1.352 9.192-3.808s3.808-5.72 3.808-9.192c0-3.472-1.352-6.737-3.808-9.192s-5.72-3.808-9.192-3.808zM16 0v0c8.837 0 16 7.163 16 16s-7.163 16-16 16c-8.837 0-16-7.163-16-16s7.163-16 16-16zM14 22h4v4h-4zM14 6h4v12h-4z"></path>
</symbol>
</defs>
</svg>

<body>
  <div id="root"></div>
  <script src="/built/bundle.js" type="text/javascript"></script>
</body>
</html>
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>KUAR Demo</title>

  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/styles.css">

  <script>
var pageContext = {"urlBase":"","hostname":"kuard-dep-79bb6d7789-zgsf5","addrs":["172.31.90.116"],"version":"v0.10.0-blue","versionColor":"hsl(339,100%,50%)","requestDump":"GET / HTTP/1.1\r\nHost: kuard-srv\r\nConnection: close\r\nConnection: close\r\nUser-Agent: Wget","requestProto":"HTTP/1.1","requestAddr":"172.31.89.207:38542"}
  </script>
</head>


<svg style="position: absolute; width: 0; height: 0; overflow: hidden;" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<symbol id="icon-power" viewBox="0 0 32 32">
<title>power</title>
<path class="path1" d="M12 0l-12 16h12l-8 16 28-20h-16l12-12z"></path>
</symbol>
<symbol id="icon-notification" viewBox="0 0 32 32">
<title>notification</title>
<path class="path1" d="M16 3c-3.472 0-6.737 1.352-9.192 3.808s-3.808 5.72-3.808 9.192c0 3.472 1.352 6.737 3.808 9.192s5.72 3.808 9.192 3.808c3.472 0 6.737-1.352 9.192-3.808s3.808-5.72 3.808-9.192c0-3.472-1.352-6.737-3.808-9.192s-5.72-3.808-9.192-3.808zM16 0v0c8.837 0 16 7.163 16 16s-7.163 16-16 16c-8.837 0-16-7.163-16-16s7.163-16 16-16zM14 22h4v4h-4zM14 6h4v12h-4z"></path>
</symbol>
</defs>
</svg>

<body>
  <div id="root"></div>
  <script src="/built/bundle.js" type="text/javascript"></script>
</body>
</html>
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>KUAR Demo</title>

  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/styles.css">

  <script>
var pageContext = {"urlBase":"","hostname":"kuard-dep-79bb6d7789-vtnwj","addrs":["172.31.88.93"],"version":"v0.10.0-blue","versionColor":"hsl(339,100%,50%)","requestDump":"GET / HTTP/1.1\r\nHost: kuard-srv\r\nConnection: close\r\nConnection: close\r\nUser-Agent: Wget","requestProto":"HTTP/1.1","requestAddr":"172.31.89.207:38550"}
  </script>
</head>


<svg style="position: absolute; width: 0; height: 0; overflow: hidden;" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<symbol id="icon-power" viewBox="0 0 32 32">
<title>power</title>
<path class="path1" d="M12 0l-12 16h12l-8 16 28-20h-16l12-12z"></path>
</symbol>
<symbol id="icon-notification" viewBox="0 0 32 32">
<title>notification</title>
<path class="path1" d="M16 3c-3.472 0-6.737 1.352-9.192 3.808s-3.808 5.72-3.808 9.192c0 3.472 1.352 6.737 3.808 9.192s5.72 3.808 9.192 3.808c3.472 0 6.737-1.352 9.192-3.808s3.808-5.72 3.808-9.192c0-3.472-1.352-6.737-3.808-9.192s-5.72-3.808-9.192-3.808zM16 0v0c8.837 0 16 7.163 16 16s-7.163 16-16 16c-8.837 0-16-7.163-16-16s7.163-16 16-16zM14 22h4v4h-4zM14 6h4v12h-4z"></path>
</symbol>
</defs>
</svg>

<body>
  <div id="root"></div>
  <script src="/built/bundle.js" type="text/javascript"></script>
</body>
</html>
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>KUAR Demo</title>

  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/styles.css">

  <script>
var pageContext = {"urlBase":"","hostname":"kuard-dep-79bb6d7789-7rspn","addrs":["172.31.18.178"],"version":"v0.10.0-blue","versionColor":"hsl(339,100%,50%)","requestDump":"GET / HTTP/1.1\r\nHost: kuard-srv\r\nConnection: close\r\nConnection: close\r\nUser-Agent: Wget","requestProto":"HTTP/1.1","requestAddr":"172.31.89.207:38556"}
  </script>
</head>


<svg style="position: absolute; width: 0; height: 0; overflow: hidden;" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<symbol id="icon-power" viewBox="0 0 32 32">
<title>power</title>
<path class="path1" d="M12 0l-12 16h12l-8 16 28-20h-16l12-12z"></path>
</symbol>
<symbol id="icon-notification" viewBox="0 0 32 32">
<title>notification</title>
<path class="path1" d="M16 3c-3.472 0-6.737 1.352-9.192 3.808s-3.808 5.72-3.808 9.192c0 3.472 1.352 6.737 3.808 9.192s5.72 3.808 9.192 3.808c3.472 0 6.737-1.352 9.192-3.808s3.808-5.72 3.808-9.192c0-3.472-1.352-6.737-3.808-9.192s-5.72-3.808-9.192-3.808zM16 0v0c8.837 0 16 7.163 16 16s-7.163 16-16 16c-8.837 0-16-7.163-16-16s7.163-16 16-16zM14 22h4v4h-4zM14 6h4v12h-4z"></path>
</symbol>
</defs>
</svg>

<body>
  <div id="root"></div>
  <script src="/built/bundle.js" type="text/javascript"></script>
</body>
</html>
```

## Task 3 - Horizontal Pod Autoscaler

```zsh
% kubectl describe hpa kuard-dep -n suu
Name:                                                  kuard-dep
Namespace:                                             suu
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Thu, 16 Apr 2026 12:47:18 +0200
Reference:                                             Deployment/kuard-dep
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  24% (24m) / 5%
Min replicas:                                          5
Max replicas:                                          10
Deployment pods:                                       10 current / 10 desired
Conditions:
  Type            Status  Reason            Message
  ----            ------  ------            -------
  AbleToScale     True    ReadyForNewScale  recommended size matches current size
  ScalingActive   True    ValidMetricFound  the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooManyReplicas   the desired replica count is more than the maximum replica count
Events:
  Type     Reason                        Age                  From                       Message
  ----     ------                        ----                 ----                       -------
  Normal   SuccessfulRescale             96s                  horizontal-pod-autoscaler  New size: 10; reason: cpu resource utilization (percentage of request) above target
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kuard-dep
  namespace: suu
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kuard
  template:
    metadata:
      labels:
        app: kuard
    spec:
      containers:
        - name: kuard
          image: jmutai/kuard-amd64:blue
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /healthy
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: kuard-srv
  namespace: suu
spec:
  type: LoadBalancer
  selector:
    app: kuard
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kuard-hpa
  namespace: suu
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kuard-dep
  minReplicas: 5
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 5
---
apiVersion: batch/v1
kind: Job
metadata:
  name: kuard-job
  namespace: suu
spec:
  template:
    spec:
      containers:
        - name: query-client
          image: busybox
          command:
            [
              "sh",
              "-c",
              "for i in 1 2 3 4 5; do wget -qO- http://kuard-srv; sleep 1; done",
            ]
        - name: load-generator
          image: busybox
          command:
            ["sh", "-c", "while true; do wget -qO- http://kuard-srv; done"]
      restartPolicy: Never
```