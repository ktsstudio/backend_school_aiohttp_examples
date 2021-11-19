export PYTHONPATH=.
python3 validation/server.py &
sleep 1
server_process="$(jobs -p)"
python3 validation/client.py
kill "$server_process"
