import csv
import io
import os
import sys

from django.core.management.base import (BaseCommand, CommandError,
                                         no_translations)
from django.db import transaction

from mainapp.models import (Aluno, Atividade, DatasFuncionamento, NotaAluno,
                            Turma, TurmaAlunos, TurmaAtividades)

date_default = DatasFuncionamento.objects.get(
    data_funcionamento__year=2019, data_funcionamento__month=7, data_funcionamento__day=6)
data_new = DatasFuncionamento.objects.get(
    data_funcionamento__year=2019, data_funcionamento__month=7, data_funcionamento__day=20)


class Command(BaseCommand):
    help = 'Importa um arquivo CSV contendo lançamentos de notas'

    requires_migrations_checks = True
    requires_system_checks = True
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('csv_file',
                            type=open, help='Arquivo CSV')
        parser.add_argument('--final-only', action='store_true',
                            help='Lance apenas uma nota final')

    @no_translations
    def handle(self, *args, **options):
        csvfile = options['csv_file']
        has_header = csv.Sniffer().has_header(csvfile.readline())
        dialect = csv.Sniffer().sniff(csvfile.readline())
        csvfile.seek(0)
        data_reader = csv.reader(csvfile, dialect)
        line_len = len(next(data_reader))
        classentity = Turma.objects.get(
            nome_turma=os.path.basename(csvfile.name)[:-4])
        activities = list()
        if has_header:
            csvfile.seek(0)
            headers = next(data_reader)
            activities = self.get_activities(
                headers[1:-1], classentity)
        elif not options['final_only']:
            raise CommandError(
                'Erro: Impossível criar atividades intermediárias sem cabeçários')
        try:
            with transaction.atomic():
                for row in data_reader:
                    aluno = Aluno.objects.filter(nome_aluno=row[0].upper())
                    if aluno.exists() and len(row) == line_len:
                        self.stdout.write(self.style.SUCCESS('[%s]\tProcessando aluno "%s":' %
                                                             (data_reader.line_num, aluno[0].nome_aluno)))
                        if not options['final_only']:
                            for pos, activity in enumerate(activities):
                                nota = NotaAluno(id_turma_aluno=TurmaAlunos.objects.get(id_turma=classentity, id_aluno=aluno[0]), id_atividades_turma=TurmaAtividades.objects.get(
                                    id_turma=classentity, id_atividade=activity), valor_nota=row[pos+1])
                                nota.save()
                                self.stdout.write('\t\tNota: %s [%s], TurmaAluno: [%s], AtividadesTurma: [%s]' % (
                                    nota.valor_nota, nota.id_nota, nota.id_turma_aluno.id_turma_aluno, nota.id_atividades_turma.id_atividades_turma))
                        else:
                            final_activity = Atividade(
                                data_funcionamento=data_new, nome='Nota Final', valor_total=100)
                            final_activity.save()
                            activity_class = TurmaAtividades(
                                id_turma=classentity, id_atividade=final_activity)
                            activity_class.save()
                            nota = NotaAluno(id_turma_aluno=TurmaAlunos.objects.get(
                                id_turma=classentity, id_aluno=aluno[0]), id_atividades_turma=activity_class, valor_nota=row[-1])
                            nota.save()
                            self.stdout.write('\t\tAtividade Final: [%s], Nota: %s [%s], TurmaAluno: id[%s], AtividadesTurma: [%s]' % (
                                final_activity.id_atividade, nota.valor_nota, nota.id_nota, nota.id_turma_aluno.id_turma_aluno, nota.id_atividades_turma.id_atividades_turma))
                    else:
                        self.stdout.write(self.style.WARNING(
                            '[%s]\tLinha inválida, ignorando "%s"' % (data_reader.line_num, row[0])))
        except:
            raise CommandError(
                'Erro na linha %s, nenhum dado foi escrito ao banco de dados' % data_reader.line_num)

    def get_activities(self, activities, classentity):
        return list(map(lambda actt: Atividade.objects.get(
            nome=actt, data_funcionamento=date_default, turmaatividades__id_turma=classentity), activities))
