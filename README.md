# feedyard/k8-local

_basic setup for local kubernetes development_  

Starting with a fresh install of docker-for-mac and kubernetes  

## 1. Local Kubernetes  

### docker-for-mac  
_(setting memory available to docker resources at 8gb)_   

Edit kubernetes manifest for AdmissionController settings. _(if you are on a Mac just go with docker-for-mac. )_  

```bash
$ screen  ~/Library/Containers/com.docker.docker/Data/vms/0/tty  
$ vi /etc/kubernetes/manifests/kube-apiserver.yaml  
```

edit the following line: (_add text in bold_)  

--enable-admission-plugins=Initializers,NodeRestriction,__MutatingAdmissionWebhook,ValidatingAdmissionWebhook__  

Restart Docker for Mac   

## 2. Installable services  

### local kubernetes related packages used in this setup (recommend homebrew to manage)  

kubectl  
helm  
stern  

### To use a set of pre-defined actions:  

The invoke tasks file can help with rapid setup of this local k8 instance.  

```bash
$ python3 -m venv .venv  
$ source .venv/bin/activate  
$ pip install --upgrade -r requirements.txt  
$ invoke -l  
```

### Install metrics  

* metrics-server (0.3.5)  
* kube-state-metrics (v1.8.0-rc.1)  

```bash
$ deploy.ksm   deploy kube-state-metrics api  
$ deploy.ms    deploy metrics-server api  
```
### Install kubernetes Web UI (dashboard)

Kubectl port-forward and access on localhost.  

```bash
$ inv deploy.db
```

### Install istio  

Get specified version (See tasks/download_versions.py), render istio-demo-auth version of install, and deploy  

```bash
$ inv get.versions
$ inv render.istio
$ deploy.istio
```

#### View dashboards

The kubernetes and istio dashboards provide observability into logs and metrics until you have local integration  
with the primary systems.  

Port forwards the kubernetes dashboard and open the login screen. Token will be in the clipboard. Select token login  
options and cmd-v + return to access.  

```bash
$ inv view.db
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

#### Using [kind](https://github.com/kubernetes-sigs/kind)  

$ kind create cluster --image kindest/node:v1.15.3 --config kind-config.yaml  
$ export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"  
$ kind delete cluster  
$ unset KUBECONFIG  

#### see the following for more setup and local development capabilities  

[stern](https://github.com/wercker/stern)  
[kube-ps1](https://github.com/jonmosco/kube-ps1) prompt tool  
[kubefwd](https://github.com/txn2/kubefwd)  
[hadolint](https://github.com/hadolint/hadolint) Dockerfile lint/inspection  
[kubeval](https://github.com/garethr/kubeval) k8 yaml lint/inspection  
[sonabouy](https://github.com/heptio/sonobuoy)  
[kind](https://github.com/kubernetes-sigs/kind)  


## sources

• [metrics-server](https://github.com/kubernetes-incubator/metrics-server)  
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)  
• [istio](https://istio.io)  
• [kubernetes dashboard](https://github.com/kubernetes/dashboard) (_recommend not using dashboard on remote clusters_)  
