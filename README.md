# lancamentonotas-2019
Aplicação provisória para lançamento de notas. 

## Setup
- Crie os containers
    ```bash
    docker-compose up -d
    ```
- Popule o banco de dados **apenas** com os alunos, turmas, atividades, etc relativas ao semestre atual (e somente as tableas inclusas em [models.py](./lancanotas/mainapp/models.py))
    ```bash
    docker exec -i lancamentonotas-2019_internaldb_1 sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < database.sql
    ```
- Setup do Django (dentro do container-serviço *app*)
    ```bash
    cd lancanotas
    python manage.py migrate
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
Extraia os dados do container, usando ```docker exec -i lancamentonotas-2019_internaldb_1 sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > lancamentos.sql``` por exemplo, e utlize o SQL gerado para importar os dados onde quiser. Tenha atenção para não importar também as tabelas de autenticação geradas pelo Django (auth_* e django_*).


Este programa não foi feito para uso regular, sem garantias de integridade de dados, etc.