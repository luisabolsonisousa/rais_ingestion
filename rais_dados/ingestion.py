
import requests
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# URL do endpoint
url = "https://bi.mte.gov.br/scripts10/dardoweb.cgi"

############ PRENCHER ESSAS VARIAVEIS ##################
start = 2002
final = 2005
folder_name  = "setor_sm"

for i in range(start,final):
    ano_variavel=i
    print(i)
    # Crie o dicionário com a variável
    """data_ = {
       'NT' : '17484013',
        'EA' : 'https%3A%2F%2Fbi.mte.gov.br%2Fbgcaged%2Fcaged_rais_vinculo_id%2F',
        'EC' : '0%3B7C725A%3BBAB19E%3BD9D6CA%3BF0EEDB',
        'AQ' : 'caged_rais_vinculo_basico_tab.par',
        'AC' : '1',
        'XC' : '1',
        'IN' : '1',
        'UM' : '1',
        'UU' : '0',
        'US' : 'basico',
        'DF' : 'https%3A%2F%2Fbi.mte.gov.br%2Fbgcaged%2Fcaged_rais_vinculo_id%2Fcaged_rais_vinculo_basico_tab.php',
        'ND' : '',
        'CJ' : 'Base+de+Gest%E3o+do+MTE%3A%3ACAGED',
        'LI' : 'Capital',
        'V1' : 'Ano+inicial',
        'V2' : 'Ano+final',
        'CO' : 'Sexo+Trabalhador',
        'V3' : 'Ano+inicial',
        'V4' : 'Ano+final',
        'UB' : 'Escolaridade+ap%F3s+2005',
        'V9' : 'Ano+inicial',
        'V0' : 'Ano+final',
        'QU' : '---------N%E3o---------',
        'V5' : 'Ano+inicial',
        'V6' : 'Ano+final',
        'SL' : 'Faixa+Remun+M%E9dia+%28SM%29',
        'V7' : 'Ano+inicial',
        'V8' : 'Ano+final',
        'CN' : '-%3EFrequ%EAncia',
        'CE1' : 'Soma',
        'TT' : '',
        'IU' : '',
        'OL' : 'SemOrdem',
        'OC' : 'SemOrdem',
        'OQ' : 'SemOrdem',
        'PL' : '',
        'YZAno' : '0',
        'YCAno': f'%22{ano_variavel}%22%3ANOME%3B{ano_variavel}',
        'YZV%EDnculo+Ativo+31%2F12' : '0',
        'YCV%EDnculo+Ativo+31%2F12' : '%221%22%3ANOME%3BSim'
    }"""


    ########transformando o data no formato correto para post
    #query_string = "&".join([f"{key}={value}" for key, value in data_.items()])
    query_string=f"NT=59523100&EA=https%3A%2F%2Fbi.mte.gov.br%2Fbgcaged%2Fcaged_rais_vinculo_id%2F&EC=0%3B7C725A%3BBAB19E%3BD9D6CA%3BF0EEDB&AQ=caged_rais_vinculo_basico_tab.par&AC=1&XC=1&IN=1&UM=1&UU=0&US=basico&DF=https%3A%2F%2Fbi.mte.gov.br%2Fbgcaged%2Fcaged_rais_vinculo_id%2Fcaged_rais_vinculo_basico_tab.php&ND=&CJ=Base+de+Gest%E3o+do+MTE%3A%3ACAGED&LI=Capital&V1=Ano+inicial&V2=Ano+final&CO=IBGE+Subsetor&V3=Ano+inicial&V4=Ano+final&UB=Sexo+Trabalhador&V9=Ano+inicial&V0=Ano+final&QU=---------N%E3o---------&V5=Ano+inicial&V6=Ano+final&SL=Faixa+Remun+M%E9dia+%28SM%29&V7=Ano+inicial&V8=Ano+final&CN=-%3EFrequ%EAncia&CE1=Soma&TT=&IU=&OL=SemOrdem&OC=SemOrdem&OQ=SemOrdem&PL=&YZAno=0&YCAno=%22{ano_variavel}%22%3ANOME%3B{ano_variavel}&YZV%EDnculo+Ativo+31%2F12=0&YCV%EDnculo+Ativo+31%2F12=%221%22%3ANOME%3BSim"
    
    # Envia a solicitação POST
    response = requests.post(url, data=query_string,verify=False)

    # Resposta do servidor
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    link_original = soup.find('frame', {'name': 'tabela'}).get('src')

    link_csv = link_original[:-5] + ".csv"

    # Desabilitar os avisos de solicitações inseguras (SSL)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # Link do arquivo CSV
    url_csv = link_csv

    # Faz o download do arquivo
    response_csv = requests.get(url_csv, verify=False)

    # Caminho do diretório local onde você deseja salvar o arquivo
    diretorio_local = f"/Users/bolsolui/Documents/personal/MECAI/git/dados/{folder_name}"

    # Se o diretório não existir, cria-o
    if not os.path.exists(diretorio_local):
        os.makedirs(diretorio_local)

    # Caminho completo do arquivo local
    caminho_local = os.path.join(diretorio_local, f"{folder_name}_{ano_variavel}.csv")
    print(f"Valor de ano_variavel: {ano_variavel}")
    # ...

    # Verifica se o download foi bem-sucedido (código de status 200)
    if response_csv.status_code == 200:
        # Salva o conteúdo no arquivo local com o nome desejado
        with open(caminho_local, 'wb') as file:
            file.write(response_csv.content)
        print(f"Download concluído. Arquivo salvo em {caminho_local}")
    else:
        print(f"Erro ao baixar o arquivo. Código de status: {response_csv.status_code}")