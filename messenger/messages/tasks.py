import json
import requests
from application.celery import app


@app.task(time_limit=6)
def publish_message(new_message, channel='chat'):
    command = {
        'method': 'publish',
        'params': {
            'channel': channel,
            'data': f'{new_message}'
        }
    }

    api_key = '7ad95d37-15a3-4d04-8795-38267a2f10b5'
    data = json.dumps(command)
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    requests.post('http://localhost:8000/api', data=data, headers=headers)