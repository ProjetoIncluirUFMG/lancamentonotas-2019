import csv
import itertools

from django.core.management.base import BaseCommand, no_translations, CommandError
from django.db import transaction
from openpyxl import load_workbook

from mainapp.models import (Atividade, DatasFuncionamento, Turma,
                            TurmaAtividades, Aluno, Periodo, NotaAluno, TurmaAlunos)


periodo = Periodo.objects.get(is_atual=1)


class Command(BaseCommand):
    help = 'Exporta um arquivo CSV a partir de uma planilha'

    requires_migrations_checks = True
    requires_system_checks = True
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('excel_file',
                            type=str, help='Planilha Excel')

    @no_translations
    @transaction.atomic()
    def handle(self, *args, **options):
        wb = load_workbook(
            filename=options['excel_file'], data_only=True)
        sheets = wb.sheetnames
        for sheetname in sheets:
            if not Turma.objects.filter(nome_turma=sheetname, id_periodo=periodo).exists():
                raise CommandError(
                    'Turma %s não encontrada no banco de dados!' % sheetname)
            turma = Turma.objects.get(
                nome_turma=sheetname, id_periodo=periodo)
            self.stdout.write(self.style.SUCCESS(
                '[1/5] Turma %s encontrada' % turma.nome_turma))
            sheet = wb[sheetname]
            # Checando se as âncoras do modelo padrão estão presentes
            if not (sheet['B6'].value.strip() == 'Nome da Atividade' and sheet['B8'].value.strip() == 'Nome do Aluno' and sheet['J6'].value.strip() == 'Total'):
                raise CommandError('Arquivo não conforma com modelo padrão!')
            self.stdout.write(self.style.SUCCESS(
                '[2/5] Documento bem-formatado'))
            alunos = list()
            for num in itertools.count(10):
                if sheet['B%d' % num].value is None:
                    break
                value = sheet['B%d' % num].value.strip().upper()
                if value == '':
                    break
                try:
                    aluno = TurmaAlunos.objects.get(
                        id_aluno__nome_aluno=value, id_turma=turma)
                    alunos.append({'ent': aluno, 'pos': num})
                    self.stdout.write(
                        '\tAluno "%s" encontrado (%s)' % (aluno.id_aluno.nome_aluno, 'B%d' % num))
                except TurmaAlunos.DoesNotExist:
                    raise CommandError(
                        'Aluno %s não existe no banco de dados!' % value)
            self.stdout.write(self.style.SUCCESS(
                '[3/5] Identificados %d alunos' % len(alunos)))
            atividades = list()
            for letter in self.char_range('c', 'i'):
                if sheet['%s6' % letter].value is None:
                    break
                value = sheet['%s6' % letter].value.strip()
                if value == '':
                    break
                try:
                    atividade = TurmaAtividades.objects.get(
                        id_atividade__nome=value, id_turma=turma)
                    atividades.append({'ent': atividade, 'pos': letter})
                    self.stdout.write(
                        '\tAtividade "%s" encontrada (%s)' % (atividade.id_atividade.nome, '%s6' % num))
                except TurmaAtividades.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        'Atividades desta turma no banco de dados: %s' % list(map(lambda ativ: ativ.nome, Atividade.objects.filter(
                            turmaatividades__id_turma=turma, turmaatividades__id_turma__id_periodo=periodo)))))
                    Atividade.objects.filter(
                        turmaatividades__id_turma__nome_turma='CAP201', turmaatividades__id_turma__id_periodo__is_atual=1)
                    raise CommandError(
                        'Atividade "%s" não encontrada no banco de dados!' % value)

            self.stdout.write(self.style.SUCCESS(
                '[3/5] Identificadas %d atividades' % len(atividades)))
            for aluno in alunos:
                for atividade in atividades:
                    if NotaAluno.objects.filter(
                            id_turma_aluno=aluno['ent'], id_atividades_turma=atividade['ent']).exists():
                        raise CommandError('Aluno "%s" já tem nota(s) lançadas para a atividade "%s"!' % (
                            aluno['ent'].id_aluno.nome_aluno, atividade['ent'].id_atividade.nome))
                    nota = NotaAluno(
                        id_turma_aluno=aluno['ent'], id_atividades_turma=atividade['ent'], valor_nota=sheet['%s%d' % (atividade['pos'], aluno['pos'])].value)
                    nota.save()
                    self.stdout.write('\tNota: %s (%d), Aluno: "%s" (%d), Atividade: "%s" (%d)' % (nota.valor_nota, nota.id_nota, nota.id_turma_aluno.id_aluno.nome_aluno,
                                                                                                   nota.id_turma_aluno.id_aluno.id_aluno, nota.id_atividades_turma.id_atividade.nome, nota.id_atividades_turma.id_atividade.id_atividade))
            self.stdout.write(self.style.SUCCESS(
                '[5/5] Lançadas %d notas' % (len(atividades)*len(alunos))))

    def char_range(self, c1, c2):
        """Generates the characters from `c1` to `c2`, inclusive."""
        for c in range(ord(c1), ord(c2)+1):
            yield chr(c)
