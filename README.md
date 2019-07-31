# feedyard/k8-local

_basic setup for local kubernetes development_  

Starting with a fresh install of docker-for-mac and kubernetes  
(setting memory available to docker resources to 8gb)  

## 1. Edit kubernetes manifest for AdmissionController settings  
```bash
$ screen  ~/Library/Containers/com.docker.docker/Data/vms/0/tty
$ vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

edit the following line: (_add text in bold_)  

--enable-admission-plugins=Initializers,NodeRestriction,__MutatingAdmissionWebhook,ValidatingAdmissionWebhook__  

Restart Docker for Mac   

## 2. Installable services  

### To see list of pre-defined actions:  
```bash
$ invoke -l
```

### Install metrics  

* metrics-server (0.3.3)  
* kube-state-metrics (1.7.0-rc.1)  

```bash
$ invoke deploy.metrics
```

### Install istio  

Get specified version (See tasks/download_versions.py), render istio-demo-auth version of install, and deploy  

```bash
$ inv get.versions
$ inv render.istio
$ deploy.istio
```

### Install kubernetes Web UI (dashboard)

Kubectl port-forward and access on localhost.  

```bash
$ inv deploy.dashboard
```

#### View dashboards

The kubernetes and istio dashboards provide observability into logs and metrics until you have local integration  
with the primary systems.  

Port forwards the kubernetes dashboard and open the login screen. Token will be in the clipboard. Select token login  
options and cmd-v + return to access.  

```bash
$ inv view.dash
```

Port-forward the appropriate services for access on localhost. See [cheat sheet](cheat_sheet.md) for individual interfaces.  

```bash
$ invoke view.istio         # forward istio premetheus, grafana, jaeger, and kiali services
```

Example: Access Grafana view of istio prometheus metrics on http://localhost:9090/graph.  

Kill all forwarders  

```bash
$ inv view.off
```
#### see the following for more setup and local development capabilities  

[stern](https://github.com/wercker/stern)
[kube-ps1](https://github.com/jonmosco/kube-ps1) prompt tool  
[kubefwd](https://github.com/txn2/kubefwd)  
[hadolint](https://github.com/hadolint/hadolint) Dockerfile lint/inspection  
[kubeval](https://github.com/garethr/kubeval) k8 yaml lint/inspection  
[sonabouy](https://github.com/heptio/sonobuoy)  


## sources

• [metrics-server](https://github.com/kubernetes-incubator/metrics-server)
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
• [istio](https://istio.io)
• [kubernetes dashboard](https://github.com/kubernetes/dashboard) (_recommend not using dashboard on remote clusters_)
