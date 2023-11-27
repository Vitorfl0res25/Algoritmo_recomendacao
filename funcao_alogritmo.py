import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import spacy
import random

def processar_dados(id_usuario, id_projeto):
    nlp = spacy.load('pt_core_news_sm')

    cred = credentials.Certificate("banco-tijuba-firebase-adminsdk-3khg4-33686be01d.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    doc_ref_time = db.document(f"usuarios/{id_usuario}/interacao_projetos/{id_projeto}")
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
    contagem_palavras_cadastro = contar_palavras(cadastradoPor_nlp)

    categoria_nlp = nlp(categoria)
    contagem_palavras_categoria = contar_palavras(categoria_nlp)

    dt_criacao_nlp = nlp(dt_criacao)
    contagem_palavras_dt = contar_palavras(dt_criacao_nlp)

    nome_projeto_nlp = nlp(nome_projeto)
    contagem_palavras_nome = contar_palavras(nome_projeto_nlp)

    descricao_nlp = nlp(descricao)
    contagem_palavras_descricao = contar_palavras(descricao_nlp)

    tempo_gasto_total = (contagem_palavras_nome + contagem_palavras_descricao + contagem_palavras_cadastro +
                         contagem_palavras_categoria + contagem_palavras_dt) / 238
    tempo_gasto_total = int(tempo_gasto_total)

    dt_entrada = doc_time.get("dt_entrada")
    entrada = dt_entrada.strftime('%H:%M:%S')

    dt_saida = doc_time.get("dt_saida")
    saida = dt_saida.strftime('%H:%M:%S')

    diferenca_segundos = (dt_saida - dt_entrada).total_seconds()

    janela_superior = tempo_gasto_total + 2
    janela_inferior = tempo_gasto_total - 2

    recomendacao = determinar_recomendacao(diferenca_segundos, janela_superior, janela_inferior)

    atualizar_categorias(id_usuario, categoria, recomendacao, dados_usuario)

    recomendar_projetos(id_usuario, caminho_usuario, categoria, recomendacao, db)


def contar_palavras(texto_nlp):
    contagem_palavras = 0
    for token in texto_nlp:
        if not token.is_punct and not token.is_space:
            contagem_palavras += 1
    return contagem_palavras


def determinar_recomendacao(diferenca_segundos, janela_superior, janela_inferior):
    if diferenca_segundos > janela_superior:
        return "recomendar"
    elif diferenca_segundos < janela_inferior:
        return "não recomendar"
    else:
        return "neutro"


def atualizar_categorias(id_usuario, categoria, recomendacao, dados_usuario):
    db = firestore.client()
    caminho_usuario = f"usuarios/{id_usuario}"

    ambiental = dados_usuario.get("Ambiental")
    educacional = dados_usuario.get("Educacional")
    saude = dados_usuario.get("Saude")
    social = dados_usuario.get("Social")

    total_indiv = 21
    total_global = ambiental + educacional + saude + social

    if recomendacao == "recomendar":
        if categoria == "Ambiental":
            # Implemente as atualizações para a categoria Ambiental
            pass
        elif categoria == "Educacional":
            # Implemente as atualizações para a categoria Educacional
            pass
        elif categoria == "Saude":
            # Implemente as atualizações para a categoria Saude
            pass
        elif categoria == "Social":
            # Implemente as atualizações para a categoria Social
            pass
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
        db.document(caminho_usuario).update({categoria: firestore.Increment(0)})


def recomendar_projetos(id_usuario, caminho_usuario, categoria, recomendacao, db):
    if (ambiental > 10 and saude > 10) or \
            (ambiental > 10 and social > 10) or \
            (ambiental > 10 and educacional > 10) or \
            (saude > 10 and social > 10) or \
            (saude > 10 and educacional > 10) or \
            (social > 10 and educacional > 10):
        caminho_documento = f"{caminho_usuario}/projeto_recomendacao/recomendacao"

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

        primeiro_id, segundo_id, terceiro_id, quarto_id = obter_ids_projetos(categoria, valores_ordenados,
                                                                             escolhido, db)

        db.document(caminho_documento).update({
            'primeiro_id': primeiro_id,
            'segundo_id': segundo_id,
            'terceiro_id': terceiro_id,
            'quarto_id': quarto_id
        })


def obter_ids_projetos(categoria, valores_ordenados, escolhido, db):
    caminho_documento = "usuarios/{id_usuario}/projeto_recomendacao/recomendacao"
    colecao = db.collection("projetos")

    primeiro_id = ""
    segundo_id = ""
    terceiro_id = ""
    quarto_id = ""

    categorias_procuradas = [valores_ordenados[0][0], escolhido[0]]

    for categoria in categorias_procuradas:
        consulta = colecao.where("categoria", '==', categoria).limit(2).stream()

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

    return primeiro_id, segundo_id, terceiro_id, quarto_id


# Exemplo de uso da função
id_usuario = "PYpIqscF0pStYuuU4Y5jwWs62Bb2"
id_projeto = "VbWNTXc81Bba8L7DZCzw"
processar_dados(id_usuario, id_projeto)
