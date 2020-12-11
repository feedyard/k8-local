## 7. Local development patterns  

### Create local namespace

Team namespaces in the cloud clusters follow the naming convention of "team name"-"pipeline environment name". For example, if you have dev, qa, and prod environments in your pipeline, and your team name is blue, then you would have the following namespaces in the nonprod or prod clusters:  

blue-dev  
blue-qa  
blue-prod  

You will also need a local namespace that matches the above pattern but identifies as the local cluster to enable a local deployment. Typical this will be `local` and continuing with the above example this means you need a local namespace of:  

blue-local  

The `devns` invoke task will create a local namespace and apply the correct istio annotations. 
```bash
$ inv deploy.devns "blue-local"  
```

### Guestbook ui development example  

This example uses the Google Guestbook sample app to demonstrate using a local CA, and the skaffold tool.  

**create local certificate**

Depends on `mkcert`  
```bash
$ inv deploy.localdomain "local.guestbook.com"
```

**add localhost entry for istio ingressgateway**
add guestbook.localhost to hostfile. Example uses `hostess` on MacOs  
```bash
$ hostess local.guestbook.com <isito-ingressgateway IP>
```
