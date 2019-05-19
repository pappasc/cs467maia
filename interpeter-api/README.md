# interpeter-api

## Main Contributor
Natasha Kvavle

## Purpose
This API addresses the fact that we cannot run LaTeX on the Standard Google AppEngine platform. This additional API will be called from employee-recognition-api and will be hosted separately on an Amazon AWS EC2 instance (via Docker container). Originally I was going to host via the OSU engineering server, but VPN requirements to access the API were too limiting. 

## Instructions
### Build
```sudo docker build -t interpeter-api:latest .```

### Run 
```sudo docker -p 8080:8080 run interpeter-api:latest```