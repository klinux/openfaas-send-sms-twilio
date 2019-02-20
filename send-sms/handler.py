import os
import requests
import json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def handle(req):
    json_req = {}
    number = None
    message = None

    if req:
        try:
            json_req = json.loads(req)
        except:
            data = { "error": "Ao deserializar o JSON.", "status": 400 }
            return json.dumps(data)
    else:
        data = { "error": "Você não forneceu um JSON para processarmos.", "status": 400 }
        return json.dumps(data)
    
    number = json_req['number']
    message = json_req['message']

    if not number or not message:
        data = { "error": "Você não forneceu dados suficientes.", "status": 400 }
        return json.dumps(data)
    else:
        account_sid = os.environ['ACCOUND_SID']
        auth_token = os.environ['AUTH_TOKEN']
        from_phone = os.environ['FROM_PHONE']
    
        client = Client(account_sid, auth_token)
    
        try:
            send = client.messages.create(
                to = "+55" + str(number), 
                from_ = from_phone,
                body = message
            )
            data = { "success": "Sua mensagem foi enviada com sucesso.", "sid": send.sid, "status": 200 }
            return json.dumps(data)
        except TwilioRestException as e:
            data = { "error": "Não foi possivel mandar o sms.", "reason": str(e.msg), "status": e.status }
            return json.dumps(data)
        finally:
            data = { "fatal": "Não conseguimos processar sua requisição.", "status": 500 }
            return json.dumps(data)
