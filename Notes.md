# to port forward prometheus itself
# kubectl port-forward -n monitoring prometheus-kube-prometheus-0 9090

# for the alert monitor
# kubectl port-forward -n monitoring alertmanager-kube-prometheus-0 9093

curl -v -HHost:httpbin.localhost --cacert old_httpbin.localhost.crt "https://httpbin.localhost/status/418"



