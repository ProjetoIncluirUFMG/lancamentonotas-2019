import csv
import io
import sys

from django.core.management.base import BaseCommand, CommandError

from mainapp.models import Aluno


class Command(BaseCommand):
    help = 'Importa um arquivo CSV contendo lançamentos de notas'

    requires_migrations_checks = True
    requires_system_checks = True
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+',
                            type=open, help='Arquivo CSV')

    def handle(self, *args, **options):
        csvfile = options['csv_file'][0]
        has_header = csv.Sniffer().has_header(csvfile.readline())
        dialect = csv.Sniffer().sniff(csvfile.readline())
        csvfile.seek(0)
        data_reader = csv.reader(csvfile, dialect)
        if has_header:
            data_reader.__next__()
        line_len = len(data_reader.__next__())
        ativ_num = line_len - 2
        try:
            for row in data_reader:
                aluno = Aluno.objects.filter(nome_aluno=row[0].upper())
                if aluno.exists() and len(row) == line_len:
                    self.stdout.write('[%s] Processando aluno "%s":' %
                                      (data_reader.line_num, aluno[0].nome_aluno))
                else:
                    self.stdout.write(self.style.WARNING(
                        '[%s] Não contém um aluno válido, ignorando' % data_reader.line_num))
        except csv.Error:
            self.stdout.write(self.style.ERROR(
                'Erro na linha %s' % data_reader.line_num))
