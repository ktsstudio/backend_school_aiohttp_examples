export PYTHONPATH=.
python3 middlewares/server.py &
sleep 1
server_process="$(jobs -p)"
python3 middlewares/client.py
kill "$server_process"
