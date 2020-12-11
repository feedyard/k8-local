## 2. Local tools and setup

### Which version of kubernetes to use for local development?  

It is recommended that you use either [minikube](https://minikube.sigs.k8s.io/docs/) or [Docker Desktop](https://www.docker.com/products/docker-desktop) as your local instance of kubernetes. The examples in this guide will use minikube.    

### local kubernetes and related packages used in this setup  

[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) • kubernetes api command-line tool  
[kubectx](https://github.com/ahmetb/kubectx) • cli to quickly swtich between local and remote k8s clusters  
[helm](https://helm.sh) • manage pod deploys  
[stern](https://github.com/wercker/stern)  • tails logs to the terminal from any number of local or remote pods  
[mkcert](https://github.com/FiloSottile/mkcert) • Automated management of certificates and CA for local https   
[skaffold](https://github.com/GoogleContainerTools/skaffold) • continuous development on local kubernetes  
[kubefwd](https://github.com/txn2/kubefwd) • develop locally with remotes services available as they would be in the remote cluster  

_code complete_  
[hadolint](https://github.com/hadolint/hadolint) • Dockerfile lint/inspection   
[kubeval](https://github.com/garethr/kubeval) • k8 yaml lint/inspection  
[git-secrets](https://github.com/awslabs/git-secrets)  

#### scripted setup

Scripts are provided that can accelerate the installation process for these tools.  

**install_mac.sh**  

Depends on the [homebrew](https://brew.sh) MacOS package manager.  

**install_windows.sh**  

**install-windows.sh**  


### Honorable mentions for additional local customization  

You may enjoy using these tools.  

[oh-my-zsh](https://ohmyz.sh)  
[kube-ps1](https://github.com/jonmosco/kube-ps1)  

<p align="center"><img width="800" alt="oh-my-zsh with kube-ps1" src="oh-my-zsh-capture.png"></p>
