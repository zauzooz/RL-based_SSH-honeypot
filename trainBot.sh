for i in {1..500}
do
    echo Training phase [$i]
    python3 trainBot/trainBot.py
    sudo python3 explorer/manage.py
done