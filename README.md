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

### Install istio (see `tasks/render.py` and `tasks/download_versions.py` for how additional info)  

Includes: tracing and kiali  
```bash
$ invoke install.istio
```

#### View istio ui  

Kubectl port-forward the appropriate services and access on localhost.  

Shortcuts available:  


```bash
$ invoke view.istio         # forward istio premetheus, grafana, jaeger, and kiali services
$ inv view.istio --window   # -w, forward istio services and open a browser window with shortcuts to localhost interfaces
```

### Install kubernetes Web UI (dashboard)

Kubectl port-forward and access on localhost.  

```bash
$ inv install.dashboard
```

#### view dashboard

```bash
$ inv view.dash
```

### Kill all port-forwarders

```bash
$ inv view.off
```

## Cheat sheet for common kubernetes development tasks

See [Cheat Sheet](cheat_sheet.md)

## sources
  
• [metrics-server](https://github.com/kubernetes-incubator/metrics-server)
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
• [istio](https://istio.io)
• [kubernetes dashboard](https://github.com/kubernetes/dashboard) (_recommend not using dashboard on remote clusters_)




### dependencies  

* invoke tasks make use of installed python packages. recommend creating a local virtualenv and installing the  
requirements.


stern
helm
python
pip
invoke
