
### Conformance testing

#### kube-bench

```bash
$ inv test.kubebench
```

Runs a kube-bench job and tests for FAIL output.  Uses https://github.com/feedyard/feedyard-kube-bench, see for details on customizing benchmark checks.  





#### Using [kind](https://github.com/kubernetes-sigs/kind)  

$ kind create cluster --image kindest/node:v1.15.3 --config kind-config.yaml  
$ export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"  
$ kind delete cluster  
$ unset KUBECONFIG  