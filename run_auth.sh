export PYTHONPATH=.
python3 auth/server.py &
server_process="$(jobs -p)"
python3 auth/client.py
kill $server_process