# PBIT-Analyzer

# Power BI Template Analyzer
Uma aplicação Flask projetada para extrair informações estruturais de projetos Power BI a partir de arquivos .pbit. O objetivo é auxiliar na geração de documentação técnica sem expor credenciais ou dados sensíveis, pois o .pbit contém apenas a estrutura do projeto.

# Funcionalidade Principal

O aplicativo permite analisar arquivos .pbit e exportar a estrutura do relatório, incluindo tabelas, colunas, medidas DAX, funções de segurança e páginas do relatório, facilitando a documentação e auditoria de projetos Power BI.

# Passo a Passo de Uso

# 1- Gerar o arquivo .pbit:

Abra seu relatório no Power BI Desktop.

Navegue até Arquivo → Salvar Como → Power BI Template (.pbit).

Salve o arquivo em seu computador.

# 2- Importar e processar no PBIT-Analyzer:

Acesse a aplicação no navegador.

Selecione o arquivo .pbit usando o botão de upload.

Clique em Enviar para processar o arquivo.

# 3- Visualizar e exportar informações:

Após o processamento, será gerada uma página com todas as informações estruturais do projeto.

É possível exportar os dados em Excel para documentação ou análise posterior.

# Funcionalidades Técnicas

Leitura Segura de Arquivos: suporte a múltiplas codificações (UTF-8, UTF-16) e tratamento de erros de decodificação.

Processamento de .pbit: descompactação de arquivos ZIP, análise do DataModelSchema, extração de expressões M e DAX, e identificação de tabelas calculadas versus tabelas padrão.

Segurança: validação de extensão de arquivo, sanitização de nomes de arquivo e nenhum dado sensível é processado.

# Requisitos

O arquivo requirements.txt deve conter:

Flask==2.3.3

Werkzeug==2.3.7
