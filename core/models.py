from django.db import models

class Cidade(models.Model):
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.cidade}, {self.uf}"

class Endereco(models.Model):
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    cep = models.CharField(max_length=8)
    bairro = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    ponto_de_referencia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade.cidade}"

class Abrigo(models.Model):
    nome = models.CharField(max_length=50)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class CRMV(models.Model):
    numero = models.CharField(max_length=20)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.numero}/{self.estado}"

class Veterinario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    senha_hash = models.CharField(max_length=255)
    crmv = models.OneToOneField(CRMV, on_delete=models.PROTECT)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome


class Especie(models.Model):
    nome_cientifico = models.CharField(max_length=50)
    nome_popular = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True, null=True)
    expectativa_de_vida = models.IntegerField()

    def __str__(self):
        return self.nome_cientifico

class Animal(models.Model):
    nome = models.CharField(max_length=50)
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT)
    abrigo = models.ForeignKey(Abrigo, on_delete=models.SET_NULL, blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('F', 'Fêmea')])

    def __str__(self):
        return f"{self.nome} ({self.especie.nome_cientifico}, {self.especie.raca})"

class TipoConsulta(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

class Item(models.Model):
    nome = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
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

    # Garante que um item só pode ser adicionado uma vez por atendimento
    class Meta:
      unique_together = ('item', 'atendimento')

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} em {self.atendimento}"

