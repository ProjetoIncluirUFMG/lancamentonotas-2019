# lancamentonotas-2019
Aplicação provisória para lançamento de notas. 

## Setup
- Crie os containers
    ```bash
    docker-compose up -d
    ```
- Popule o banco de dados
    ```bash
    docker exec -i lancamentonotas-2019_internaldb_1 sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD" fechamentoincluir' < database.sql
    ```
- Setup do Django (dentro do container-serviço *app*)
    ```bash
    cd lancanotas
    python manage.py migrate
    python manage.py check
    ```
- Pronto para executar o comando!

## Executando o comando

O comando ```python manage.py importnotas``` lê um arquivo CSV com o nome do código de uma turma ('ART201', por ex.), devidamente formatado desta forma:
```csv
Nome do Aluno, [Atividade(s)], Nota Final
João, [1,2...], 90
```
e insere as notas no banco de dados apropriadamente, ignorando a última coluna da nota final.


Há também um argumento que pode ser adicionado ao final do comando: ```--final-only```. Ele fará com que só seja lançada a Nota Final especificada na última coluna do arquivo.

## Use os dados no seu banco de dados
Extraia os dados do container, usando ```docker exec -i lancamentonotas-2019_internaldb_1 sh -c 'exec mysqldump fechamentoincluir -uroot -p"$MYSQL_ROOT_PASSWORD"' > lancamentos.sql``` por exemplo, e utlize o SQL gerado para importar os dados onde quiser. Tenha atenção para não importar também as tabelas geradas pelo Django (django_*).


Este programa não foi feito para uso regular, sem garantias de integridade de dados, etc.