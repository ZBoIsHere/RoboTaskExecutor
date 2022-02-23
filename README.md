# RoboTaskExecutor

todo
* 解析出错如何解决
* udp出错如何解决

#!/bin/bash

#define key value
declare -A roboName2URI
roboName2URI=(
["ysc-robo"]="192.168.1.102"
["arm64-robo"]="192.168.0.75"
["x20robot"]="192.168.1.102"
)

# deploy navi task to some robo

touch navi-deploy.yaml
touch navi-svc.yaml
touch navi-vs.yaml
touch navi-gw.yaml
cat /dev/null > navi-deploy.yaml
cat /dev/null > navi-svc.yaml
cat /dev/null > navi-vs.yaml
cat /dev/null > navi-gw.yaml

echo "apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: navi-vs
spec:
  gateways:
    - navi-gw
  hosts:
    - '*'
  http:" > navi-vs.yaml


# create navi deploy
#for ROBONAME in `kubectl get nodes | grep agent | awk '{print $1}'`
for ROBONAME in ysc-robo arm64-robo
do
    ROSMASTERURI="localhost"
    if [ -n "${roboName2URI[$ROBONAME]}" ];then
        ROSMASTERURI=${roboName2URI[$ROBONAME]}
    fi
    echo "apiVersion: apps/v1
kind: Deployment
metadata:
  name: navi-${ROBONAME}-deploy
  labels:
    app: navi-${ROBONAME}-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: navi-${ROBONAME}-deploy
  template:
    metadata:
      labels:
        app: navi-${ROBONAME}-deploy
    spec:
      nodeName: ${ROBONAME}
      hostNetwork: true
      containers:
      - env:
        - name: ROS_MASTER_URI
          value: http://${ROSMASTERURI}:11311
        name: navi-${ROBONAME}-deploy
        image: navi_task:v21121521
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 8080
---" >> navi-deploy.yaml

    echo "apiVersion: v1
kind: Service
metadata:
  name: navi-${ROBONAME}-svc
spec:
  selector:
    app: navi-${ROBONAME}-deploy
  ports:
    - name: http-0
      port: 12345
      protocol: TCP
      targetPort: 8080
---" >> navi-svc.yaml

    echo "    - match:
      - uri:
          prefix: /${ROBONAME}
      route:
      - destination:
          host: navi-${ROBONAME}-svc
          port:
            number: 12345" >> navi-vs.yaml
done

echo "apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: navi-gw
spec:
  selector:
    kubeedge: navi-gw
  servers:
    - hosts:
        - '*'
      port:
        name: http-0
        number: 23334
        protocol: HTTP" > navi-gw.yaml

kubectl apply -f navi-deploy.yaml
kubectl apply -f navi-svc.yaml
kubectl apply -f navi-vs.yaml
kubectl apply -f navi-gw.yaml
