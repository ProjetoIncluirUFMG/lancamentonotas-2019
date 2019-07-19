from django.contrib import admin

# Register your models here.

from .models import Aluno, Atividade, NotaAluno, Turma

admin.site.register(Aluno)
admin.site.register(Atividade)
admin.site.register(NotaAluno)
admin.site.register(Turma)
