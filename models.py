from main import database



class Produto(database.Model):
    cdProduto = database.Column(database.Integer, primary_key=True)
    dsNome = database.Column(database.String, nullable=False)
    dsDescricao = database.Column(database.String,nullable=False)
    nrCodigo = database.Column(database.String, nullable=False)
    nrLarg = database.Column(database.Decimal, nullable=False)
    nrComp = database.Column(database.Decimal, nullable=False)
    nrAlt = database.Column(database.Decimal, nullable=False)
    cdStatus = database.Column(database.Integer, nullable=False, default=1)

class Cliente(database.Model):
    cdCliente = database.Column(database.Integer, primary_key=True)
    dsNome = database.Column(database.String,nullable=False)
    nrCnpj = database.Column(database.String, nullable=False)
    nrIe = database.Column(database.String, nullable=False)
    nrInscMun = database.Column(database.String, nullable=False)
    dsLogradouro = database.Column(database.String,nullable=False)
    nrNumero = database.Column(database.String, nullable=False)
    dsComplemento = database.Column(database.String,nullable=False)
    dsBairro = database.Column(database.String,nullable=False)
    dsCep = database.Column(database.String,nullable=False)
    dsUF = database.Column(database.String,nullable=False)
    dsCidade = database.Column(database.String)
    dsObs = database.Column(database.String,nullable=False)
    cdStatus = database.Column(database.Integer, nullable=False, default=1)

class Destinatario(database.Model):
    cdDestinatario = database.Column(database.Integer, primary_key=True)
    dsNome = database.Column(database.String,nullable=False)
    nrCnpj = database.Column(database.String, nullable=False)
    nrIe = database.Column(database.String, nullable=False)
    nrInscMun = database.Column(database.String, nullable=False)
    dsLogradouro = database.Column(database.String,nullable=False)
    nrNumero = database.Column(database.String, nullable=False)
    dsComplemento = database.Column(database.String,nullable=False)
    dsBairro = database.Column(database.String,nullable=False)
    dsCep = database.Column(database.String,nullable=False)
    dsUF = database.Column(database.String,nullable=False)
    dsCidade = database.Column(database.String)
    dsObs = database.Column(database.String,nullable=False)
    cdStatus = database.Column(database.Integer, nullable=False, default=1)

class Usuario(database.Model):
    cdUsuario = database.Column(database.Integer, primary_key=True)
    dsNome = database.Column(database.String, nullable=False)
    dsLogin = database.Column(database.Text, nullable=False)
    dsSenha = database.Column(database.DateTime, nullable=False)
    cdPerfil = database.Column(database.Integer,  nullable=False)

class Funcionario(database.Model):
    cdFuncionario = database.Column(database.Integer, primary_key=False)
    dsNomeEmpregado = database.Column(database.String, nullable=False)
    dsCpf = database.Column(database.String, nullable=False)
    dsEntrada = database.Column(database.DateTime, nullable=False)
    dsSaida = database.Column(database.DateTime, nullable=False)
    cdPerfil = database.Column(database.Integer,  nullable=False)
    dsFuncao = database.Column(database.String, nullable=False)
    dsEmpresa = database.Column(database.String, nullable=False)
    dsEscala = database.Column(database.String, nullable=False)
    nrCargaHoraria = database.Column(database.String, nullable=False)
    nrCargaHorariaMes = database.Column(database.String, nullable=False)
