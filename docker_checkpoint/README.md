# Docker checkpoint

Self-contained Docker practice environment using official Docker Hub images. No private image repository is required.

## Prerequisites

Start Docker Desktop with the Linux engine, then run these commands from this directory:

```powershell
Set-Location C:\Users\melki\OneDrive\Desktop\learn_git\docker_checkpoint
```

## Docker basics

```powershell
docker pull nginx:latest
docker run -d --name checkpoint-nginx -p 8080:80 nginx:latest
docker ps
docker exec checkpoint-nginx ls -la /usr/share/nginx/html
docker exec -it checkpoint-nginx sh
ls -la /usr/share/nginx/html
exit
docker restart checkpoint-nginx
docker port checkpoint-nginx
docker inspect --format '{{.HostConfig.PortBindings}}' checkpoint-nginx
```

Open `http://localhost:8080` to view Nginx. The restart keeps the container's port configuration. Remove the exercise resources:

```powershell
docker rm -f checkpoint-nginx
docker rmi nginx:latest
```

## Dockerfile and image layers

The root `Dockerfile` uses `python:3.12-slim`, copies `app.py` and `requirements.txt`, installs dependencies, and runs `python app.py` by default.

```powershell
docker build -t my-python-app:v1 .
docker run -d --name checkpoint-python -p 5000:5000 my-python-app:v1
Invoke-RestMethod http://localhost:5000/health
docker history my-python-app:v1
docker rm -f checkpoint-python
docker rmi my-python-app:v1
```

## MySQL volume persistence

Create a named volume and start MySQL. Wait for the logs to say it is ready:

```powershell
docker volume create checkpoint-mysql-data
docker run -d --name checkpoint-mysql `
  -e MYSQL_ROOT_PASSWORD=local-root-password `
  -e MYSQL_DATABASE=checkpoint `
  -v checkpoint-mysql-data:/var/lib/mysql `
  mysql:8.4
docker logs -f checkpoint-mysql
```

Press `Ctrl+C`, then create and query data in MySQL:

```powershell
docker exec -it checkpoint-mysql mysql -uroot -plocal-root-password checkpoint
CREATE TABLE notes (id INT PRIMARY KEY AUTO_INCREMENT, body VARCHAR(255) NOT NULL);
INSERT INTO notes (body) VALUES ('volume data survives container removal');
SELECT * FROM notes;
exit
```

Stop and remove the container, start another with the same volume, and confirm the row remains:

```powershell
docker stop checkpoint-mysql
docker rm checkpoint-mysql
docker run -d --name checkpoint-mysql-2 `
  -e MYSQL_ROOT_PASSWORD=local-root-password `
  -e MYSQL_DATABASE=checkpoint `
  -v checkpoint-mysql-data:/var/lib/mysql `
  mysql:8.4
docker exec -it checkpoint-mysql-2 mysql -uroot -plocal-root-password checkpoint -e "SELECT * FROM notes;"
docker rm -f checkpoint-mysql-2
docker volume rm checkpoint-mysql-data
```

Copy `.env.example` to `.env` for local variables if desired. Never commit real passwords:

```powershell
Copy-Item .env.example .env
```

## User-defined networking

```powershell
docker network create internal-net
docker run -d --name network-web --network internal-net nginx:latest
docker run --rm --network internal-net curlimages/curl:latest curl -s http://network-web
docker run --rm --network internal-net alpine:latest ping -c 3 network-web
docker rm -f network-web
docker network rm internal-net
```

The curl and ping clients resolve the other container by its name on `internal-net`.

## Docker Compose

`docker-compose.yml` defines a Flask backend and an Nginx reverse proxy on shared network `app-net`. Only Nginx is exposed to the host:

```powershell
docker compose up -d --build
docker compose ps
docker compose logs backend nginx
Invoke-RestMethod http://localhost:8080/health
```

Browse to `http://localhost:8080` to verify the proxy. Shut down the stack and remove its local image:

```powershell
docker compose down
docker rmi my-python-app:v1
```

## Reproduction and image sources

Copy or clone this directory, start Docker Desktop's Linux engine, and run `docker compose up -d --build`. The app is available at `http://localhost:8080`.

Images come from Docker Hub: `nginx:latest`, `python:3.12-slim`, `mysql:8.4`, `alpine:latest`, and `curlimages/curl:latest`. `my-python-app:v1` is built locally from `Dockerfile`; there is no remote custom image repository.