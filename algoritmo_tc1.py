import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import spacy
nlp = spacy.load('pt_core_news_sm')

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred)

db = firestore.client()

id_usuario = "PYpIqscF0pStYuuU4Y5jwWs62Bb2"
id_projeto = "LxRDgSXI8gFIQ9smNazp"

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

tempo_gasto_total = ((contagem_palavras_nome * 225)+(contagem_palavras_descricao * 225)+(contagem_palavras_cadastro * 225)+(contagem_palavras_categoria * 225)+(contagem_palavras_dt * 225))/1000
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



