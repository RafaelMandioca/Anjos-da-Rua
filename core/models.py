from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class CodigoAcesso(models.Model):
    codigo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilizado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.codigo)

class VeterinarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Veterinario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    crmv = models.OneToOneField('CRMV', on_delete=models.PROTECT, null=True, blank=True)
    endereco = models.ForeignKey('Endereco', on_delete=models.SET_NULL, null=True)
    codigo_acesso = models.OneToOneField(CodigoAcesso, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = VeterinarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    def __str__(self):
        return self.nome

# NOVO MODELO
class UF(models.Model):
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.sigla

class Cidade(models.Model):
    cidade = models.CharField(max_length=100)
    # CAMPO ALTERADO
    uf = models.ForeignKey(UF, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.cidade}, {self.uf.sigla}"

class Endereco(models.Model):
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    cep = models.CharField(max_length=8)
    bairro = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    ponto_de_referencia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}"

class Abrigo(models.Model):
    nome = models.CharField(max_length=50)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class CRMV(models.Model):
    numero = models.CharField(max_length=20)
    # CAMPO ALTERADO
    estado = models.ForeignKey(UF, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.numero}/{self.estado.sigla}"

class Especie(models.Model):
    nome_cientifico = models.CharField(max_length=50)
    nome_popular = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True, null=True)
    expectativa_de_vida = models.IntegerField()

    def __str__(self):
        return self.nome_cientifico

class Animal(models.Model):
    nome = models.CharField(max_length=50)
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, null=True, blank=True)
    abrigo = models.ForeignKey(Abrigo, on_delete=models.SET_NULL, blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('F', 'Fêmea')])

    def __str__(self):
        return f"{self.nome} ({self.especie.nome_cientifico if self.especie else 'N/A'}, {self.especie.raca if self.especie else 'N/A'})"

class TipoConsulta(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

class Item(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    data_validade = models.DateField()

    def __str__(self):
        return f"{self.nome}, ${self.preco_unitario}"

class AtendimentoVeterinario(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT)
    tipo_consulta = models.ForeignKey(TipoConsulta, on_delete=models.PROTECT)
    data_do_atendimento = models.DateTimeField()
    observacoes = models.TextField()
    
    itens_utilizados = models.ManyToManyField(
        Item,
        through='ItemHasAtendimentoVeterinario'
    )

    def __str__(self):
        return f"Atendimento para {self.animal.nome} em {self.data_do_atendimento.strftime('%d/%m/%Y')}"

class ItemHasAtendimentoVeterinario(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    atendimento = models.ForeignKey(AtendimentoVeterinario, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
      unique_together = ('item', 'atendimento')

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} em {self.atendimento}"