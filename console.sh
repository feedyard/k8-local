helm install stable/kubernetes-dashboard --name console
sleep 4
export POD_NAME=$(kubectl get pods -n default -l "app=kubernetes-dashboard,release=console" -o jsonpath="{.items[0].metadata.name}")
echo https://127.0.0.1:8443/
kubectl -n default port-forward $POD_NAME 8443:8443 &