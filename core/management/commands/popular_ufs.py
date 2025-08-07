import sys
from django.core.management.base import BaseCommand
from core.models import UF

class Command(BaseCommand):
    help = 'Popula o banco de dados com as Unidades Federativas (UFs) do Brasil'

    # Lista de UFs para popular o banco de dados
    UFS_BRASIL = [
        {'sigla': 'AC', 'nome': 'Acre'},
        {'sigla': 'AL', 'nome': 'Alagoas'},
        {'sigla': 'AP', 'nome': 'Amapá'},
        {'sigla': 'AM', 'nome': 'Amazonas'},
        {'sigla': 'BA', 'nome': 'Bahia'},
        {'sigla': 'CE', 'nome': 'Ceará'},
        {'sigla': 'DF', 'nome': 'Distrito Federal'},
        {'sigla': 'ES', 'nome': 'Espírito Santo'},
        {'sigla': 'GO', 'nome': 'Goiás'},
        {'sigla': 'MA', 'nome': 'Maranhão'},
        {'sigla': 'MT', 'nome': 'Mato Grosso'},
        {'sigla': 'MS', 'nome': 'Mato Grosso do Sul'},
        {'sigla': 'MG', 'nome': 'Minas Gerais'},
        {'sigla': 'PA', 'nome': 'Pará'},
        {'sigla': 'PB', 'nome': 'Paraíba'},
        {'sigla': 'PR', 'nome': 'Paraná'},
        {'sigla': 'PE', 'nome': 'Pernambuco'},
        {'sigla': 'PI', 'nome': 'Piauí'},
        {'sigla': 'RJ', 'nome': 'Rio de Janeiro'},
        {'sigla': 'RN', 'nome': 'Rio Grande do Norte'},
        {'sigla': 'RS', 'nome': 'Rio Grande do Sul'},
        {'sigla': 'RO', 'nome': 'Rondônia'},
        {'sigla': 'RR', 'nome': 'Roraima'},
        {'sigla': 'SC', 'nome': 'Santa Catarina'},
        {'sigla': 'SP', 'nome': 'São Paulo'},
        {'sigla': 'SE', 'nome': 'Sergipe'},
        {'sigla': 'TO', 'nome': 'Tocantins'}
    ]

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando o script para popular as UFs...'))
        
        total_criadas = 0
        total_existentes = 0

        for uf_data in self.UFS_BRASIL:
            # get_or_create tenta buscar um objeto. Se não encontrar, ele cria um novo.
            # A variável 'created' será True se um novo objeto foi criado, e False caso contrário.
            obj, created = UF.objects.get_or_create(
                sigla=uf_data['sigla'],
                defaults={'nome': uf_data['nome']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'UF "{uf_data["sigla"]}" criada com sucesso.'))
                total_criadas += 1
            else:
                self.stdout.write(self.style.WARNING(f'UF "{uf_data["sigla"]}" já existe.'))
                total_existentes += 1
        
        self.stdout.write(self.style.SUCCESS('-----------------------------------------'))
        self.stdout.write(self.style.SUCCESS(f'Processo finalizado.'))
        self.stdout.write(self.style.SUCCESS(f'{total_criadas} UFs foram criadas.'))
        self.stdout.write(self.style.SUCCESS(f'{total_existentes} UFs já estavam no banco de dados.'))