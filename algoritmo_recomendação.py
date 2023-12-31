import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import spacy
nlp = spacy.load('pt_core_news_sm')

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred)

db = firestore.client()

id_usuario = ""
id_projeto = ""

doc_ref_time = firestore.client().document(f"usuarios/{id_usuario}/interacao_projetos/{id_projeto}")

doc_time = doc_ref_time.get()
doc_time = doc_time.to_dict()

caminho_usuario = f"usuarios/{id_usuario}" 
caminho_projeto = f"projetos/{id_projeto}"

colecao_usuarios = db.collection("usuarios")
colecao_projetos = db.collection("projetos")

doc_ref = colecao_usuarios.document(id_usuario)
doc_ref_projetos = colecao_projetos.document(id_projeto)


doc_snapshot = doc_ref.get()
doc_projetos = doc_ref_projetos.get()
dados_usuario = doc_snapshot.to_dict()
dados_projetos = doc_projetos.to_dict()


cadastradoPor = dados_projetos.get("cadastradorPor")
categoria = dados_projetos.get("categoria")
dt_criacao = str(dados_projetos.get("dt_criacao"))
nome_projeto = dados_projetos.get("nome_projeto")
descricao = dados_projetos.get("descricao")


cadastradoPor_nlp = nlp(cadastradoPor)
contagem_palavras_cadastro = 0
for token in cadastradoPor_nlp:
  if not token.is_punct and not token.is_space:
    contagem_palavras_cadastro += 1

#print(f"cadastro: {contagem_palavras_cadastro}")

categoria_nlp = nlp(categoria)
contagem_palavras_categoria = 0
for token in categoria_nlp:
  if not token.is_punct and not token.is_space:
    contagem_palavras_categoria += 1

#print(f"categoria: {contagem_palavras_categoria}")

dt_criacao_nlp = nlp(dt_criacao)
contagem_palavras_dt = 0
for token in dt_criacao_nlp:
  if not token.is_punct and not token.is_space:
    contagem_palavras_dt += 1

#print(f"dt: {contagem_palavras_dt}")

nome_projeto_nlp = nlp(nome_projeto)
contagem_palavras_nome = 0
for token in nome_projeto_nlp:
  if not token.is_punct and not token.is_space:
    contagem_palavras_nome += 1

#print(f"nome: {contagem_palavras_nome}")

descricao_nlp = nlp(descricao)
contagem_palavras_descricao = 0
for token in descricao_nlp:
  if not token.is_punct and not token.is_space:
    contagem_palavras_descricao += 1

#print(f"descricao: {contagem_palavras_descricao}")

tempo_gasto_total = (contagem_palavras_nome + contagem_palavras_descricao + contagem_palavras_cadastro + contagem_palavras_categoria + contagem_palavras_dt)/250
tempo_gasto_total = int(tempo_gasto_total)
#print(f"tempo de leitura da pagina: {tempo#_gasto_total}")

dt_entrada = doc_time.get("dt_entrada")
entrada = dt_entrada.strftime('%H:%M:%S')

dt_saida = doc_time.get("dt_saida")
saida = dt_saida.strftime('%H:%M:%S')

diferenca_segundos = (dt_saida - dt_entrada).total_seconds()

#print(f"primeiro: {entrada}, segundo: {saida}, diferenca: {diferenca_segundos}")

janela_superior = tempo_gasto_total + 2
janela_inferior = tempo_gasto_total - 2

if diferenca_segundos > janela_superior:
    recomendacao = "recomendar"
elif diferenca_segundos < janela_inferior:
    recomendacao = "não recomendar"
else:
    recomendacao = "neutro"

#print(f"A recomendação final é: {recomendacao}")

db = firestore.client()

colecao_usuarios = db.collection("usuarios")

doc_ref = colecao_usuarios.document(f"{id_usuario}")
doc_snapshot = doc_ref.get()
dados_usuario = doc_snapshot.to_dict()

ambiental = dados_usuario.get("Ambiental")
educacional = dados_usuario.get("Educacional")
saude = dados_usuario.get("Saude")
social = dados_usuario.get("Social")

