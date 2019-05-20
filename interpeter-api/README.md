# interpeter-api

## Main Contributor
Natasha Kvavle

## Purpose
This API addresses the fact that we cannot run LaTeX on the Standard Google AppEngine platform. This additional API will be called from employee-recognition-api and will be hosted separately on an Amazon AWS EC2 instance (via Docker container). Originally I was going to host via the OSU engineering server, but VPN requirements to access the API were too limiting. 

## Instructions
### Build
```sudo docker build -t cs467maia-backend:latest .```

### Push to Docker Hub (private repo)
```docker push kvavlen/cs467maia-backend:latest```

### Run
1. ssh to ECS instance: ```ssh -i "cs467-maia-key-pair.pem" ec2-user@ec2-54-203-128-106.us-west-2.compute.amazonaws.com
``` 
2. Pull down image ```sudo docker pull kvavlen/cs467maia-backend:latest```
2. Run on port 80 ```sudo docker -p 8080:80 run kvavlen/cs467maia-backend:latest```

