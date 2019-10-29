export PYTHONPATH=$PWD/burstout/pb2:$PYTHONPATH
export GRPC_VERBOSITY=WARNING
export GRPC_TRACE=all
sudo systemctl restart haproxy.service
python manage.py grpcserver --autoreload --max_workers=20
