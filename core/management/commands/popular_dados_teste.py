import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from core.models import (
    UF, Cidade, Endereco, CRMV, Especie, Abrigo, Animal, 
    TipoConsulta, Item, Veterinario, AtendimentoVeterinario
)

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para todas as tabelas (exceto UF e Cidade).'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando a população com dados de teste...'))
        
        fake = Faker('pt_BR')

        if not UF.objects.exists() or not Cidade.objects.exists():
            self.stdout.write(self.style.ERROR('ERRO: Popule as UFs e Cidades antes de rodar este script.'))
            return
        
        ufs = list(UF.objects.all())
        cidades = list(Cidade.objects.all())

        self.stdout.write('Criando Itens...')
        itens_criados = []
        for _ in range(10):
            item = Item.objects.create(
               nome=fake.word().capitalize() + ' ' + fake.word(),
               descricao=fake.sentence(nb_words=6),
               quantidade=random.randint(5, 50),
               preco_unitario=round(random.uniform(5.0, 150.0), 2),
               data_validade=fake.future_date(end_date="+2y")
            )
            itens_criados.append(item)
        self.stdout.write(self.style.SUCCESS('Itens criados.'))

        self.stdout.write('Criando Tipos de Consulta...')
        tipos_consulta = []
        consultas_base = ['Consulta de Rotina', 'Emergência', 'Vacinação', 'Cirurgia Eletiva', 'Acompanhamento Pós-operatório']
        for desc in consultas_base:
            tipo, _ = TipoConsulta.objects.get_or_create(descricao=desc)
            tipos_consulta.append(tipo)
        self.stdout.write(self.style.SUCCESS('Tipos de Consulta criados.'))

        self.stdout.write('Criando Espécies...')
        especies_criadas = []
        for _ in range(10):
            especie = Especie.objects.create(
               nome_cientifico=f"Canis familiaris var.{random.randint(1, 100)}",
               nome_popular=f"Cachorro {fake.word().capitalize()}",
               raca=fake.word().capitalize(),
               expectativa_de_vida=random.randint(10, 18)
            )
            especies_criadas.append(especie)
        self.stdout.write(self.style.SUCCESS('Espécies criadas.'))

        self.stdout.write('Criando Veterinários, Endereços e CRMVs...')
        veterinarios_criados = []
        for i in range(10):
            cidade_aleatoria = random.choice(cidades)
            endereco = Endereco.objects.create(
               cidade=cidade_aleatoria,
               # CORREÇÃO AQUI: Removemos o hífen e outros caracteres não numéricos
               cep=fake.postcode().replace('-', ''),
               bairro=fake.bairro(),
               logradouro=fake.street_name(),
               numero=str(random.randint(1, 2000))
            )
            
            uf_aleatoria = random.choice(ufs)
            crmv = CRMV.objects.create(
               numero=str(random.randint(1000, 9999)),
               estado=uf_aleatoria
            )

            veterinario = Veterinario.objects.create_user(
               email=f'vet{i}@anjosdarua.com',
               password='123',
               nome=fake.name(),
               cpf=fake.unique.cpf().replace('.','').replace('-',''),
               telefone=fake.msisdn()[:11],
               crmv=crmv,
               endereco=endereco
            )
            veterinarios_criados.append(veterinario)
        self.stdout.write(self.style.SUCCESS('Veterinários, Endereços e CRMVs criados.'))

        self.stdout.write('Criando Abrigos...')
        abrigos_criados = []
        for _ in range(10):
            cidade_aleatoria = random.choice(cidades)
            endereco_abrigo = Endereco.objects.create(
               cidade=cidade_aleatoria,
               # CORREÇÃO AQUI TAMBÉM:
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
        self.stdout.write(self.style.SUCCESS('Abrigos criados.'))

        self.stdout.write('Criando Animais...')
        animais_criados = []
        for _ in range(20):
            animal = Animal.objects.create(
               nome=fake.first_name(),
               especie=random.choice(especies_criadas),
               abrigo=random.choice(abrigos_criados),
               peso=round(random.uniform(1.0, 40.0), 2),
               idade=random.randint(1, 15),
               sexo=random.choice(['M', 'F'])
            )
            animais_criados.append(animal)
        self.stdout.write(self.style.SUCCESS('Animais criados.'))

        self.stdout.write('Criando Atendimentos...')
        for _ in range(15):
            atendimento = AtendimentoVeterinario.objects.create(
               animal=random.choice(animais_criados),
               veterinario=random.choice(veterinarios_criados),
               tipo_consulta=random.choice(tipos_consulta),
               data_do_atendimento=fake.date_time_this_year(),
               observacoes=fake.text(max_nb_chars=200)
            )
            itens_para_atendimento = random.sample(itens_criados, random.randint(1, 3))
            for item in itens_para_atendimento:
                atendimento.itens_utilizados.add(item, through_defaults={'quantidade': random.randint(1, 5)})
        self.stdout.write(self.style.SUCCESS('Atendimentos criados.'))

        self.stdout.write(self.style.SUCCESS('-----------------------------------------'))
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))