export PYTHONPATH=.
python3 app/common_application.py &
server_process="$(jobs -p)"
python3 app/client.py
kill "$server_process"
