# Ingress Metrics

| Metric name| Metric type | Labels/tags | Status |
| ---------- | ----------- | ----------- | ----------- |
| kube_ingress_info | Gauge | `ingress`=&lt;ingress-name&gt; <br> `namespace`=&lt;ingress-namespace&gt; | STABLE |
| kube_ingress_labels | Gauge | `ingress`=&lt;ingress-name&gt; <br> `namespace`=&lt;ingress-namespace&gt; <br> `label_INGRESS_LABEL`=&lt;INGRESS_LABEL&gt; | STABLE |
| kube_ingress_created  | Gauge | `ingress`=&lt;ingress-name&gt; <br> `namespace`=&lt;ingress-namespace&gt; | STABLE |
| kube_ingress_metadata_resource_version  | Gauge | `ingress`=&lt;ingress-name&gt; <br> `namespace`=&lt;ingress-namespace&gt; <br> `resource_version`=&lt;ingress-resource-version&gt; | STABLE |
| kube_ingress_path | Gauge | `ingress`=&lt;ingress-name&gt; <br> `namespace`=&lt;ingress-namespace&gt; <br> `host`=&lt;ingress-host&gt; <br> `path`=&lt;ingress-path&gt; <br> `service_name`=&lt;service name for the path&gt; <br> `service_port`=&lt;service port for hte path&gt; | STABLE |
| kube_ingress_annotations | Gauge | `annotation_INGRESS_ANNOTATION`=&lt;INGRESS_ANNOTATION&gt; <br> `ingress`=&lt;ingress-name&gt; <br> `namespace`=&lt;ingress-namespace&gt; | EXPERIMENTAL |
