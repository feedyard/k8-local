# Overview

[![Build Status](https://travis-ci.org/kubernetes/kube-state-metrics.svg?branch=master)](https://travis-ci.org/kubernetes/kube-state-metrics)  [![Go Report Card](https://goreportcard.com/badge/github.com/kubernetes/kube-state-metrics)](https://goreportcard.com/report/github.com/kubernetes/kube-state-metrics)

kube-state-metrics is a simple service that listens to the Kubernetes API
server and generates metrics about the state of the objects. (See examples in
the Metrics section below.) It is not focused on the health of the individual
Kubernetes components, but rather on the health of the various objects inside,
such as deployments, nodes and pods.

kube-state-metrics is about generating metrics from Kubernetes API objects
without modification. This ensures that features provided by kube-state-metrics
have the same grade of stability as the Kubernetes API objects themselves. In
turn, this means that kube-state-metrics in certain situations may not show the
exact same values as kubectl, as kubectl applies certain heuristics to display
comprehensible messages. kube-state-metrics exposes raw data unmodified from the
Kubernetes API, this way users have all the data they require and perform
heuristics as they see fit.

The metrics are exported on the HTTP endpoint `/metrics` on the listening port
(default 80). They are served as plaintext. They are designed to be consumed
either by Prometheus itself or by a scraper that is compatible with scraping a
Prometheus client endpoint. You can also open `/metrics` in a browser to see
the raw metrics.

## Table of Contents

- [Versioning](#versioning)
  - [Kubernetes Version](#kubernetes-version)
  - [Compatibility matrix](#compatibility-matrix)
  - [Resource group version compatibility](#resource-group-version-compatibility)
  - [Container Image](#container-image)
- [Metrics Documentation](#metrics-documentation)
- [Kube-state-metrics self metrics](#kube-state-metrics-self-metrics)
- [Resource recommendation](#resource-recommendation)
- [A note on costing](#a-note-on-costing)
- [kube-state-metrics vs. metrics-server](#kube-state-metrics-vs-metrics-server)
- [Setup](#setup)
  - [Building the Docker container](#building-the-docker-container)
- [Usage](#usage)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Limited privileges environment](#limited-privileges-environment)
  - [Development](#development)

### Versioning

#### Kubernetes Version

kube-state-metrics uses [`client-go`](https://github.com/kubernetes/client-go) to talk with
Kubernetes clusters. The supported Kubernetes cluster version is determined by `client-go`.
The compatibility matrix for client-go and Kubernetes cluster can be found
[here](https://github.com/kubernetes/client-go#compatibility-matrix).
All additional compatibility is only best effort, or happens to still/already be supported.

#### Compatibility matrix
At most, 5 kube-state-metrics and 5 [kubernetes releases](https://github.com/kubernetes/kubernetes/releases) will be recorded below.

| kube-state-metrics | client-go  | **Kubernetes 1.11** | **Kubernetes 1.12** | **Kubernetes 1.13** | **Kubernetes 1.14** |  **Kubernetes 1.15** |
|--------------------|------------|---------------------|---------------------|---------------------|---------------------|----------------------|
| **v1.3.1**         |  v6.0.0    |         ✓           |         ✓           |         -           |         -           |          -           |
| **v1.4.0**         |  v8.0.0    |         ✓           |         ✓           |         -           |         -           |          -           |
| **v1.5.0**         |  v8.0.0    |         ✓           |         ✓           |         -           |         -           |          -           |
| **v1.6.0**         |  v11.0.0   |         ✓           |         ✓           |         ✓           |         ✓           |          -           |
| **v1.7.0-rc.0**    |  v12.0.0   |         ✓           |         ✓           |         ✓           |         ✓           |          ✓           |
| **master**         |  v12.0.0   |         ✓           |         ✓           |         ✓           |         ✓           |          ✓           |
- `✓` Fully supported version range.
- `-` The Kubernetes cluster has features the client-go library can't use (additional API objects, etc).

#### Resource group version compatibility
Resources in Kubernetes can evolve, i.e., the group version for a resource may change from alpha to beta and finally GA
in different Kubernetes versions. For now, kube-state-metrics will only use the oldest API available in the latest
release.

#### Container Image

The latest container image can be found at:
* `quay.io/coreos/kube-state-metrics:v1.6.0`
* `k8s.gcr.io/kube-state-metrics:v1.6.0`

**Note**:
The recommended docker registry for kube-state-metrics is `quay.io`. kube-state-metrics on
`gcr.io` is only maintained on best effort as it requires external help from Google employees.

### Metrics Documentation

There are many more metrics we could report, but this first pass is focused on
those that could be used for actionable alerts. Please contribute PR's for
additional metrics!

> WARNING: THESE METRIC/TAG NAMES ARE UNSTABLE AND MAY CHANGE IN A FUTURE RELEASE.
> For now, the following metrics and collectors
>
> **metrics**
>	* kube_pod_container_resource_requests_nvidia_gpu_devices
>	* kube_pod_container_resource_limits_nvidia_gpu_devices
>	* kube_node_status_capacity_nvidia_gpu_cards
>	* kube_node_status_allocatable_nvidia_gpu_cards
>
>	are removed in kube-state-metrics v1.4.0.
>
> Any collectors and metrics based on alpha Kubernetes APIs are excluded from any stability guarantee,
> which may be changed at any given release.

See the [`docs`](docs) directory for more information on the exposed metrics.

### Kube-state-metrics self metrics
kube-state-metrics exposes its own general process metrics under `--telemetry-host` and `--telemetry-port` (default 81).

### Resource recommendation

Resource usage for kube-state-metrics changes with the Kubernetes objects(Pods/Nodes/Deployments/Secrets etc.) size of the cluster.
To some extent, the Kubernetes objects in a cluster are in direct proportion to the node number of the cluster.

As a general rule, you should allocate

* 200MiB memory
* 0.1 cores

For clusters of more than 100 nodes, allocate at least

* 2MiB memory per node
* 0.001 cores per node

These numbers are based on [scalability tests](https://github.com/kubernetes/kube-state-metrics/issues/124#issuecomment-318394185) at 30 pods per node.

Note that if CPU limits are set too low, kube-state-metrics' internal queues will not be able to be worked off quickly enough, resulting in increased memory consumption as the queue length grows. If you experience problems resulting from high memory allocation, try increasing the CPU limits.

### A note on costing
By default, kube-state-metrics exposes several metrics for events across your cluster. If you have a large number of frequently-updating resources on your cluster, you may find that a lot of data is ingested into these metrics. This can incur high costs on some cloud providers. Please take a moment to [configure what metrics you'd like to expose](docs/cli-arguments.md), as well as consult the documentation for your Kubernetes environment in order to avoid unexpectedly high costs.  

### kube-state-metrics vs. metrics-server

The [metrics-server](https://github.com/kubernetes-incubator/metrics-server)
is a project that has been inspired by
[Heapster](https://github.com/kubernetes-retired/heapster) and is implemented
to serve the goals of core metrics pipelines in [Kubernetes monitoring
architecture](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/monitoring_architecture.md).
It is a cluster level component which periodically scrapes metrics from all
Kubernetes nodes served by Kubelet through Summary API. The metrics are
aggregated, stored in memory and served in [Metrics API
format](https://git.k8s.io/metrics/pkg/apis/metrics/v1alpha1/types.go). The
metric-server stores the latest values only and is not responsible for
forwarding metrics to third-party destinations.

kube-state-metrics is focused on generating completely new metrics from
Kubernetes' object state (e.g. metrics based on deployments, replica sets,
etc.). It holds an entire snapshot of Kubernetes state in memory and
continuously generates new metrics based off of it. And just like the
metric-server it too is not responsibile for exporting its metrics anywhere.

Having kube-state-metrics as a separate project also enables access to these
metrics from monitoring systems such as Prometheus.

### Setup

Install this project to your `$GOPATH` using `go get`:

```
go get k8s.io/kube-state-metrics
```

#### Building the Docker container

Simply run the following command in this root folder, which will create a
self-contained, statically-linked binary and build a Docker image:
```
make container
```

### Usage

Simply build and run kube-state-metrics inside a Kubernetes pod which has a
service account token that has read-only access to the Kubernetes cluster.

#### Kubernetes Deployment

To deploy this project, you can simply run `kubectl apply -f kubernetes` and a
Kubernetes service and deployment will be created. (Note: Adjust the apiVersion of some resource if your kubernetes cluster's version is not 1.8+, check the yaml file for more information). The service already has a
`prometheus.io/scrape: 'true'` annotation and if you added the recommended
Prometheus service-endpoint scraping configuration, Prometheus will pick it up automatically and you can start using the generated
metrics right away.

**Note:** Google Kubernetes Engine (GKE) Users - GKE has strict role permissions that will prevent the kube-state-metrics roles and role bindings from being created. To work around this, you can give your GCP identity the cluster-admin role by running the following one-liner:

```
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud info --format='value(config.account)')
```

Note that your GCP identity is case sensitive but `gcloud info` as of Google Cloud SDK 221.0.0 is not. This means that if your IAM member contains capital letters, the above one-liner may not work for you. If you have 403 forbidden responses after running the above command and kubectl apply -f kubernetes, check the IAM member associated with your account at https://console.cloud.google.com/iam-admin/iam?project=PROJECT_ID. If it contains capital letters, you may need to set the --user flag in the command above to the case-sensitive role listed at https://console.cloud.google.com/iam-admin/iam?project=PROJECT_ID.

After running the above, if you see `Clusterrolebinding "cluster-admin-binding" created`, then you are able to continue with the setup of this service.

#### Limited privileges environment

If you want to run kube-state-metrics in an environment where you don't have cluster-reader role, you can:

- create a serviceaccount
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-state-metrics
  namespace: your-namespace-where-kube-state-metrics-will-deployed
```

- give it `view` privileges on specific namespaces (using roleBinding) (*note: you can add this roleBinding to all the NS you want your serviceaccount to access*)
```yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: RoleBinding
metadata:
  name: kube-state-metrics
  namespace: project1
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: view
subjects:
  - kind: ServiceAccount
    name: kube-state-metrics
    namespace: your-namespace-where-kube-state-metrics-will-deployed
```

- then specify a set of namespaces (using the `--namespace` option) and a set of kubernetes objects (using the `--collectors`) that your serviceaccount has access to in the `kube-state-metrics` deployment configuration

```yaml
spec:
  template:
    spec:
      containers:
        - args:
          - '--collectors=pods'
          - '--namespace=project1'
```

For the full list of arguments available, see the documentation in [docs/cli-arguments.md](./docs/cli-arguments.md)

#### Development

When developing, test a metric dump against your local Kubernetes cluster by
running:

> Users can override the apiserver address in KUBE-CONFIG file with `--apiserver` command line.

	go install
	kube-state-metrics --port=8080 --telemetry-port=8081 --kubeconfig=<KUBE-CONFIG> --apiserver=<APISERVER>

Then curl the metrics endpoint

	curl localhost:8080/metrics

To run the e2e tests locally see the documentation in [tests/README.md](./tests/README.md).
