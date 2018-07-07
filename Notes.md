# using example output from ingress deployment, the dashboard is accessible at http://localhost:31432/dashboard/   trailing slash necessary
# kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/alternative/kubernetes-dashboard.yaml
kubectl create -f dashboard/

# deploy heapster-influx-grafana default(deprecated) autoscaling support
kubectl create -f heapster/










example helm based dashboard deploy

#!/usr/bin/env bash
helm install stable/kubernetes-dashboard --name console
sleep 4
export POD_NAME=$(kubectl get pods -n default -l "app=kubernetes-dashboard,release=console" -o jsonpath="{.items[0].metadata.name}")
echo https://127.0.0.1:8443/
kubectl -n default port-forward $POD_NAME 8443:8443 &





helm install coreos/prometheus-operator --name prometheus-operator --namespace monitoring
helm install coreos/kube-prometheus --name kube-prometheus --set global.rbacEnable=true --namespace monitoring
sleep 4
kubectl port-forward $(kubectl get  pods --selector=app=kube-prometheus-grafana -n  monitoring --output=jsonpath="{.items..metadata.name}") -n monitoring  3000

# to port forward prometheus itself
# kubectl port-forward -n monitoring prometheus-kube-prometheus-0 9090


# for the alert monitor
# kubectl port-forward -n monitoring alertmanager-kube-prometheus-0 9093