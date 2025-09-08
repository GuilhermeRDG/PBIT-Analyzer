# PBIT-Analyzer


Power BI Template Analyzer
Uma aplicação Flask para analisar arquivos .pbit (Power BI Template) e extrair informações sobre o modelo de dados, medidas, funções de segurança e páginas do relatório.

#Funcionalidades
Upload de arquivos .pbit: Interface para upload seguro de arquivos Power BI Template

Extração de metadados: Descompacta e analisa o conteúdo do arquivo .pbit

Análise do modelo de dados: Identifica tabelas, colunas e seus tipos

Detecção de medidas: Extrai todas as medidas DAX do modelo

Verificação de segurança: Analisa funções e permissões de segurança

Visualização de páginas: Lista todas as páginas do relatório

Classificação de tabelas: Distingue entre tabelas calculadas e tabelas padrão


#Como Usar
Acesse a aplicação no navegador

Selecione um arquivo .pbit usando o botão de upload

Clique em enviar para processar o arquivo

Visualize as informações extraídas na interface

Estrutura do requirements.txt
O arquivo requirements.txt contém todas as dependências necessárias:

txt
Flask==2.3.3
Werkzeug==2.3.7
Funcionalidades Técnicas
Leitura Segura de Arquivos
Suporte a múltiplas codificações (UTF-8, UTF-16, UTF-16-LE, UTF-16-BE)

Tratamento de erros de decodificação

Processamento de .pbit
Descompactação de arquivos ZIP (.pbit)

Análise do DataModelSchema

Extração de expressões M e DAX

Identificação de tabelas calculadas vs. tabelas padrão

Segurança
Validação de extensões de arquivo permitidas

Sanitização de nomes de arquivo

Tratamento de erros robusto
