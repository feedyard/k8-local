### 4. Deploy supporting services to kubernetes  

The python `invoke` files in this repository provide a convenient way to install the following services.  

• [metrics-server](https://github.com/kubernetes-incubator/metrics-server)  
• [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)  
• [istio](https://istio.io)  
• open policy agent

_setup invoke under python3_  

```bash
$ python3 -m venv .venv  
$ source .venv/bin/activate  
$ pip install --upgrade -r requirements.txt  
```

Use `invoke -l` to see a list of available shortcuts.  

### metrics collectors 

• metrics-server (0.3.7)  
• kube-state-metrics (v1.9.7)  

```bash
$ invoke deploy.ksm   deploy kube-state-metrics api  
$ invoke deploy.ms    deploy metrics-server api  
```

### istio  

• Install the istioctl cli (v1.7.0)  

```bash
$ mv istio/bin/istioctl /usr/local/bin/istioctl
```
_or add the local folder to your $PATH_ 

• deploy  

```bash
$ deploy.istio     # default profile with telemetry.enabled=true
```


### opa-istio-plugin  

• opa-istio-plugin (v0.14.2)  

