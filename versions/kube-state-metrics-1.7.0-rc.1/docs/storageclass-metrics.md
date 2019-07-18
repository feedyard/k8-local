# StorageClass Metrics

| Metric name| Metric type | Labels/tags | Status |
| ---------- | ----------- | ----------- | ----------- |
| kube_storageclass_info | Gauge | `storageclass`=&lt;storageclass-name&gt; <br> `provisioner`=&lt;storageclass-provisioner&gt; <br> `reclaimPolicy`=&lt;storageclass-reclaimPolicy&gt; <br> `volumeBindingMode`=&lt;storageclass-volumeBindingMode&gt; | STABLE |
| kube_storageclass_labels | Gauge | `storageclass`=&lt;storageclass-name&gt; <br> `label_STORAGECLASS_LABEL`=&lt;STORAGECLASS_LABEL&gt; | STABLE |
| kube_storageclass_created  | Gauge | `storageclass`=&lt;storageclass-name&gt; | STABLE |
