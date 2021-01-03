
### 5. Local kubernetes observability

#### Istio Dashboards

$ istioctl dashboard grafana
$ istioctl dashboard kiali
$ istioctl dashbaord jaeger
$ istioctl dashboard prometheus

#### Install kubernetes Web UI ([dashboard](https://github.com/kubernetes/dashboard))  (_recommend not using dashboard on remote clusters_)  

To view the dashboard:  
```bash
$ inv view.dash
dashboard token copied to clipboard
Starting to serve on 127.0.0.1:8001
```
A browser windows will appear. Select the `token` authentication method and Ctrl-V to paste  
the admin-user token in your clipboard. (You will receive a 'unsigned' cert error message.)

To fetch local kubernetes-dashboard user token to the clipboard again:  
```bash
$ inv view.token
```

Kill the dashboard port forwarder:  
```bash
$ inv view.dashoff
```

#### Logs  

[Using](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs) kubectl to view individual pod logs.  

[Stern](https://github.com/wercker/stern): Multi pod and container log tailing for Kubernetes.  

Logs can also be viewed through the kubernetes dashboard.  

