### 4. Deploy supporting services to kubernetes  

The python `invoke` files in this repository provide a convenient way to install the following services.  

• [metrics-server](https://github.com/kubernetes-incubator/metrics-server)  
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)  
• [istio](https://istio.io)  
• open policy agent (pending)

_setup invoke under python3_  

```bash
$ python3 -m venv .venv  
$ source .venv/bin/activate  
$ pip install --upgrade invoke  
```

Use `invoke -l` to see a list of available shortcuts.  

### metrics collectors 

• metrics-server (0.4.1)  
• kube-state-metrics (v1.9.7)  

```bash
$ invoke deploy.ms    deploy metrics-server api  
$ invoke deploy.ksm   deploy kube-state-metrics api 
```

### istio  

_Assumes istioctl is installed locally, from the tools section_

```bash
$ deploy.istio  
$ deploy.istiotools  # installs prometheus, grafana, jeager, and kiali locally  
```

### Kubernetes Dashboard

While the kubernetes dashboard is not deployed to cloud-based clusters, it may of course be deployed locally should you prefer.  

```bash
$ deploy.dash  # v2.0.5 
```
### opa-istio-plugin (pending)  

• opa-istio-plugin (v0.14.2)  

