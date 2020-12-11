## 3. Local Kubernetes install/setup (with userspace virtualization, on macos) 

Virtualization running in Userspace will consistently outperform full virtualization, all else being equal. RAM is a potentially critical requirement. (8gb at least in order to support istio.)  

• [minikube](https://minikube.sigs.k8s.io) on [hyperkit(https://github.com/moby/hyperkit)], or  

• [docker desktop](https://www.docker.com/products/docker-desktop) with kubernetes  


### minikube

• install hyperkit and minikube  

```bash
$ brew install hyperkit
$ brew install minikube
```

• configure minikube settings and start  

```bash
$ minikube config set vm-driver hyperkit
$ minikube config set memory 12288
$ minikube config set cpus 6
$ minikube start --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.address=0.0.0.0 --extra-config=controller-manager.address=0.0.0.0
```

• Launch minikube [LoadBalancer](https://minikube.sigs.k8s.io/docs/tasks/loadbalancer/#using-minikube-tunnel) *in separate terminal window*  

```bash
$ minikube tunnel
```

See the IP used by the istio ingressgateway  
```bash
$ kubectl get svc istio-ingressgateway -n istio-system
```

You will see something like:  
```bash
NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)                                                                      AGE
istio-ingressgateway   LoadBalancer   10.96.138.70   10.96.138.70   15021:32452/TCP,80:30496/TCP,443:31765/TCP,15012:31912/TCP,15443:32267/TCP   19m
```

The EXTERNAL-IP is the address to use when setting localhost DNS values.  

### Local k8s security profile

To see how the default local development configuration compares to EKS using the CIS benchmark:  
```bash
$ inv view.bench
```
