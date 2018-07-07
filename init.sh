#!/usr/bin/env bash
#
# setup core local kubernetes development services

kubectl create -f metrics-server/
kubectl apply -f heapster/

# create ingress service based on traefik
kubectl apply -f ingress/traefik-rbac.yaml
kubectl apply -f ingress/traefik-deployment.yaml
kubectl describe svc -n kube-system traefik-ingress-service

kubectl apply -f dashboard/

kubectl apply -f namespaces.yaml

cat <<EOF

Note port references from result of traefik describe:  e.g.,

Traefik admin:         http://localhost:32527/dashboard/
Kubernetes dashboard:  http://localhost:31432/console
EOF


# example output from describe
# todo: gathering all these startup capabililities into an html page with appropriate localhost links
# Name:                     traefik-ingress-service
# Namespace:                kube-system
# Labels:                   <none>
# Annotations:              kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"traefik-ingress-service","namespace":"kube-system"},"spec":{"ports":[{"name":"...
# Selector:                 k8s-app=traefik-ingress-lb
# Type:                     NodePort
# IP:                       10.110.158.175
# LoadBalancer Ingress:     localhost
# Port:                     web  80/TCP
# TargetPort:               80/TCP
# NodePort:                 web  31432/TCP
# Endpoints:                10.1.0.5:80
# Port:                     admin  8080/TCP
# TargetPort:               8080/TCP
# NodePort:                 admin  32527/TCP
# Endpoints:                10.1.0.5:8080
# Session Affinity:         None
# External Traffic Policy:  Cluster
# Events:                   <none>
#
# access traefik admin gui with admin port from above, e.g., http://localhost:32527
# services will be published from the web port above. e.g., kubernetes dashboard is at http://localhost:31432/console
