export PYTHONPATH=.
python3 app/custom_application.py &
sleep 1
server_process="$(jobs -p)"
python3 app/client.py
kill "$server_process"
