# Docker

[TOC]

## Docker 명령어


```dockerfile
docker [OPTIONS] COMMAND
```

### version

```dockerfile
docker version [OPTIONS]
```

- 도커의 버전을 확인

### run

```dockerfile
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

- 컨테이너의 실행

#### run - options

`—rm` : 프로세스 종료시 컨테이너 삭제

`—it` : 키보드 입력

`-d` : 프로세스를 백그라운드로 동작

`-p` : 포트포워딩 (ex. docker run -p 1234:6379 -p 5678:6006 IMAGE)

`--name` : ID의 이름을 지정

`--link` : 

### ps

```dockerfile
docker ps [OPTIONS]
```

- 컨테이너의 목록을 나열

#### ps - options

`-a, --all` : 모든 컨테이너를 보여줌 (기본적으로는 동작 중인 컨테이너만 보여줌)

### stop

```dockerfile
docker stop [OPTIONS] CONTAINER [CONTAINER...]
```

- 하나 또는 그 이상의 동작 중인 컨테이너를 정지

### rm

```dockerfile
docker rm [OPTIONS] CONTAINER [CONTAINER...]
```

- 하나 또는 하나 이상의 컨테이너를 삭제

### images

```dockerfile
docker images [OPTIONS] [REPOSITORY[:TAG]]
```

- 이미지들을 나열

### pull

```dockerfile
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
```

### rmi

```dockerfile
docker rmi [OPTIONS] IMAGE [IMAGE...]
```

### logs

```dockerfile
docker logs [OPTIONS] CONTAINER
```

### exec

```dockerfile
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

## Docker-compose 명령어

```dockerfile
docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]
```

### up

```dockerfile
docker-compose up [options] [--scale SERVICE=NUM...] [SERVICE...]
```

### bundle

```dockerfile
docker-compose bundle [options]
```

#### bundle - options

`install` : compose 파일을 가지고 DAB(분산 어플리케이션 번들)을 생성

