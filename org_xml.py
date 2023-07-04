import os
from lxml import etree as ET
from datetime import datetime
import calendar
import locale
import shutil

# Definir o idioma como português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

diretorio = os.getcwd()  # Obter o diretório de trabalho atual

# Percorrer todos os arquivos no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.endswith('.xml'):
        caminho_arquivo = os.path.join(diretorio, arquivo)

        # Abrir o arquivo XML
        nsNFe = {"ns": "http://www.portalfiscal.inf.br/nfe"}
        root = ET.parse(caminho_arquivo)
        node = root.findall("./ns:NFe/ns:infNFe/ns:dest/ns:CNPJ", nsNFe)
        if len(node) != 1:
            continue
        cnpj = node[0].text
        node2 = root.findall("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFe)
        if len(node2) != 1:
            continue
        data = node2[0].text
        data_sem_fuso = data[:-6]
        data_obj = datetime.strptime(data_sem_fuso, "%Y-%m-%dT%H:%M:%S")
        ano = data_obj.year
        mes = calendar.month_name[data_obj.month].capitalize()

        # Criar a estrutura de diretórios para cada separação
        pasta_cnpj = os.path.join(diretorio, cnpj)
        pasta_ano = os.path.join(pasta_cnpj, str(ano))
        pasta_mes = os.path.join(pasta_ano, str(mes))
        os.makedirs(pasta_mes, exist_ok=True)

        # Mover o arquivo XML para a pasta correspondente
        novo_caminho_arquivo = os.path.join(pasta_mes, arquivo)
        shutil.move(caminho_arquivo, novo_caminho_arquivo)
