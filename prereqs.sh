#!/bin/bash
echo "We're going to try to install the dependencies for you!"

set -e

# this quick setup only supports MacOS at the moment
[[ $(uname) == "Darwin" ]] || ( echo "installation only works on Mac" && exit 1 )

# assumes homebrew in already installed
hash brew &>/dev/null || ( echo "you need to install homebrew manually" && exit 1 )

# install all brew packages
hyperkit
minikube
[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)  
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl"
helm
skaffold 
stern

kube-ps1
kubectx   
git-secrets

### additional support for local development  

[mkcert](https://github.com/FiloSottile/mkcert) For local CA/certs

[Vault](https://www.vaultproject.io)
[Consul](https://www.hashicorp.com/products/consul)
[buildkite cli](https://github.com/buildkite/cli)


[hadolint](https://github.com/hadolint/hadolint) Dockerfile lint/inspection  
[kubeval](https://github.com/garethr/kubeval) k8 yaml lint/inspection  



hash python3 &>/dev/null || brew install python3
hash virtualenv &>/dev/null || pip install virtualenv
[[ -e .env/bin/activate ]] || virtualenv -p python3 .env
( . .env/bin/activate && pip install -r requirements.txt )
echo "python dependencies installed in a virtualenv. run \`. .env/bin/activate\` to use"
hash bundle &>/dev/null || ( echo -e "you somehow have no Ruby, so we're installing latest\n" && brew install ruby )
bundle install || ( echo "your bundle install failed, which means you're running base install Ruby or a pre 2.1 version. You'll need to resolve it yourself if you want to run the tests, but the rest will work fine." && exit 1)