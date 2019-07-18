/*
Copyright 2019 The Kubernetes Authors All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package store

import (
	"testing"

	v1 "k8s.io/api/core/v1"
	storagev1 "k8s.io/api/storage/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/kube-state-metrics/pkg/metric"
)

func TestStorageClassStore(t *testing.T) {
	// Fixed metadata on type and help text. We prepend this to every expected
	// output so we only have to modify a single place when doing adjustments.

	startTime := 1501569018
	metav1StartTime := metav1.Unix(int64(startTime), 0)
	reclaimPolicy := v1.PersistentVolumeReclaimDelete
	volumeBindingMode := storagev1.VolumeBindingImmediate

	const metadata = `
			# HELP kube_storageclass_labels Kubernetes labels converted to Prometheus labels.
			# TYPE kube_storageclass_labels gauge
			# HELP kube_storageclass_info Information about storageclass.
			# TYPE kube_storageclass_info gauge
			# HELP kube_storageclass_created Unix creation timestamp
			# TYPE kube_storageclass_created gauge
	`
	cases := []generateMetricsTestCase{
		{
			Obj: &storagev1.StorageClass{
				ObjectMeta: metav1.ObjectMeta{
					Name: "test_storageclass-info",
				},
				Provisioner:       "kubernetes.io/rbd",
				ReclaimPolicy:     &reclaimPolicy,
				VolumeBindingMode: &volumeBindingMode,
			},
			Want: `
					kube_storageclass_info{storageclass="test_storageclass-info",provisioner="kubernetes.io/rbd",reclaimPolicy="Delete",volumeBindingMode="Immediate"} 1
				`,
			MetricNames: []string{
				"kube_storageclass_info",
			},
		},
		{
			Obj: &storagev1.StorageClass{
				ObjectMeta: metav1.ObjectMeta{
					Name:              "test_kube_storageclass_created",
					CreationTimestamp: metav1StartTime,
				},
				Provisioner:       "kubernetes.io/rbd",
				ReclaimPolicy:     &reclaimPolicy,
				VolumeBindingMode: &volumeBindingMode,
			},
			Want: `
					kube_storageclass_created{storageclass="test_kube_storageclass_created"} 1.501569018e+09
				`,
			MetricNames: []string{
				"kube_storageclass_created",
			},
		},
		{
			Obj: &storagev1.StorageClass{
				ObjectMeta: metav1.ObjectMeta{
					Name: "test_storageclass-labels",
					Labels: map[string]string{
						"foo": "bar",
					},
				},
				Provisioner:       "kubernetes.io/rbd",
				ReclaimPolicy:     &reclaimPolicy,
				VolumeBindingMode: &volumeBindingMode,
			},
			Want: `
					kube_storageclass_labels{storageclass="test_storageclass-labels",label_foo="bar"} 1
				`,
			MetricNames: []string{
				"kube_storageclass_labels",
			},
		},
	}
	for i, c := range cases {
		c.Func = metric.ComposeMetricGenFuncs(storageClassMetricFamilies)
		if err := c.run(); err != nil {
			t.Errorf("unexpected collecting result in %vth run:\n%s", i, err)
		}
	}
}
