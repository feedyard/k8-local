
### Additional 

#### Using [kind](https://github.com/kubernetes-sigs/kind)  

$ kind create cluster --image kindest/node:v1.15.3 --config kind-config.yaml  
$ export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"  
$ kind delete cluster  
$ unset KUBECONFIG  
