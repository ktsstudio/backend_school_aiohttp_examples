export PYTHONPATH=.
python3 routes/server.py &
sleep 1
server_process="$(jobs -p)"
python3 routes/client.py
kill "$server_process"
