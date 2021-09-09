import http
import json

import numpy as np
import requests as req
from flask import Flask, request
from main import *

app = Flask(__name__)  # instância do aplicativo (deve sempre ficar antes da criação das páginas)


@app.route('/')  # Rota -> localhost:5000/[Rota] Obs. Sem metodo o padrão é GET (Método para leitura)
def health():
    return "OK"  # retorno do servidor, formato string (html nada mais é do que uma string com as tags para interpretação)


@app.route('/message/1', methods=['GET'])  # Método POST: o servidor vai receber uma mensagem sua
def chat():
    text = trigger()
    if text is not 0:
        print(text)
        data = {'text': str(text), "message_id": '12jb1l'}
        r = req.post('http://localhost:5005/model/parse', json.dumps(data))
        r.raise_for_status()  # raises exception when not a 2xx response
        if r.status_code != 204:
            #print(r.json())
            response = dict(r.json())
            print(response['intent']['name'])
        return text
    else:
        return http.HTTPStatus(500)


# Função de inicialização
if __name__ == '__main__':
    app.run(debug=False, host='localhost', threaded=True)  # port e host padrão

