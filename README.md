# feedyard/k8-local


## dashboard

```bash

kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
```

1. Copy token from Data section
2. run `kubectl proxy`
3. Access dashbaord:  http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
4. Use the provided Token
