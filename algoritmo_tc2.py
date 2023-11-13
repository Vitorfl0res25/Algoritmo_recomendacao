import firebase_admin
from firebase_admin import credentials, firestore
import random

cred = credentials.Certificate("banco-tijuba-firebase-adminsdk-3khg4-33686be01d.json")
firebase_admin.initialize_app(cred)

#id_usuario = 

caminho_documento = "usuarios/PYpIqscF0pStYuuU4Y5jwWs62Bb2/projeto_recomendacao/recomendacoes "

db = firestore.client()

colecao_usuarios = db.collection("usuarios")

doc_ref = colecao_usuarios.document("PYpIqscF0pStYuuU4Y5jwWs62Bb2")#fornecido pelo app

doc_snapshot = doc_ref.get()

dados_usuario = doc_snapshot.to_dict()
ambiental = dados_usuario.get("Ambiental")
educacional = dados_usuario.get("Educacional")
saude = dados_usuario.get("Saude")
social = dados_usuario.get("Social")

valores = {
    'ambiental': ambiental,
    'educacional': educacional,
    'saude': saude,
    'social': social
}

valores_ordenados = sorted(valores.items(), key=lambda item: item[1], reverse=True)

if valores_ordenados[1][1] == valores_ordenados[2][1]:
    escolhido = random.choice([valores_ordenados[1], valores_ordenados[2]])
else:
    escolhido = valores_ordenados[1]

#print(f'Os dois maiores valores são: {valores_ordenados[0][1]} (pertence a {valores_ordenados[0][0]}) e {escolhido[1]} (pertence a {escolhido[0]})')
#db.document(caminho_documento).update({"Pmaior": valores_ordenados[0][0]})
#db.document(caminho_documento).update({"Smaior": escolhido[0]})

primeiro_id = None
segundo_id = None
terceiro_id = None
quarto_id = None

recomendacao = db.collection("projetos")

categorias_procuradas = [valores_ordenados[0][0], escolhido[0]]

for categoria in categorias_procuradas:
    consulta = colecao.where("nome_do_campo_categoria", '==', categoria).limit(2).stream()

    for i, documento in enumerate(consulta):
        if categoria == valores_ordenados[0][0]:
            if i == 0:
                primeiro_id = documento.id
            elif i == 1:
                segundo_id = documento.id
        elif categoria == escolhido[0]:
            if i == 0:
                terceiro_id = documento.id
            elif i == 1:
                quarto_id = documento.id


db.document(caminho_documento).update(primeiro_id)
db.document(caminho_documento).update(segundo_id)
db.document(caminho_documento).update(terceiro_id)
db.document(caminho_documento).update(quarto_id)