# trainBot

First, check current directory is `~/RL-based_SSH-honeypot`.

Run to generate dataset, run the following command:

```
sudo python3 trainBot/trainset_gen.py
```

To train the RL stupidPot, first run `SSH_server.py`. Then run:

```
python3 trainBot.py
```