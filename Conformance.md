# Conformance testing locally  

## kube-bench  


##### accepted for local  

-master config accepted for local
[FAIL] 1.1.21 Ensure that the --kubelet-certificate-authority argument is set as appropriate (Scored)  
[FAIL] 1.1.36 Ensure that the admission control plugin EventRateLimit is set (Scored)  
[FAIL] 1.1.37b Ensure that the AdvancedAuditing argument is not set to false (Scored)  
[FAIL] 1.3.6 Ensure that the RotateKubeletServerCertificate argument is set to true (Scored)  
[FAIL] 1.4.12 Ensure that the etcd data directory ownership is set to etcd:etcd (Scored)  
[FAIL] 1.1.24 Ensure that the admission control plugin PodSecurityPolicy is set (Scored)  
[FAIL] 1.1.15 Ensure that the --audit-log-path argument is set as appropriate (Scored)  

-node config accepted for local  
[FAIL] 2.1.4 Ensure that the --read-only-port argument is set to 0 (Scored)  
[FAIL] 2.1.6 Ensure that the --protect-kernel-defaults argument is set to true (Scored)  
[FAIL] 2.1.8 Ensure that the --hostname-override argument is not set (Scored)  
[FAIL] 2.1.9 Ensure that the --event-qps argument is set to 0 (Scored)  
[FAIL] 2.1.10 Ensure that the --tls-cert-file and --tls-private-key-file arguments are set as appropriate (Scored)  
[FAIL] 2.1.13 Ensure that the RotateKubeletServerCertificate argument is set to true (Scored)  
[FAIL] 2.2.3 Ensure that the kubelet service file permissions are set to 644 or more restrictive (Scored)  
[FAIL] 2.2.4 Ensure that the kubelet service file ownership is set to root:root (Scored)  
[FAIL] 2.2.5 Ensure that the proxy kubeconfig file permissions are set to 644 or more restrictive (Scored)  
[FAIL] 2.2.6 Ensure that the proxy kubeconfig file ownership is set to root:root (Scored)  


## sonobuoy  


### example conformance testing  

VERSION=0.16.1 OS=darwin && \
   curl -L "https://github.com/vmware-tanzu/sonobuoy/releases/download/v${VERSION}/sonobuoy_${VERSION}_${OS}_amd64.tar.gz" --output $HOME/bin/sonobuoy.tar.gz && \
   tar -xzf $HOME/bin/sonobuoy.tar.gz -C $HOME/bin && \
   chmod +x $HOME/bin/sonobuoy && \
   rm $HOME/bin/sonobuoy.tar.gz
