#!/bin/bash

python provider_a/server.py &
python provider_b/server.py &
python airflow/server.py &


while :
do
    read -rsn1 input
    if [ "$input" = "Q" ]; then

        pkill -f provider_a/server.py 
        echo "killed proider a"
        pkill -f provider_b/server.py 
        echo "killed proider b"
        pkill -f airflow/server.py 
        echo "killed airlow"

        break
    fi   
done
