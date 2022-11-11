import gnupg
import json
import os

from datetime import datetime
from Útil.gerarBuApuracao import *

# Código adotado por cada partido de acordo com o cargo.
PRESIDENTE = ["91", "81", "71", "61", "51"]
GOVERNADOR = ["91", "81", "71", "61", "51"]
SENADOR = ["912", "812", "712", "612", "512"]
DEP_FEDERAL = ["9101", "8101", "7101", "6101", "5101"]
DEP_ESTADUAL = ["91000", "81000", "71000", "61000", "51000"]

NOME_ARQUIVO_VOTOS = "votos"
EXTENSAO_ARQUIVO = ".txt"
VALOR_INICIAL_ARQUIVO = 1
QUANTIDADE_URNAS = 4 
LISTA_VOTOS = []

# Representação do voto branco.
VOTO_BRANCO = "0"

# Nome do arquivo que contém a estrutura para armazenar os votos. (Dicionário BU)
ESTRUTURA_VOTOS = 'buApuracao.json'

# Obtém o diretório atual do programa.
#DIRETORIO = "/home/samuel/Downloads/Apuração" # <- TEMP '''os.getcwd()'''

# Define o caractere separador de diretórios de acordo com Sistema Operacional.
BARRA = ("\\" if os.name == "nt" else "/")

# Definindo o diretório do GPG.
gpg = gnupg.GPG(gnupghome=f'{BARRA}home{BARRA}aluno{BARRA}.gnupg')


# Funções para obter a data e hora corrente.
def getDate(): return  datetime.now().strftime(DATE_PATTERN)
def getTime(): return  datetime.now().strftime(TIME_PATERN)

# Relação de votos lidas dos arquivos de urna.
votos = []

# Dados sobre os eleitores.
info_eleitores = {'total_eleitores':0, 'comparecimentos':0, 'faltas':0}



