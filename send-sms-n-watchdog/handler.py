import os
import requests
import json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from flask import jsonify


def handle(req):
    json_req = {}
    number = None
    message = None

    if req:
        try:
            json_req = json.loads(req)
        except:
            data = { "error": "Ao deserializar o JSON." }
            return jsonify(data), 200
    else:
        data = { "error": "Você não forneceu um JSON para processarmos." }
        return jsonify(data), 400
    
    number = json_req['number']
    message = json_req['message']

    if not number or not message:
        data = { "error": "Você não forneceu dados suficientes." }
        return jsonify(data), 400
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
            data = { "success": "SMS enviado com sucesso" , "status": send.status, "sid": send.sid }
            return jsonify(data), 200
        except TwilioRestException as e:
            data = { "error": "Não foi possivel mandar o sms.", "reason": str(e.msg) }
            return jsonify(data), e.status