valor_categoria = dados_usuario.get(categoria)

#print("Ambiental", ambiental)
#print("educacional", educacional)
#print("saude", saude)
#print("social", social)

total_indiv = 21
total_global = ambiental + educacional + saude + social
#print(total_global)

if recomendacao == "recomendar":
  if categoria == "Ambiental":
    if ambiental == total_indiv:
      db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
    elif total_global < 44 and ambiental != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
    elif total_global == 44 and ambiental != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
      if educacional > 1:
        db.document(caminho_usuario).update({"Educacional": firestore.Increment(-1)})
      elif saude > 1:
        db.document(caminho_usuario).update({"Saude": firestore.Increment(-1)})
      elif social > 1:
        db.document(caminho_usuario).update({"social": firestore.Increment(-1)})

  if categoria == "Educacional":
    if educacional == total_indiv:
      db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
    elif total_global < 44 and educacional != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
    elif total_global == 44 and educacional != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
      if ambiental > 1:
        db.document(caminho_usuario).update({"Ambiental": firestore.Increment(-1)})
      elif saude > 1:
        db.document(caminho_usuario).update({"Saude": firestore.Increment(-1)})
      elif social > 1:
        db.document(caminho_usuario).update({"social": firestore.Increment(-1)})

  if categoria == "Saude":
    if saude == total_indiv:
      db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
    elif total_global < 44 and saude != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
    elif total_global == 44 and saude != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
      if ambiental > 1:
        db.document(caminho_usuario).update({"Ambiental": firestore.Increment(-1)})
      elif educacional > 1:
        db.document(caminho_usuario).update({"Educacional": firestore.Increment(-1)})
      elif social > 1:
        db.document(caminho_usuario).update({"social": firestore.Increment(-1)})

  if categoria == "Social":
    if social == total_indiv:
      db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
    elif total_global < 44 and social != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
    elif total_global == 44 and social != 21:
      db.document(caminho_usuario).update({categoria: firestore.Increment(1)})
      if ambiental > 1:
        db.document(caminho_usuario).update({"Ambiental": firestore.Increment(-1)})
      elif educacional > 1:
        db.document(caminho_usuario).update({"Educacional": firestore.Increment(-1)})
      elif saude > 1:
        db.document(caminho_usuario).update({"Saude": firestore.Increment(-1)})

elif recomendacao == "não recomendar":
  if categoria == "Ambiental" and ambiental > 1:
    db.document(caminho_usuario).update({categoria: firestore.Increment(-1)})
  elif categoria == "Educacional" and educacional > 1:
    db.document(caminho_usuario).update({categoria: firestore.Increment(-1)})
  elif categoria == "Saude" and saude > 1:
    db.document(caminho_usuario).update({categoria: firestore.Increment(-1)})
  elif categoria == "Social" and social > 1:
    db.document(caminho_usuario).update({categoria: firestore.Increment(-1)})

elif recomendacao == "neutro":
  if categoria == "Ambiental":
    db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
  elif categoria == "Educacional":
    db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
  elif categoria == "Saude":
    db.document(caminho_usuario).update({categoria: firestore.Increment(0)})
  elif categoria == "Social":
    db.document(caminho_usuario).update({categoria: firestore.Increment(0)})



#---------------------------------------------------------------------------------------------------------#

if (ambiental > 10 and saude > 10) or \
    (ambiental > 10 and social > 10) or \
    (ambiental > 10 and educacional > 10) or \
    (saude > 10 and social > 10) or \
    (saude > 10 and educacional > 10) or \
    (social > 10 and educacional > 10):

    doc_ref = colecao_usuarios.document("{id_usuario}")

    doc_snapshot = doc_ref.get()

    dados_usuario = doc_snapshot.to_dict()
    ambiental = dados_usuario.get("Ambiental")
    educacional = dados_usuario.get("Educacional")
    saude = dados_usuario.get("Saude")
    social = dados_usuario.get("Social")

    valores = {
        'Ambiental': ambiental,
        'Educação': educacional,
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

