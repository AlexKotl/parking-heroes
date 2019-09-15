## About ##
Telegram bot about parking disturbers.

## Start project ##
`pipenv install`
`pipenv shell`
`nohup python parking.py &` or `nohup python -u parking.py &> ./../parking.log &`

To stop background process: 
`ps -ef | grep "parking.py" | grep -v grep | awk '{print $2}' | xargs kill`

For convenience run bash scripts:
```
./start.sh
./stop.sh
./restart.sh
```

### Cron setup ###
You can setup crontab to restart app if it will crash. Add cron using:
`crontab -e`

Then add this task:
`* * * * * pgrep -f parking.py || cd /home/PATH_TO_DIR/parking/; /local/bin/pipenv run python -u parking.py >> log.txt 2>&1`

### Setting up webhooks ###
Generate certificate:
```
openssl req -newkey rsa:2048 -sha256 -nodes -keyout cert.key -x509 -days 365 -out cert.pem -subj "/C=UA/ST=Kyiv/L=Kyiv/O=Home/CN=DMAIN_NAME"
```
