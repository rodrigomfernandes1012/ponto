from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class FormCriarConta(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormProduto(FlaskForm):
    cdCodigo = StringField('Código do Produto', validators=[DataRequired()])
    dsNome = StringField('Nome do Produto', validators=[DataRequired()])
    dsDescricao = StringField('Descrição do Produto', validators=[DataRequired()])
    nrCodigo = StringField('Código da Loja', validators=[DataRequired()])
    nrLarg = StringField('Largura do Produto', validators=[DataRequired()])
    nrComp = StringField('Comprimento do Produto', validators=[DataRequired()])
    nrAlt = StringField('Altura do Produto', validators=[DataRequired()])
    cdStatus = StringField('Status do Produto', validators=[DataRequired()])
    botao_submit_cadastrar = SubmitField('Salvar')
    botao_submit_alterar = SubmitField('Alterar')
    botao_submit_excluir = SubmitField('Excluir')

class FormCliente(FlaskForm):
    cdCliente = StringField('ID', validators=[DataRequired()])
    dsNome = StringField('Cliente', validators=[DataRequired()])
    nrCnpj = StringField('CNPJ', validators=[DataRequired()])
    nrIe = StringField('IE', validators=[DataRequired()])
    nrInscMun = StringField('Insc. Mun.', validators=[DataRequired()])
    dsLogradouro = StringField('Logradouro', validators=[DataRequired()])
    nrNumero = StringField('Num.', validators=[DataRequired()])
    dsComplemento = StringField('Complemento', validators=[DataRequired()])
    dsBairro = StringField('Bairro', validators=[DataRequired()])
    dsCep = StringField('CEP', validators=[DataRequired()])
    dsUF = StringField('UF', validators=[DataRequired()])
    dsCidade = StringField('Cidade', validators=[DataRequired()])
    dsObs = StringField('Obs', validators=[DataRequired()])
    cdStatus = StringField('Status', validators=[DataRequired()])
    botao_submit_cadastrar = SubmitField('Salvar')
    botao_submit_alterar = SubmitField('Alterar')
    botao_submit_excluir = SubmitField('Excluir')

class FormDestinatario(FlaskForm):
    cdDestinatario = StringField('ID', validators=[DataRequired()])
    dsNome = StringField('Cliente', validators=[DataRequired()])
    nrCnpj = StringField('CNPJ', validators=[DataRequired()])
    nrIe = StringField('IE', validators=[DataRequired()])
    nrInscMun = StringField('Insc. Mun.', validators=[DataRequired()])
    dsLogradouro = StringField('Logradouro', validators=[DataRequired()])
    nrNumero = StringField('Num.', validators=[DataRequired()])
    dsComplemento = StringField('Complemento', validators=[DataRequired()])
    dsBairro = StringField('Bairro', validators=[DataRequired()])
    dsCep = StringField('CEP', validators=[DataRequired()])
    dsUF = StringField('UF', validators=[DataRequired()])
    dsCidade = StringField('Cidade', validators=[DataRequired()])
    dsObs = StringField('Obs', validators=[DataRequired()])
    cdStatus = StringField('Status', validators=[DataRequired()])
    botao_submit_cadastrar = SubmitField('Salvar')
    botao_submit_alterar = SubmitField('Alterar')
    botao_submit_excluir = SubmitField('Excluir')


class FormUsuario(FlaskForm):
    cdUsuario = StringField('ID', validators=[DataRequired()])
    dsNome = StringField('Nome', validators=[DataRequired()])
    dsLogin = StringField('Login', validators=[DataRequired()])
    dsSenha = StringField('Senha', validators=[DataRequired()])
    cdPerfil = StringField('Perfil', validators=[DataRequired()])
    botao_submit_cadastrar = SubmitField('Salvar')
    botao_submit_alterar = SubmitField('Alterar')
    botao_submit_excluir = SubmitField('Excluir')

class FuncionarioForm(FlaskForm):
    cdFuncionario = StringField('ID', validators=[DataRequired()])
    dsNomeEmpregado = StringField('Nome', validators=[DataRequired()])
    dsCpf = StringField('Cpf', validators=[DataRequired()])
    dsFuncao  = StringField('Funcao', validators=[DataRequired()])
    dsEmpresa  = StringField('Empresa', validators=[DataRequired()])
    dsEntrada = StringField('Entrada', validators=[DataRequired()])
    dsSaida = StringField('Saida', validators=[DataRequired()])
    cdPerfil = StringField('Perfil', validators=[DataRequired()])
    dsEscala  = StringField('Escala', validators=[DataRequired()])
    nrCargaHoraria  = StringField('Carga Horária Semana', validators=[DataRequired()])
    nrCargaHorariaMes  = StringField('Carga Horária Mês', validators=[DataRequired()])
    #botao_submit_cadastrar = SubmitField('Salvar')
    botao_submit_importar = SubmitField('Importar')
    botao_submit_alterar = SubmitField('Salvar')
    botao_submit_excluir = SubmitField('Excluir')
