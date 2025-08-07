import requests
from django.core.management.base import BaseCommand
from core.models import UF, Cidade

class Command(BaseCommand):
    help = 'Popula o banco de dados com as cidades do Brasil a partir da API do IBGE'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando o script para popular as Cidades...'))
        
        # Primeiro, garantir que todas as UFs estão no banco de dados.
        ufs_no_db = set(UF.objects.values_list('sigla', flat=True))
        if len(ufs_no_db) < 27:
            self.stdout.write(self.style.ERROR('ERRO: Por favor, popule as UFs primeiro rodando "python manage.py popular_ufs"'))
            return

        # URL da API de municípios do IBGE
        url_estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        
        try:
            response_estados = requests.get(url_estados)
            response_estados.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx
            estados = response_estados.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'ERRO ao buscar a lista de estados: {e}'))
            return

        total_criadas = 0
        total_existentes = 0

        for estado in sorted(estados, key=lambda x: x['sigla']):
            uf_sigla = estado['sigla']
            url_municipios = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_sigla}/municipios'
            
            self.stdout.write(f'Buscando cidades para o estado: {uf_sigla}')

            try:
                # Busca a instância da UF no banco de dados
                uf_obj = UF.objects.get(sigla=uf_sigla)
                
                response_municipios = requests.get(url_municipios)
                response_municipios.raise_for_status()
                municipios = response_municipios.json()

                for municipio in municipios:
                    nome_cidade = municipio['nome']
                    
                    # Usa get_or_create para evitar duplicatas
                    cidade_obj, created = Cidade.objects.get_or_create(
                        cidade=nome_cidade,
                        uf=uf_obj
                    )

                    if created:
                        total_criadas += 1
                    else:
                        total_existentes += 1

            except UF.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'UF com sigla "{uf_sigla}" não encontrada no banco de dados.'))
                continue
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'ERRO ao buscar municípios para {uf_sigla}: {e}'))
                continue
        
        self.stdout.write(self.style.SUCCESS('-----------------------------------------'))
        self.stdout.write(self.style.SUCCESS('Processo finalizado.'))
        self.stdout.write(self.style.SUCCESS(f'{total_criadas} cidades foram criadas.'))
        self.stdout.write(self.style.SUCCESS(f'{total_existentes} cidades já estavam no banco de dados.'))