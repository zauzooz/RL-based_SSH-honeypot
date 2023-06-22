for i in {1..1000}
do
    echo Training phase [$i]
    python3 trainBot/trainBot.py
    sudo python3 explorer/manage.py
done