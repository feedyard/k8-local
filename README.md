# feedyard/k8-local

_review the dependencies section below for laptop setup_

Starting with a fresh install of docker-for-mac and kubernetes  
(setting memory available to docker resources to 8gb recommended)  

1. Edit kubernetes manifest for AdmissionController settings
```bash
$ screen  ~/Library/Containers/com.docker.docker/Data/vms/0/tty
$ vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

edit the following line: (_add text in bold_)  

--enable-admission-plugins=Initializers,NodeRestriction,__MutatingAdmissionWebhook,ValidatingAdmissionWebhook__

Restart Docker for Mac  

2. Get latest versions of services

```bash
$ invoke update
```


3. Deploy metrics server and dashboard  

```bash
$ invoke init
```

Deploys:  
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
• [eventrouter](https://github.com/heptiolabs/eventrouter)
• [kubernetes dashboard](https://github.com/kubernetes/dashboard) (_recommend not using dashboard on remote clusters_)



4. Install istio (see section below on how deploy templates were generates)


Generate kubernetes deployment  
```bash
$ invoke generateistio
```

Deploy istio
```bash
invoke istio
```

### dependencies  

stern
helm
python
pip
invoke
