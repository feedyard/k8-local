# cheatsheet.md

## how port-forwards are configured for various services

### istio  

#### prometheus

```bash
$ kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=prometheus -o jsonpath='{.items[0].metadata.name}') 9090:9090 &
```

http://localhost:9090/graph  

#### grafana  

```bash
$ kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=grafana -o jsonpath='{.items[0].metadata.name}') 3000:3000 &
```

http://localhost:3000/dashboard/db/istio-mesh-dashboard  

#### Jaeger

```bash
$ kubectl port-forward -n istio-system $(kubectl get pod -n istio-system -l app=jaeger -o jsonpath='{.items[0].metadata.name}') 16686:16686  &
```

http://localhost:16686  

#### kiali

```bash
$ kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=kiali -o jsonpath='{.items[0].metadata.name}') 20001:20001 &
```

http://localhost:20001/kiali/console  

