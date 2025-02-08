import pandas as pd
import requests
import os
# from langchain_community import LangChain


url_base = "https://www.bcb.gov.br/api/servico/sitebcb/atascopom/ultimas"


def baixar_pdf(url_pdf, nome_arquivo):

    resposta = requests.get(url_pdf)
    
    if resposta.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(resposta.content)
        print(f"Arquivo {nome_arquivo} baixado com sucesso.")
    else:
        print(f"Falha ao baixar o arquivo {nome_arquivo}. Código de status: {resposta.status_code}")


def obter_atas(quantidade):
    url = f"{url_base}?quantidade={quantidade}&filtro=Id%20ne%20%27250%27"
    
    resposta = requests.get(url)
    
    if resposta.status_code == 200:

        dados = resposta.json()
        print(dados)  
        
        atas = []
        for ata in dados['conteudo']:  
            ata_info = {
                'data': ata.get('DataReferencia'),  
                'link_pdf': ata.get('Url'),  
                'id': ata.get('Titulo')  
            }
            atas.append(ata_info)
        
        df = pd.DataFrame(atas)

        # baixando PDFs
        pasta_destino = "atas_pdf"
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        for index, row in df.iterrows():
            nome_arquivo = os.path.join(pasta_destino, f"{row['id']}.pdf")
            url_pdf = f"https://www.bcb.gov.br{row['link_pdf']}"
            baixar_pdf(url_pdf, nome_arquivo)

        return df
    else:
        print(f"Erro ao acessar a API. Código de status: {resposta.status_code}")
        return None


quantidade = 2
df_atas = obter_atas(quantidade)

if df_atas is not None:
    print(df_atas)
