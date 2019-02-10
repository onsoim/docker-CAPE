# Progress

## 1. Install Cuckoo manually

![image-20190210105553771](README.assets/image-20190210105553771.png)

![image-20190210105658714](README.assets/image-20190210105658714.png)

[*] Problem: network connection between virtual machine and host machine

## 2. Study about Docker

![image-20190210103824432](README.assets/image-20190210103824432.png)

- I just studied about how to use docker and make docker image.

## 3. Install Cuckoo by using Docker ( It takes less than 5 min!! WoW )

![image-20190210100946129](README.assets/image-20190210100946129.png)

![image-20190210101358019](README.assets/image-20190210101358019.png)

[*] Problem: When I submit a file to Cuckoo, it stucks in pending.

## 4. Build docker images for CAPE

![image-20190210103732824](README.assets/image-20190210103732824.png)

[*] Problem: It's not working properly in my ubuntu.

# Moving Forward

## 4-1. Edit CAPE source code (It's little out of date, so there are some points that I have to edit it.)

First of all, I'm not sure it is for python2 or python3.

![image-20190210111650213](README.assets/image-20190210111650213.png)

In case of django>=1.7, it requires python3.

![image-20190210110703852](README.assets/image-20190210110703852.png)

![image-20190210110855785](README.assets/image-20190210110855785.png)

In python3 `configParser` renamed to `configparser`. In my guess, dJango needs python3 and others need python2.

So they need to evince specific version of python and devide the requirements into python2 and python3.

[*] Working on:

- find apt dependencies
- devide the requirements into python2 and python3.

## 4-2. Make docker Image and Upload to docker hub

## 4-3. Make docker-compose, Dockerfile etc.