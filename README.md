# 사용한 기술
<img src="images/infra.png" width="50%"/>  

### **[Terraform](https://www.terraform.io/)**  
AWS의 resource들을 편하고 일관성 있게 provisioning하기 위해 사용했다.

### **[Velero](https://velero.io/)**  
EKS 클러스터를 백업하기 위해 사용했다.
etcdctl을 사용하지 않는 이유는 아래에 기술되어 있다.
<br>

# Velero Vs. etcdctl
- Amazon EKS에서는 사용자가 etcd에 직접 접근할 수 없으므로 etcdctl은 사용하기가 어렵다.
- Kubernetes resource 뿐만 아니라 disk snapshot을 생성함으로써 PV 상태도 저장한다.
- etcdctl 자체 기능만으로는 scheduled back up이 불가능하다.
<br>

### 구성도
<img src="images/arch.png" width="80%" />

Terraform으로 EKS 클러스터, RDS, Bastion, S3 bucket 등을 provision하고 Velero가 EKS 클러스터를 S3 bucket으로 백업한다.
