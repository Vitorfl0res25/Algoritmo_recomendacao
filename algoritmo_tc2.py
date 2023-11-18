import firebase_admin
from firebase_admin import credentials, firestore
import random

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred)

id_usuario = ""

db = firestore.client()

colecao_usuarios = db.collection("usuarios")

doc_ref = colecao_usuarios.document(id_usuario)

doc_snapshot = doc_ref.get()

dados_usuario = doc_snapshot.to_dict()
ambiental = dados_usuario.get("Ambiental")
educacional = dados_usuario.get("Educacional")
saude = dados_usuario.get("Saude")
social = dados_usuario.get("Social")

valores = {
    'Ambiental': ambiental,
    'Educacional': educacional,
    'Saude': saude,
    'Social': social
}

valores_ordenados = sorted(valores.items(), key=lambda item: item[1], reverse=True)

if valores_ordenados[1][1] == valores_ordenados[2][1]:
    escolhido = random.choice([valores_ordenados[1], valores_ordenados[2]])
else:
    escolhido = valores_ordenados[1]

#print(f'Os dois maiores valores são: {valores_ordenados[0][1]} (pertence a {valores_ordenados[0][0]}) e {escolhido[1]} (pertence a {escolhido[0]})')
#db.document(caminho_documento).update({"Pmaior": valores_ordenados[0][0]})
#db.document(caminho_documento).update({"Smaior": escolhido[0]})

caminho_documento = "usuarios/{id_usuario}/projeto_recomendacao/recomendacao"
colecao = db.collection("projetos")

primeiro_id = "" 
segundo_id = ""
terceiro_id = ""
quarto_id = ""

categorias_procuradas = [valores_ordenados[0][0], escolhido[0]]

for categoria in categorias_procuradas:
    consulta = colecao.where("categoria", '==', categoria).limit(2).stream()

    #print(f'Resultados para categoria "{categoria}":')
    for i, documento in enumerate(consulta):
        #print(f'Documento ID: {documento.id}')

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

#print(f'ID 1: {primeiro_id}')
#print(f'ID 2: {segundo_id}')
#print(f'ID 3: {terceiro_id}')
#print(f'ID 4: {quarto_id}')

db.document(caminho_documento).update({
    'primeiro_id': primeiro_id,
    'segundo_id': segundo_id,
    'terceiro_id': terceiro_id,
    'quarto_id': quarto_id
})
