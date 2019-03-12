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




apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
  name: fluentd-logzio
  namespace: kube-system
  labels:
    k8s-app: fluentd-logzio
    version: v1
    kubernetes.io/cluster-service: "true"
spec:
  template:
    metadata:
      labels:
        k8s-app: fluentd-logzio
        version: v1
        kubernetes.io/cluster-service: "true"
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd
        image: logzio/logzio-k8s:1.0.0
        env:
          - name:  LOGZIO_TOKEN
            value: "your logz.io account token"
          - name:  LOGZIO_URL
            value: "your logz.io host url" ##example:https://listener.logz.io:8071  
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
    readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers