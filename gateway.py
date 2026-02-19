from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# --- SIMULAÇÃO DOS MICROSERVIÇOS ---

# Microserviço 1: Catálogo
@app.route('/servico-catalogo/<id>')
def get_catalogo(id):
    # Simulando um banco de dados
    return jsonify({"id": id, "nome": "Minecraft", "categoria": "Sandbox"})

# Microserviço 2: Preços
@app.route('/servico-precos/<id>')
def get_precos(id):
    return jsonify({"id": id, "preco": 99.90, "moeda": "BRL"})

# --- O API GATEWAY ---

@app.route('/produto/<id>')
def api_gateway(id):
    # O Gateway faz a 'Composição de API' (Fan-out)
    # 1. Chama o serviço de catálogo
    res_cat = requests.get(f'http://127.0.0.1:5000/servico-catalogo/{id}')
    dados_cat = res_cat.json()
    
    # 2. Chama o serviço de preços
    res_pre = requests.get(f'http://127.0.0.1:5000/servico-precos/{id}')
    dados_pre = res_pre.json()
    
    # 3. Agrega os dados em uma resposta única para o cliente
    resposta_final = {
        "produto": dados_cat['nome'],
        "categoria": dados_cat['categoria'],
        "valor": dados_pre['preco'],
        "local_original": "API Gateway"
    }
    
    return jsonify(resposta_final)

if __name__ == '__main__':
    CORS(app) # Isso permite que o HTML acesse a API
    app.run(port=5000)