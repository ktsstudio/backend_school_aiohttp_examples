export PYTHONPATH=.
python3 request_response/server.py &
sleep 1
server_process="$(jobs -p)"
python3 request_response/client.py
kill "$server_process"
