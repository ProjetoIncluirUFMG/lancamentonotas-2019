# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nome_admin = models.CharField(max_length=100)
    login_admin = models.CharField(max_length=100)
    senha_admin = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'administrador'


class Alimento(models.Model):
    id_alimento = models.AutoField(primary_key=True)
    nome_alimento = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'alimento'


class Aluno(models.Model):
    id_aluno = models.AutoField(primary_key=True)
    nome_aluno = models.CharField(max_length=100)
    sexo = models.IntegerField(blank=True, null=True)
    cpf = models.CharField(max_length=15)
    is_cpf_responsavel = models.IntegerField()
    rg = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    endereco = models.CharField(max_length=150, blank=True, null=True)
    numero = models.PositiveIntegerField(blank=True, null=True)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=150, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    data_registro = models.DateField(blank=True, null=True)
    status = models.IntegerField()
    data_desligamento = models.DateField(blank=True, null=True)
    motivo_desligamento = models.CharField(
        max_length=300, blank=True, null=True)
    escolaridade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    nome_responsavel = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aluno'


class Atividade(models.Model):
    id_atividade = models.AutoField(primary_key=True)
    data_funcionamento = models.ForeignKey(
        'DatasFuncionamento', models.DO_NOTHING, db_column='data_funcionamento')
    nome = models.CharField(max_length=45, blank=True, null=True)
    descricao = models.CharField(max_length=300, blank=True, null=True)
    valor_total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividade'


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nome_curso = models.CharField(max_length=45)
    descricao_curso = models.CharField(max_length=300, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'curso'


class DatasFuncionamento(models.Model):
    data_funcionamento = models.DateField(primary_key=True)
    id_periodo = models.ForeignKey(
        'Periodo', models.DO_NOTHING, db_column='id_periodo')

    class Meta:
        managed = False
        db_table = 'datas_funcionamento'


class DatasLancamentosFrequenciasTurmas(models.Model):
    id_data_lancamento = models.AutoField(primary_key=True)
    data_funcionamento = models.ForeignKey(
        DatasFuncionamento, models.DO_NOTHING, db_column='data_funcionamento')
    id_turma = models.ForeignKey(
        'Turma', models.DO_NOTHING, db_column='id_turma')

    class Meta:
        managed = False
        db_table = 'datas_lancamentos_frequencias_turmas'


class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(max_length=100)
    ementa_disciplina = models.CharField(max_length=300, blank=True, null=True)
    id_curso = models.ForeignKey(
        Curso, models.DO_NOTHING, db_column='id_curso')
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'disciplina'


class DisciplinaPreRequisitos(models.Model):
    id_disciplina = models.ForeignKey(
        Disciplina, models.DO_NOTHING, db_column='id_disciplina', primary_key=True)
    id_disciplina_pre_requisito = models.ForeignKey(
        Disciplina, models.DO_NOTHING, db_column='id_disciplina_pre_requisito')

    class Meta:
        managed = False
        db_table = 'disciplina_pre_requisitos'
        unique_together = (('id_disciplina', 'id_disciplina_pre_requisito'),)


class EscalaFrequenciaVoluntario(models.Model):
    id_frequencia = models.IntegerField(primary_key=True)
    data_funcionamento = models.ForeignKey(
        DatasFuncionamento, models.DO_NOTHING, db_column='data_funcionamento')
    hora_entrada = models.TimeField(blank=True, null=True)
    hora_saida = models.TimeField(blank=True, null=True)
    is_presente = models.IntegerField(blank=True, null=True)
    id_voluntario = models.ForeignKey(
        'Voluntario', models.DO_NOTHING, db_column='id_voluntario')

    class Meta:
        managed = False
        db_table = 'escala_frequencia_voluntario'


class Falta(models.Model):
    id_falta = models.AutoField(primary_key=True)
    id_turma_aluno = models.ForeignKey(
        'TurmaAlunos', models.DO_NOTHING, db_column='id_turma_aluno')
    data_funcionamento = models.ForeignKey(
        DatasFuncionamento, models.DO_NOTHING, db_column='data_funcionamento')
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'falta'
        unique_together = (
            ('id_falta', 'id_turma_aluno', 'data_funcionamento'),)


class Log(models.Model):
    id_log = models.AutoField(primary_key=True)
    data_log = models.DateField()
    tipo_tarefa = models.CharField(max_length=100)
    nome_usuario = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'log'


class NotaAluno(models.Model):
    id_nota = models.AutoField(primary_key=True)
    id_turma_aluno = models.ForeignKey(
        'TurmaAlunos', models.DO_NOTHING, db_column='id_turma_aluno')
    id_atividades_turma = models.ForeignKey(
        'TurmaAtividades', models.DO_NOTHING, db_column='id_atividades_turma')
    valor_nota = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nota_aluno'
        unique_together = (
            ('id_nota', 'id_turma_aluno', 'id_atividades_turma'),)


class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    valor_pago = models.FloatField()
    situacao = models.IntegerField()
    condicao = models.IntegerField()
    tipo_isencao_pendencia = models.IntegerField(blank=True, null=True)
    num_recibo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagamento'


class PagamentoAlimentos(models.Model):
    id_pagamento = models.ForeignKey(
        Pagamento, models.DO_NOTHING, db_column='id_pagamento', primary_key=True)
    id_alimento = models.ForeignKey(
        Alimento, models.DO_NOTHING, db_column='id_alimento')
    quantidade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagamento_alimentos'
        unique_together = (('id_pagamento', 'id_alimento'),)


class Periodo(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    nome_periodo = models.CharField(max_length=45)
    data_inicio = models.DateField()
    data_termino = models.DateField(blank=True, null=True)
    is_atual = models.IntegerField(blank=True, null=True)
    valor_liberacao_periodo = models.FloatField()
    freq_min_aprov = models.IntegerField()
    total_pts_periodo = models.IntegerField()
    min_pts_aprov = models.IntegerField()
    quantidade_alimentos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'periodo'


class Permissao(models.Model):
    id_permissao = models.AutoField(primary_key=True)
    titulo_permissao = models.CharField(max_length=45)
    controller = models.CharField(max_length=45)
    action = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'permissao'


class Turma(models.Model):
    id_turma = models.AutoField(primary_key=True)
    nome_turma = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    horario_inicio = models.TimeField(blank=True, null=True)
    horario_fim = models.TimeField(blank=True, null=True)
    status = models.IntegerField()
    id_periodo = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column='id_periodo')
    id_disciplina = models.ForeignKey(
        Disciplina, models.DO_NOTHING, db_column='id_disciplina')
    sala = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turma'


class TurmaAlunos(models.Model):
    id_turma_aluno = models.AutoField(primary_key=True)
    id_turma = models.ForeignKey(
        Turma, models.DO_NOTHING, db_column='id_turma')
    id_aluno = models.ForeignKey(
        Aluno, models.DO_NOTHING, db_column='id_aluno')
    id_pagamento = models.ForeignKey(
        Pagamento, models.DO_NOTHING, db_column='id_pagamento')
    aprovado = models.IntegerField(blank=True, null=True)
    liberacao = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turma_alunos'


class TurmaAtividades(models.Model):
    id_atividades_turma = models.AutoField(primary_key=True)
    id_turma = models.ForeignKey(
        Turma, models.DO_NOTHING, db_column='id_turma')
    id_atividade = models.ForeignKey(
        Atividade, models.DO_NOTHING, db_column='id_atividade')

    class Meta:
        managed = False
        db_table = 'turma_atividades'


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    login_usuario = models.CharField(max_length=100)
    senha_usuario = models.CharField(max_length=100)
    id_voluntario = models.ForeignKey(
        'Voluntario', models.DO_NOTHING, db_column='id_voluntario')

    class Meta:
        managed = False
        db_table = 'usuario'
        unique_together = (('id_usuario', 'id_voluntario'),)


class UsuarioPermissoes(models.Model):
    id_usuario = models.ForeignKey(
        Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_voluntario = models.ForeignKey(
        Usuario, models.DO_NOTHING, db_column='id_voluntario')
    id_usuario_permissao = models.ForeignKey(
        Permissao, models.DO_NOTHING, db_column='id_usuario_permissao')

    class Meta:
        managed = False
        db_table = 'usuario_permissoes'
        unique_together = (
            ('id_usuario', 'id_voluntario', 'id_usuario_permissao'),)


class Voluntario(models.Model):
    id_voluntario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=15)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    formacao = models.CharField(max_length=45, blank=True, null=True)
    profissao = models.CharField(max_length=45, blank=True, null=True)
    telefone_fixo = models.CharField(max_length=45, blank=True, null=True)
    telefone_celular = models.CharField(max_length=45, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    complemento = models.CharField(max_length=45, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    funcao_informatica = models.CharField(
        max_length=100, blank=True, null=True)
    funcao_rh = models.CharField(max_length=100, blank=True, null=True)
    funcao_secretaria = models.CharField(max_length=100, blank=True, null=True)
    funcao_marketing = models.CharField(max_length=100, blank=True, null=True)
    carga_horaria = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_desligamento = models.DateField(blank=True, null=True)
    motivo_desligamento = models.CharField(
        max_length=300, blank=True, null=True)
    disponibilidade = models.TextField(blank=True, null=True)
    conhecimento = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'voluntario'


class VoluntarioDisciplinas(models.Model):
    id_voluntario = models.ForeignKey(
        Voluntario, models.DO_NOTHING, db_column='id_voluntario', primary_key=True)
    id_disciplina = models.ForeignKey(
        Disciplina, models.DO_NOTHING, db_column='id_disciplina')

    class Meta:
        managed = False
        db_table = 'voluntario_disciplinas'
        unique_together = (('id_voluntario', 'id_disciplina'),)


class VoluntarioTurmas(models.Model):
    id_voluntario = models.ForeignKey(
        Voluntario, models.DO_NOTHING, db_column='id_voluntario', primary_key=True)
    id_turma = models.ForeignKey(
        Turma, models.DO_NOTHING, db_column='id_turma')

    class Meta:
        managed = False
        db_table = 'voluntario_turmas'
        unique_together = (('id_voluntario', 'id_turma'),)
