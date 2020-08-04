
### 5. View dashboards

#### Install kubernetes Web UI ([dashboard](https://github.com/kubernetes/dashboard))  (_recommend not using dashboard on remote clusters_)  

This will create a local admin-user and launch the kubernetes dashboard.    

```bash
$ inv deploy.dash
```

To view the dashboard:
```bash
$ inv view.dash
dashboard token copied to clipboard
Starting to serve on 127.0.0.1:8001
```
A browser windows will appear. Select the `token` authentication method and Ctrl-V to paste  
the admin-user token in your clipboard. (You will receive a 'unsigned' cert error message.)

#### Istio Dashboards

$ istioctl dashboard grafana
$ istioctl dashboard kiali
$ istioctl dashbaord jaeger
$ istioctl dashboard prometheus

Port-forward the appropriate services for access on localhost. See [cheat sheet](cheat_sheet.md) for individual interfaces.  

```bash
$ invoke view.istio         # forward istio premetheus, grafana, jaeger, and kiali services
```

Example: Access Grafana view of istio prometheus metrics on http://localhost:9090/graph.  

Kill all forwarders  

```bash
$ inv view.off
```
