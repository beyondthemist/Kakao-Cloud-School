#!bin/sh

# update
sudo apt -y update
sleep 3
sudo apt -y upgrade
sleep 3

# kubectl
if which kubectl >/dev/null; then
    echo "kubectl is already installed. Skip installation"
    sleep 1
else
    sudo curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.10/2023-01-30/bin/linux/amd64/kubectl
    sleep 5
    sudo chmod +x ./kubectl
    sleep 5
    sudo mv ./kubectl /usr/local/sbin
    sleep 5
    kubectl version --short --client
    sleep 1
fi

# Kubernetes bash completion
if dpkg -s bash-completion >/dev/null 2>&1; then
    echo "bash-completion is already installed. Skip Installation."
else
    sudo apt install -y bash-completion
fi
kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
sleep 5
sudo sh -c 'echo "source /usr/share/bash-completion/bash_completion" >> /etc/bash.bashrc'
sleep 2
sudo sh -c 'echo "alias k=kubectl" >> /etc/bash.bashrc'
sleep 2
sudo sh -c 'echo "complete -o default -F __start_kubectl k" >> /etc/bash.bashrc'
sleep 2
sudo sh -c 'echo "if [ -s ~/.bashrc ]; then" >> /etc/profile'
sleep 2
sudo sh -c 'echo "    source ~/.bashrc;" >> /etc/profile'
sleep 2
sudo sh -c 'echo "fi" >> /etc/profile'
sleep 2

# AWS CLI 2
if which aws >/dev/null; then
    echo "AWS CLI is already installed. Skip Installation."
else
    sudo apt -y install unzip
    sleep 5
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    sleep 5
    unzip awscliv2.zip
    sleep 5
    sudo ./aws/install
    sleep 5
    aws --version
    sleep 1
fi

# AWS configuration
REGION="ap-northeast-2"
sleep 1
aws configure set aws_access_key_id AKIA2MTTUWBTLXHWR6Y3
sleep 1
aws configure set aws_secret_access_key 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
sleep 1
aws configure set region ${REGION}
sleep 1

# update kubernetes context
aws eks update-kubeconfig --region ap-northeast-2 --name terraform-eks
sleep 2

# velero
sudo apt -y install wget
sleep 5
wget https://github.com/vmware-tanzu/velero/releases/download/v1.10.2/velero-v1.10.2-linux-amd64.tar.gz
sleep 5
tar -xvf velero-v1.10.2-linux-amd64.tar.gz
sleep 5
sudo mv velero-v1.10.2-linux-amd64/velero /usr/local/sbin
sleep 5
BUCKET="source-seoul-s3-bucket"
sleep 1
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.6.0 \
    --bucket ${BUCKET} \
    --backup-location-config region=${REGION} \
    --snapshot-location-config region=${REGION} \
    --secret-file ${HOME}/.aws/credentials
sleep 5
velero schedule create backup-everyday --schedule "0 4 * * *"
sleep 5

# Install docker
sudo curl -ssL https://get.docker.com/ | bash
sleep 5

# ecr login
ACCOUNT=236747833953
sleep 1
REGION=ap-northeast-2
sleep 1
SECRET_NAME=${REGION}-ecr-secret
sleep 1
EMAIL=mega@coffee.com
sleep 1
TOKEN=`aws ecr --region=$REGION get-authorization-token --output text --query authorizationData[].authorizationToken | base64 -d | cut -d: -f2`
sleep 1
kubectl create secret docker-registry $SECRET_NAME \
    --docker-server=https://${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com \
    --docker-username=AWS \
    --docker-password="${TOKEN}" \
    --docker-email="${EMAIL}"
sleep 5
aws ecr get-login-password --region ${REGION} | sudo docker login --username AWS --password-stdin ${ACCOUNT}.dkr.ecr.ap-northeast-2.amazonaws.com
sleep 5
