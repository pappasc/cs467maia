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

### Run on EC2 
1. ssh to EC2 instance: ```ssh -i "cs467-maia-key-pair.pem" ec2-user@ec2-54-203-128-106.us-west-2.compute.amazonaws.com
``` 
2. Login to docker if needed ```docker login```
3. Pull down image ```docker pull kvavlen/cs467maia-backend:latest```
4. Run on port 80 ```docker run -v interpreter_api:/app -d -p 80:8080 kvavlen/cs467maia-backend:latest```

## Notes
Data on Amazon AWS is stored in volume at: 
```/var/lib/docker/volumes/interpreter_api/_data```


## References
1. https://www.ybrikman.com/writing/2015/11/11/running-docker-aws-ground-up/ re: setup ec2 and install docker 
2. https://docs.docker.com/storage/volumes/#start-a-service-with-volumes re: use of volumes