## dashboard

Dashboard token has been copied to clipboard  

1. run `kubectl proxy`  
2. From your local browser:  http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/  
3. Select Token option and paste (Ctrl-V) token into the field   

Alternate: now or any time after closing dashboard and ending proxy, you can re-access the dashboard by: 

```bash
$ invoke dash
```

