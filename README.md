```
export DJANGO_SETTINGS_MODULE=burstout.settings
find . -path "*/migrations/*.pyc" -delete
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate --fake burstout
python manage.py migrate burstout --run-syncdb



export DJANGO_SETTINGS_MODULE=burstout.settings
find . -path "*/migrations/*.pyc" -delete
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate burstout --run-syncdb


python manage.py showmigrations
```

```
\c postgres
DROP DATABASE burstout_alpha_db;
CREATE DATABASE burstout_alpha_db;
GRANT ALL PRIVILEGES ON DATABASE  burstout_alpha_db TO raven_dev;

SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'burstout_alpha_db' ;
```

python -m grpc_tools.protoc -I burstout/protos --python_out=./burstout/pb2 --grpc_python_out=./burstout/pb2 burstout/protos/main.proto

Setup:
HA Proxy>=1.9
https://haproxy.debian.net/#?distribution=Ubuntu&release=bionic&version=1.8

```
export REDIS_HOST=127.0.0.1
export REDIS_PORT=6379
python manage.py runscript init_models
```

# Generating GRPC JS files

In the django directory

```
export OUT_DIR=./grpc_out
protoc -I=. burstout/protos/main.proto --js_out=import_style=commonjs:$OUT_DIR --grpc-web_out=import_style=commonjs,mode=grpcwebtext:$OUT_DIR
cp grpc_out/burstout/protos/* ~/Dropbox/projects/burstout/webapp/src/grpc/
```
