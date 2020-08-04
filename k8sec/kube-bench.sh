#!/usr/bin/env bash
kubectl apply -f k8sec/kube-bench/kube-bench-job.yaml && sleep 10

kubectl logs -f job.batch/kube-bench --all-containers=true | grep "\[FAIL" > temp.results
if [[ $(cat temp.results) ]]; then
  echo "kube-bench conformance results error:"
  cat temp.results
  exit 1
fi
rm temp.results

kubectl delete -f k8sec/kube-bench/kube-bench-job.yaml
