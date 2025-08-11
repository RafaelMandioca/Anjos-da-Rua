import random
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from core.models import (
    UF, Cidade, Endereco, CRMV, Especie, Abrigo, Animal, 
    TipoConsulta, Item, Veterinario, AtendimentoVeterinario, StatusAtendimento, CodigoAcesso
)

class Command(BaseCommand):
    help = 'Executa todos os scripts para popular o banco de dados com dados iniciais e de teste.'

    def popular_ufs(self):
        self.stdout.write(self.style.SUCCESS('--- Iniciando: Populando UFs ---'))
        UFS_BRASIL = [
            {'sigla': 'AC', 'nome': 'Acre'}, {'sigla': 'AL', 'nome': 'Alagoas'},
            {'sigla': 'AP', 'nome': 'Amapá'}, {'sigla': 'AM', 'nome': 'Amazonas'},
            {'sigla': 'BA', 'nome': 'Bahia'}, {'sigla': 'CE', 'nome': 'Ceará'},
            {'sigla': 'DF', 'nome': 'Distrito Federal'}, {'sigla': 'ES', 'nome': 'Espírito Santo'},
            {'sigla': 'GO', 'nome': 'Goiás'}, {'sigla': 'MA', 'nome': 'Maranhão'},
            {'sigla': 'MT', 'nome': 'Mato Grosso'}, {'sigla': 'MS', 'nome': 'Mato Grosso do Sul'},
            {'sigla': 'MG', 'nome': 'Minas Gerais'}, {'sigla': 'PA', 'nome': 'Pará'},
            {'sigla': 'PB', 'nome': 'Paraíba'}, {'sigla': 'PR', 'nome': 'Paraná'},
            {'sigla': 'PE', 'nome': 'Pernambuco'}, {'sigla': 'PI', 'nome': 'Piauí'},
            {'sigla': 'RJ', 'nome': 'Rio de Janeiro'}, {'sigla': 'RN', 'nome': 'Rio Grande do Norte'},
            {'sigla': 'RS', 'nome': 'Rio Grande do Sul'}, {'sigla': 'RO', 'nome': 'Rondônia'},
            {'sigla': 'RR', 'nome': 'Roraima'}, {'sigla': 'SC', 'nome': 'Santa Catarina'},
            {'sigla': 'SP', 'nome': 'São Paulo'}, {'sigla': 'SE', 'nome': 'Sergipe'},
            {'sigla': 'TO', 'nome': 'Tocantins'}
        ]
        for uf_data in UFS_BRASIL:
            UF.objects.get_or_create(sigla=uf_data['sigla'], defaults={'nome': uf_data['nome']})
        self.stdout.write(self.style.SUCCESS('UFs populadas com sucesso.'))

    def popular_cidades(self):
        self.stdout.write(self.style.SUCCESS('\n--- Iniciando: Populando Cidades via API do IBGE ---'))
        if UF.objects.count() < 27:
            self.stdout.write(self.style.ERROR('ERRO: UFs não foram populadas. Rode o passo anterior primeiro.'))
            return
        
        url_estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        try:
            response_estados = requests.get(url_estados)
            response_estados.raise_for_status()
            estados = response_estados.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'ERRO ao buscar a lista de estados: {e}'))
            return

        for estado in sorted(estados, key=lambda x: x['sigla']):
            uf_sigla = estado['sigla']
            url_municipios = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_sigla}/municipios'
            self.stdout.write(f'Buscando cidades para o estado: {uf_sigla}...')
            try:
                uf_obj = UF.objects.get(sigla=uf_sigla)
                response_municipios = requests.get(url_municipios)
                response_municipios.raise_for_status()
                municipios = response_municipios.json()
                for municipio in municipios:
                    Cidade.objects.get_or_create(cidade=municipio['nome'], uf=uf_obj)
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'ERRO ao buscar municípios para {uf_sigla}: {e}'))
                continue
        self.stdout.write(self.style.SUCCESS('Cidades populadas com sucesso.'))
        
    def popular_dados_teste(self):
        self.stdout.write(self.style.SUCCESS('\n--- Iniciando: Populando com Dados de Teste ---'))
        fake = Faker('pt_BR')

        # Popula Status de Atendimento
        status_nao_concluido, _ = StatusAtendimento.objects.get_or_create(descricao='Não Concluído')
        status_concluido, _ = StatusAtendimento.objects.get_or_create(descricao='Concluído')
        self.stdout.write('Status de Atendimento criados.')

        # Cria Códigos de Acesso
        for _ in range(15):  # Criar alguns códigos extras
            CodigoAcesso.objects.create()
        self.stdout.write('Códigos de Acesso criados.')

        ufs = list(UF.objects.all())
        cidades = list(Cidade.objects.all())

        # Cria Itens
        itens_criados = []
        for _ in range(20):
            item = Item.objects.create(
               nome=fake.word().capitalize() + ' ' + fake.word(),
               descricao=fake.sentence(nb_words=6),
               quantidade=random.randint(50, 200),
               preco_unitario=round(random.uniform(5.0, 150.0), 2),
               data_validade=fake.future_date(end_date="+2y")
            )
            itens_criados.append(item)
        self.stdout.write('Itens de estoque criados.')

        # Cria Tipos de Consulta
        tipos_consulta = []
        consultas_base = ['Consulta de Rotina', 'Emergência', 'Vacinação', 'Cirurgia Eletiva', 'Acompanhamento Pós-operatório']
        for desc in consultas_base:
            tipo, _ = TipoConsulta.objects.get_or_create(descricao=desc)
            tipos_consulta.append(tipo)
        self.stdout.write('Tipos de Consulta criados.')

        # Cria Espécies
        especies_criadas = []
        for _ in range(15):
            especie = Especie.objects.create(
               nome_cientifico=f"Genus species var.{random.randint(1, 100)}",
               nome_popular=random.choice(['Cachorro', 'Gato', 'Pássaro', 'Hamster']),
               raca=fake.word().capitalize(),
               expectativa_de_vida=random.randint(8, 20)
            )
            especies_criadas.append(especie)
        self.stdout.write('Espécies criadas.')

        # Cria Veterinários
        veterinarios_criados = []
        codigos_acesso_disponiveis = list(CodigoAcesso.objects.filter(utilizado=False))
        
        # Cria um Superusuário (Admin)
        admin_user = Veterinario.objects.create_superuser(
            email='admin@anjosdarua.com',
            password='admin',
            nome='Administrador Geral',
            cpf=fake.unique.cpf().replace('.','').replace('-','')
        )
        self.stdout.write('Superusuário "admin@anjosdarua.com" (senha: admin) criado.')

        for i in range(10):
            endereco = Endereco.objects.create(
               cidade=random.choice(cidades),
               cep=fake.postcode().replace('-', ''),
               bairro=fake.bairro(),
               logradouro=fake.street_name(),
               numero=str(random.randint(1, 2000))
            )
            crmv = CRMV.objects.create(
               numero=str(random.randint(10000, 99999)),
               estado=random.choice(ufs)
            )
            codigo_acesso = codigos_acesso_disponiveis.pop()
            veterinario = Veterinario.objects.create_user(
               email=f'vet{i}@anjosdarua.com',
               password='123',
               nome=fake.name(),
               cpf=fake.unique.cpf().replace('.','').replace('-',''),
               telefone=fake.msisdn()[:11],
               crmv=crmv,
               endereco=endereco,
               codigo_acesso=codigo_acesso
            )
            codigo_acesso.utilizado = True
            codigo_acesso.save()
            veterinarios_criados.append(veterinario)
        self.stdout.write('Veterinários, Endereços e CRMVs criados.')

        # Cria Abrigos
        abrigos_criados = []
        for _ in range(5):
            endereco_abrigo = Endereco.objects.create(
               cidade=random.choice(cidades),
               cep=fake.postcode().replace('-', ''),
               bairro=fake.bairro(),
               logradouro=fake.street_name(),
               numero=str(random.randint(1, 2000))
            )
            abrigo = Abrigo.objects.create(
               nome=f"Abrigo {fake.company()}",
               endereco=endereco_abrigo
            )
            abrigos_criados.append(abrigo)
        self.stdout.write('Abrigos criados.')

        # Cria Animais com nomes mais realistas
        nomes_animais = ['Max', 'Bella', 'Charlie', 'Lucy', 'Cooper', 'Daisy', 'Milo', 'Luna', 'Rocky', 'Zoe', 'Buddy', 'Lola', 'Jack', 'Sadie', 'Toby', 'Molly', 'Cody', 'Bailey', 'Leo', 'Maggie']
        animais_criados = []
        for _ in range(30):
            animal = Animal.objects.create(
               nome=random.choice(nomes_animais),
               especie=random.choice(especies_criadas),
               abrigo=random.choice(abrigos_criados),
               peso=round(random.uniform(1.0, 40.0), 2),
               idade=random.randint(1, 15),
               sexo=random.choice(['M', 'F'])
            )
            animais_criados.append(animal)
        self.stdout.write('Animais criados.')

        # Cria Atendimentos
        for _ in range(25):
            atendimento = AtendimentoVeterinario.objects.create(
               animal=random.choice(animais_criados),
               veterinario=random.choice(veterinarios_criados),
               tipo_consulta=random.choice(tipos_consulta),
               status=status_nao_concluido, # Todos começam como não concluídos
               data_do_atendimento=fake.date_time_this_year(),
               observacoes=fake.text(max_nb_chars=200)
            )
            itens_para_atendimento = random.sample(itens_criados, random.randint(1, 3))
            for item in itens_para_atendimento:
                atendimento.itens_utilizados.add(item, through_defaults={'quantidade': random.randint(1, 5)})
        self.stdout.write('Atendimentos criados.')

    @transaction.atomic
    def handle(self, *args, **options):
        self.popular_ufs()
        self.popular_cidades()
        self.popular_dados_teste()
        self.stdout.write(self.style.SUCCESS('\n--- Processo Finalizado ---'))
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))