helm install coreos/prometheus-operator --name prometheus-operator --namespace monitoring
helm install coreos/kube-prometheus --name kube-prometheus --set global.rbacEnable=true --namespace monitoring
sleep 4
kubectl port-forward $(kubectl get  pods --selector=app=kube-prometheus-grafana -n  monitoring --output=jsonpath="{.items..metadata.name}") -n monitoring  3000

# to port forward prometheus itself
# kubectl port-forward -n monitoring prometheus-kube-prometheus-0 9090


# for the alert monitor
# kubectl port-forward -n monitoring alertmanager-kube-prometheus-0 9093