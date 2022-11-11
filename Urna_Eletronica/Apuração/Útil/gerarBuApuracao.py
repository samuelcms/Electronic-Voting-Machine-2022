import json
import os

from datetime import datetime

COLUNAS_RELATORIO = 38
TIME_PATERN = "%H:%M:%S"
DATE_PATTERN = "%d/%m/%Y"
BLANK_LINE = "\n\n"
NEW_LINE = "\n"
BARRA = ("\\" if os.name == "nt" else "/")


# Funções para obter a data e hora corrente.
def getDate(): return  datetime.now().strftime(DATE_PATTERN)
def getTime(): return  datetime.now().strftime(TIME_PATERN)

'''
    Gera uma string formatada com o nome do campo e o seu respectivo valor alinhado à direita.
    Ex: "Eleitores Aptos:                      0"
'''
def gerarLinhaFormatada(nomeCampo, campo):

    deslocamento = (COLUNAS_RELATORIO - (len(nomeCampo) - 1))
    return f"{nomeCampo}{campo.rjust(deslocamento)}"

#gerarLinhaFormatada


# Recupera os dados do arquivo de votação para geração do Boletim de Urna.
def parseBoletim(nomeArquivo):

    try:
        with open(nomeArquivo) as file:
            conteudoArquivo = file.read()
            boletimJson = json.loads(conteudoArquivo)
            
            return boletimJson

    except FileNotFoundError: pass
    
# parseBoletim()


def gerarCabecalho():
    
    cabecalho = ("JUSTIÇA ELEITORAL").center(COLUNAS_RELATORIO) + BLANK_LINE
    cabecalho += ("Tribunal Regional Eleitoral [Lab. Redes]").center(COLUNAS_RELATORIO) + BLANK_LINE
    cabecalho += ("1º Turno").center(COLUNAS_RELATORIO) + NEW_LINE
    cabecalho += (f"{getDate()}").center(COLUNAS_RELATORIO) + BLANK_LINE
    cabecalho += ("Eleições Gerais").center(COLUNAS_RELATORIO) + BLANK_LINE
        
    return cabecalho

# gerarCabecalho()


def getInfoEleicao(boletimJson):
    
    infoEleicao = gerarLinhaFormatada("Município:", "Barbacena") + NEW_LINE    
    infoEleicao += gerarLinhaFormatada("Eleitores Aptos:", boletimJson["info_eleitores"]["eleitores_aptos"]) + NEW_LINE
    infoEleicao += gerarLinhaFormatada("Comparecimentos:", boletimJson["info_eleitores"]["comparecimentos"]) + NEW_LINE
    infoEleicao += gerarLinhaFormatada("Faltas:", boletimJson["info_eleitores"]["faltas"])  + BLANK_LINE

    infoEleicao += gerarLinhaFormatada("Data de Abertura:", boletimJson["data_hora"]["data_abertura"]) + NEW_LINE
    infoEleicao += gerarLinhaFormatada("Hora de Abertura:", boletimJson["data_hora"]["hora_abertura"]) + BLANK_LINE
    infoEleicao += gerarLinhaFormatada("Data de Fechamento:", boletimJson["data_hora"]["data_fechamento"]) + NEW_LINE
    infoEleicao += gerarLinhaFormatada("Hora de Fechamento:", boletimJson["data_hora"]["hora_fechamento"]) + BLANK_LINE

    infoEleicao += "".center(COLUNAS_RELATORIO + 1, '=') + NEW_LINE
    
    return infoEleicao

# getInfoEleicao()


def getResCargo(boletimJson, nomeCabecalho, cargoCandidato):

    resCandidato = NEW_LINE + nomeCabecalho.center(COLUNAS_RELATORIO + 1, '-') + BLANK_LINE
    
    resCandidato += gerarLinhaFormatada("Votos Válidos:", boletimJson["candidatos"][cargoCandidato][0]["votos_validos"]) + NEW_LINE
    resCandidato += gerarLinhaFormatada("Votos Brancos:", boletimJson["candidatos"][cargoCandidato][0]["votos_brancos"]) + NEW_LINE
    resCandidato += gerarLinhaFormatada("Votos Nulos:", boletimJson["candidatos"][cargoCandidato][0]["votos_nulos"]) + BLANK_LINE

    deslocamento = 1 + (len(boletimJson["candidatos"][cargoCandidato][1]["codigo"]) - 2)
    resCandidato += gerarLinhaFormatada(f"ID{deslocamento * ' '}Nome", "Votos") + BLANK_LINE
    index = 1
    while index < len(boletimJson["candidatos"][cargoCandidato]):
        candidato = boletimJson["candidatos"][cargoCandidato][index]
        resCandidato += gerarLinhaFormatada(f"{candidato['codigo']} {candidato['nome']}", candidato["votos"]) + NEW_LINE       
        index += 1
        
    return resCandidato

# getResCargo()


def gerarBoletim(boletim):
    
    boletimJson = boletim
    
    relatorio = gerarCabecalho()
    relatorio += getInfoEleicao(boletimJson)    
    relatorio += getResCargo(boletimJson, "PRESIDENTE", "presidente") 
    relatorio += getResCargo(boletimJson, "GOVERNADOR", "governador")
    relatorio += getResCargo(boletimJson, "SENADOR", "senador")
    relatorio += getResCargo(boletimJson, "DEP. FEDERAL", "deputado_federal")
    relatorio += getResCargo(boletimJson, "DEP. ESTADUAL", "deputado_estadual")

    # Gerando o boletim da urna em formato ".txt".
    with open(f'Resultado{BARRA}resultado_apuracao.txt', 'w', encoding='utf8') as file:
        file.write(relatorio)
    print(relatorio)

# gerarBoletim()


def main():
    gerarBoletim()


if __name__ == "__main__":
    main()