# Urna Eletrônica

Trabalho prático da disciplina Segurança em Sistemas Computacionais. O ano de 2022 no Brasil foi marcado pelas eleições Presidenciais e, em meio aos rumores de fraudes eleitorais, foi proposta como atividade a criação de um algoritmo que simulasse o processo de eleição.


Documentação python-gnupg:
   - https://gnupg.readthedocs.io/en/latest/
   

### Requisitos
  
  - Python 3.10+
  - GnuPG 
  
### Configurando ambiente para execução (LabRedes)

#### Criando ambiente no conda

   - conda create -n [nome_do_ambiente] (criar)
   - source activate [nome_do_ambiente] (ativar)
   - source deactivate [nome_do_ambiente] (desativar)

#### Instalando as dependências no ambiente conda

   - pip install -r requirements.txt                  (Dependências para execução das eleições)
   - pip install -r requirements_apuracao.txt         (Dependências para execução da apuração dos votos)
    

#### Referências
   
   - [Documentação técnica do software da urna eletrônica - Eleições 2022](https://www.tse.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica)
   - [Usando o GPG para Autenticação e Criptografia](https://www.guiafoca.org/guiaonline/avancado/ch20s05.html)
