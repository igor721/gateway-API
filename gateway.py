from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# --- SIMULAÇÃO DOS MICROSERVIÇOS (Lendo de arquivos JSON) ---

@app.route('/servico-catalogo/<id>')
def get_catalogo(id):
    with open('catalogo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    # Busca o ID no JSON ou retorna erro se não existir
    jogo = dados.get(id)
    return jsonify(jogo) if jogo else (jsonify({"erro": "Jogo não encontrado"}), 404)

@app.route('/servico-precos/<id>')
def get_precos(id):
    with open('precos.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    preco = dados.get(id)
    return jsonify(preco) if preco else (jsonify({"erro": "Preço não encontrado"}), 404)

# --- O API GATEWAY (Mantém a mesma lógica de agregação) ---

@app.route('/produto/<id>')
def api_gateway(id):
    try:
        # O Gateway continua chamando as URLs, mas agora elas retornam dados dos arquivos
        res_cat = requests.get(f'http://127.0.0.1:5000/servico-catalogo/{id}')
        if res_cat.status_code != 200:
            return jsonify({"erro": "Erro no serviço de catálogo"}), 404
        
        res_pre = requests.get(f'http://127.0.0.1:5000/servico-precos/{id}')
        if res_pre.status_code != 200:
            return jsonify({"erro": "Erro no serviço de preços"}), 404

        dados_cat = res_cat.json()
        dados_pre = res_pre.json()
        
        # Agregação final
        resposta_final = {
            "id_original": id,
            "produto": dados_cat['nome'],
            "categoria": dados_cat['categoria'],
            "valor": dados_pre['preco'],
            "em_estoque": dados_pre['estoque'],
            "msg": "Dados agregados de múltiplos microserviços via JSON"
        }
        return jsonify(resposta_final)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)