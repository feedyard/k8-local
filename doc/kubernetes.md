## 1. Local Kubernetes install/setup (with userspace virtualization, on macos) 

Virtualization running in Userspace will consistently outperform full virtualization, all else being equal. RAM is a potentially critical requirement. (8gb at least in order to support istio.)  

• [minikube](https://minikube.sigs.k8s.io) on [hyperkit(https://github.com/moby/hyperkit)], or  

• [docker-for-mac edge](https://docs.docker.com/docker-for-mac/edge-release-notes/) with kubernetes  


### minikube

• install hyperkit and minikube  

```bash
$ brew install hyperkit
$ brew install minikube
```

• configure minikube settings and start  

```
$ minikube config set vm-driver hyperkit
$ minikube config set memory 12288
$ minikube config set cpus 6
$ minikube start --extra-config=kubelet.authentication-token-webhook=true
```

• Launch minikube LoadBalancer *In separate terminal window*  

```
$ minikube [tunnel](https://minikube.sigs.k8s.io/docs/tasks/loadbalancer/#using-minikube-tunnel)
```

### docker-for-mac  

• Install Docker-for-Mac edge  
• Edit kubernetes manifest AdmissionController settings  

```bash
$ screen  ~/Library/Containers/com.docker.docker/Data/vms/0/tty  
$ vi /etc/kubernetes/manifests/kube-apiserver.yaml  
```

until Kubernetes version >= 1.16, edit the following line: (_add text in bold_)  
```
--enable-admission-plugins=Initializers,NodeRestriction,__MutatingAdmissionWebhook,ValidatingAdmissionWebhook__  
```

• Restart Docker-for-Mac   