# Descriptografa o arquivo de votos (remove a assinatura do TSE).
def descriptografar_arquivo_votos(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        gpg.decrypt_file(nome_arquivo, output = nome_arquivo)
        
        '''
        # Status da operação
        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)
        '''

# def descriptografar_arquivo_votos()

# Verifica se um voto é válido. Retorna true, se verdadeiro e false caso contrário.
def verificar_voto(cargo, voto_computado): return True if voto_computado in cargo else False


# Retorna True se o voto for branco e false, caso contrário.
def voto_branco(voto_computado): return True if voto_computado == VOTO_BRANCO else False


# Obtém o voto do eleitor a partir do dicionário 'voto'.
def processar_voto(voto_eleitor, cargo): return voto_eleitor[cargo]


# Carregando para uma variável o modelo do dicionário de apuração.
def carregar_estrutura_apuracao():
    
    with open(f"Útil{BARRA}{ESTRUTURA_VOTOS}") as file:
        data = file.read()   
    
    return json.loads(data)

# carregar_dados_apuracao()


def registra_voto_cargo(estrutura_apuracao, codigos, cargo, voto_eleitor): 

    if verificar_voto(codigos, voto_eleitor) == True:
        
        estrutura_apuracao["candidatos"][cargo][0]["votos_validos"] = str(int(estrutura_apuracao["candidatos"][cargo][0]["votos_validos"]) + 1)

        i = 1
        while i < len(estrutura_apuracao["candidatos"][cargo]):
            
            if(voto_eleitor == estrutura_apuracao["candidatos"][cargo][i]["codigo"]):
                
                estrutura_apuracao["candidatos"][cargo][i]["votos"] = str(int(estrutura_apuracao["candidatos"][cargo][i]["votos"]) + 1)
                break
            
            else: i += 1
    
    elif voto_branco(voto_eleitor): estrutura_apuracao["candidatos"][cargo][0]["votos_brancos"] = str(int(estrutura_apuracao["candidatos"][cargo][0]["votos_brancos"]) + 1)
    else: estrutura_apuracao["candidatos"][cargo][0]["votos_nulos"] = str(int(estrutura_apuracao["candidatos"][cargo][0]["votos_nulos"]) + 1)

# registra_voto_cargo() 


def registrar_data_hora(apuracao, data, hora):
    
    apuracao["data_hora"][data] = getDate()
    apuracao["data_hora"][hora] = getTime()

#registrar_data_hora()


def registrar_resultados(votos_apurados):
    
    # Gerando um arquivo ".json" a partir do dicionário com o boletim final (resultado da eleição).
    with open(f"Resultado{BARRA}resultado_apuracao.json",'w') as convert_file:
        convert_file.write(json.dumps(votos_apurados))

    # Gerando um boletim com o resultado da apuração das urnas.
    gerarBoletim(votos_apurados)

# registrar_resultados()


def apurar_votos():

    # Estrutura com os votos apurados.
    votos_apurados = carregar_estrutura_apuracao()
    carregar_dados_eleicao()

    registrar_data_hora(votos_apurados, "data_abertura", "hora_abertura")
    
    for voto_eleitor in LISTA_VOTOS:
        
        registra_voto_cargo(votos_apurados, PRESIDENTE, "presidente", processar_voto(voto_eleitor, "Presidente"))
        registra_voto_cargo(votos_apurados, GOVERNADOR, "governador", processar_voto(voto_eleitor, "Governador"))
        registra_voto_cargo(votos_apurados, SENADOR, "senador", processar_voto(voto_eleitor, "Senador"))
        registra_voto_cargo(votos_apurados, DEP_FEDERAL, "deputado_federal", processar_voto(voto_eleitor, "Deputado Federal"))
        registra_voto_cargo(votos_apurados, DEP_ESTADUAL, "deputado_estadual", processar_voto(voto_eleitor, "Deputado Estadual"))

    registrar_data_hora(votos_apurados, "data_fechamento", "hora_fechamento")
    atualiza_dados_eleitores(votos_apurados)
    registrar_resultados(votos_apurados)
            
# apurar_votos()


# Converte um String para o formato JSON.
def converter_para_json(linha):
    
    # Formatando a linha de modo que as strings sejam separadas por aspas conforme a especifcação JSON.
    linha = linha.replace('\'', '\"')
    return json.loads(linha)

# converter_para_json()


# Contabiliza os dados da eleição relativos aos eleitores: Total de eleitores, comparecimentos e faltas.
def contabiliza_dados_eleitores(dados):
    
    dados = dados.replace(':', '-').replace(' ', '').replace(',','-').split('-')
    
    info_eleitores["comparecimentos"] += int(dados[1])
    info_eleitores["faltas"] += int(dados[3])
    
# contabiliza_dados_eleicao()


def atualiza_dados_eleitores(estrutura_apuracao):

    info_eleitores["total_eleitores"] += info_eleitores["comparecimentos"] + info_eleitores["faltas"]

    estrutura_apuracao["info_eleitores"]["eleitores_aptos"] = str(info_eleitores["total_eleitores"])
    estrutura_apuracao["info_eleitores"]["comparecimentos"] = str(info_eleitores["comparecimentos"])
    estrutura_apuracao["info_eleitores"]["faltas"] = str(info_eleitores["faltas"])

# atualiza_dados_eleitores()


def carregar_dados_eleicao():
    
    index = 1
    numerourna = 1
    while index <= QUANTIDADE_URNAS:
        try:
            if verificar_dados_integros(f'Resultado Urnas{BARRA}{NOME_ARQUIVO_VOTOS}{numerourna:04d}{EXTENSAO_ARQUIVO}',
                                    f"Resultado Urnas{BARRA}{NOME_ARQUIVO_VOTOS}{numerourna:04d}signature{EXTENSAO_ARQUIVO}"):
                index+= 1
                numerourna += 1
            else:
                print("\033[31m\nDADOS DOS VOTOS ALTERADOS, FRAUDE DETECTADA!!!\n\nENCERRANDO APURAÇÃO!!!\033[0;0m\n")
                exit()
        except FileNotFoundError:
            numerourna += 1
    index = 1
    numerourna = 1
    while index <= QUANTIDADE_URNAS:
        try:
            parse_arquivo_votos(f'Resultado Urnas{BARRA}{NOME_ARQUIVO_VOTOS}{numerourna:04d}{EXTENSAO_ARQUIVO}')
            index += 1
            numerourna += 1
        except FileNotFoundError:
            numerourna += 1   

# carregar_dados_eleicao()


def verificar_dados_integros(nome_arquivo,nome_assinatura_arquivo):
    with open(nome_assinatura_arquivo, "rb") as ASSINATURA:
        DADOS_INTEGROS = gpg.verify_file(ASSINATURA,nome_arquivo)
    return DADOS_INTEGROS.valid



# Obtém o conteúdo de um arquivo que contém os votos e os dados da eleição.
def parse_arquivo_votos(nome_arquivo):

    descriptografar_arquivo_votos(nome_arquivo)

    with open(nome_arquivo) as file:
        conteudo_arquivo = file.readlines()
        
    qtd_linhas = len(conteudo_arquivo)

    contador = 0
    for linha in conteudo_arquivo:
            
        if(contador == (qtd_linhas - 1)):
            contabiliza_dados_eleitores(linha)
            break

        # Adicionando cada voto à lista de votos.
        LISTA_VOTOS.append(converter_para_json(linha)['candidatos'])
            
        contador += 1
        
    

def main():
    apurar_votos()


if __name__ == "__main__":
    main()
