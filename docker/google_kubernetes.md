# How to launch multiple komodod miners on Google Kubernetes cluster
## Install SDK
```
cd /var/tmp
wget -c https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-200.0.0-linux-x86_64.tar.gz
tar -xvzf google-cloud-sdk-200.0.0-linux-x86_64.tar.gz
cd google-cloud-sdk
./install.sh
```

```
gcloud init
```

Choose region - e.g. in our case europe-west3-a (frankfurt).

```
gcloud auth list
gcloud config list
```

## Install Kubernetes client tool
```
gcloud components install kubectl
```

Make sure Docker CE and git is installed on our PC/laptop.

```
export PROJECT_ID="$(gcloud config get-value project -q)"
```
The value of PROJECT_ID will be used to tag the container image for pushing it to your private Container Registry.

## Build the image and upload to GCR
Use this repo: https://github.com/patchkez/kmdplatform
Build the image:
```
docker-compose -f docker-compose.yml -f docker-compose-SCALE.yml build KMD
```

Check if image works:
```
docker run -it gcr.io/calsync-1457
````

Push Image to registry

```
gcloud docker -- push gcr.io/${PROJECT_ID}/kmdplatform_komodod_dev:latest
```

## Create cluster
```
gcloud container clusters create kmdscalingtest3  --machine-type=n1-standard-1  --num-nodes=3 --password=secretpass  --username=mysuername
kubeconfig entry generated for kmdscalingtest3.
NAME             LOCATION        MASTER_VERSION  MASTER_IP       MACHINE_TYPE   NODE_VERSION  NUM_NODES  STATUS
kmdscalingtest3  europe-west3-a  1.8.8-gke.0     35.198.184.88  n1-standard-1  1.8.8-gke.0   3          RUNNING
```

Without auth:
```
gcloud container clusters create kmdscalingtest3  --machine-type=n1-standard-1  --num-nodes=3
gcloud container clusters create kmdscalingtest1  --machine-type=n1-highcpu-4  --num-nodes=5
```

Delete cluster:
```
gcloud container clusters delete kmdscalingtest3
```


## Download kompose -docker-compose converter
```
curl -L https://github.com/kubernetes/kompose/releases/download/v1.1.0/kompose-linux-amd64 -o kompose
```

Deploy into k8:
```
kompose -f docker-compose-assets-test3.yml up
INFO We are going to create Kubernetes Deployments, Services and PersistentVolumeClaims for your Dockerized application. If you need different kind of resources, use the 'kompose convert' and 'kubectl create -f' commands instead. 

 INFO Deploying application in "default" namespace
 INFO Successfully created Service: txscl18b
 INFO Successfully created Service: txscl1ca
 INFO Successfully created Service: txscl1e9
 INFO Successfully created Deployment: txscl18b
 INFO Successfully created Deployment: txscl1ca
 INFO Successfully created Deployment: txscl1e9

 Your application has been deployed to Kubernetes. You can run 'kubectl get deployment,svc,pods,pvc' for details.
 ```

Get details about deployment,services and pods:
```
$ kubectl get deployment
NAME       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
txscl18b   1         1         1            0           43s
txscl1ca   1         1         1            0           43s
txscl1e9   1         1         1            0           43s
```

```
$ kubectl get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)               AGE
kubernetes   ClusterIP   10.39.240.1     <none>        443/TCP               8m
txscl18b     ClusterIP   10.39.243.12    <none>        51737/TCP,51736/TCP   51s
txscl1ca     ClusterIP   10.39.248.212   <none>        55054/TCP,55053/TCP   51s
txscl1e9     ClusterIP   10.39.250.182   <none>        35414/TCP,35413/TCP   51s
```

```
$ kubectl get pods
NAME                        READY     STATUS              RESTARTS   AGE
txscl18b-7bbc55578d-s7r26   0/1       ContainerCreating   0          1m
txscl1ca-6c48d644cb-l7wzk   1/1       Running             0          1m
txscl1e9-b895cdb46-6xpm5    1/1       Running             0          1m
```

```
$ kubectl get pods
NAME                        READY     STATUS    RESTARTS   AGE
txscl18b-7bbc55578d-s7r26   1/1       Running   0          1m
txscl1ca-6c48d644cb-l7wzk   1/1       Running   0          1m
txscl1e9-b895cdb46-6xpm5    1/1       Running   0          1m
```


Connect to container:
```
kubectl exec -it txscl0ce-66d5f88b6c-4l557 -- bash
```

Show CPU/RAM usage for nodes:
```
kubectl top node
```


## Change project
```
gcloud config set project komodoscaling
```


## Extend cluster
List pools of nodes:
```
tmp gcloud container node-pools list --cluster=kmdscalingtest1
NAME          MACHINE_TYPE  DISK_SIZE_GB  NODE_VERSION
default-pool  n1-highcpu-4  100           1.8.8-gke.0
```

##Create new pool of nodes:
```
gcloud container node-pools create high-cpu-8-cores --cluster=kmdscalingtest1 --machine-type=n1-standard-8 --num-nodes=13

gcloud container node-pools create high-cpu-8-cores --cluster=kmdscalingtest1 --machine-type=n1-standard-8 --num-nodes=125

gcloud container node-pools create high-cpu-4-cores --cluster=kmdscalingtest1 --machine-type=n1-standard-4 --num-nodes=1
```

## Delete pool:
```
gcloud container node-pools delete high-cpu-8-cores --cluster=kmdscalingtest1
```

# Convert docker-compose file via kompose and start via kubectl
```
kompose convert' and 'kubectl create -f convertedk8n.yaml
```
