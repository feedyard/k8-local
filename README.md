# feedyard/k8-local

_review the dependencies section below for laptop setup_  

Starting with a fresh install of docker-for-mac and kubernetes  
(setting memory available to docker resources to 8gb recommended)  

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

Port forwards the kubernetes dashboard and open the login screen. Token will be in the clipboard. Select token login  
options and cmd-v + return to access.  

```bash
$ inv view.dash
```

Port-forward the appropriate services for access on localhost. See cheat_sheet.md for individual interfaces.  

```bash
$ invoke view.istio         # forward istio premetheus, grafana, jaeger, and kiali services
```

Example: Access Grafana view of istio prometheus metrics on http://localhost:9090/graph.  

Kill all forwaders  

```bash
$ inv view.off
```

## sources
  
• [metrics-server](https://github.com/kubernetes-incubator/metrics-server)
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
• [istio](https://istio.io)
• [kubernetes dashboard](https://github.com/kubernetes/dashboard) (_recommend not using dashboard on remote clusters_)
