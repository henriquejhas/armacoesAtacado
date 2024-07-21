from flask_wtf import FlaskForm
from wtforms import (StringField, validators,SubmitField,
                     PasswordField, EmailField, TextAreaField, IntegerField, SelectField,FileField)

class FormularioUsuario(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.length(min=1, max=100)])
    login = SubmitField('Login')

class FormularioCadastro(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.length(min=1, max=40)])
    loja = StringField('Loja', [validators.DataRequired(), validators.length(min=1, max=20)])
    endereco = StringField('Endereço', [validators.DataRequired(), validators.length(min=1, max=100)])
    cep = StringField('CEP', [validators.DataRequired(), validators.length(min=8, max=9)])
    cnpj = StringField('CPF/CNPJ', [validators.DataRequired(), validators.length(min=14, max=18)])
    celular = StringField('Celular', [validators.DataRequired(), validators.length(min=11, max=15, message="O número de celular deve ter 11 dígitos!")])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.length(min=1, max=100)])
    senha2 = PasswordField('Confirmar Senha', [validators.DataRequired(), validators.length(min=1, max=100)])
    cadastrar = SubmitField('Cadasstrar')

class FormularioCadastro2(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.length(min=1, max=40)])
    loja = StringField('Loja', [validators.DataRequired(), validators.length(min=1, max=20)])
    endereco = StringField('Endereço', [validators.DataRequired(), validators.length(min=1, max=100)])
    cep = StringField('CEP', [validators.DataRequired(), validators.length(min=8, max=9)])
    cnpj = StringField('CPF/CNPJ', [validators.DataRequired(), validators.length(min=14, max=18)])
    celular = StringField('Celular', [validators.DataRequired(), validators.length(min=11, max=14, message="O número de celular deve ter 11 dígitos!")])


class FormularioAdicionar(FlaskForm):
    codigo = StringField('Código', [validators.DataRequired(), validators.length(min=1, max=30)])
    dimensoes = StringField('Dimensoes', [validators.DataRequired(), validators.length(min=1, max=13)])
    preco = StringField('Preço', [validators.DataRequired(), validators.length(min=1, max=7)])
    descricao = TextAreaField('Descrição', [validators.DataRequired(), validators.length(min=1, max=105)])
    '''c1 = IntegerField('C1', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c2 = IntegerField('C2', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c3 = IntegerField('C3', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c4 = IntegerField('C4', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c5 = IntegerField('C5', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c6 = IntegerField('C6', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c7 = IntegerField('C7', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c8 = IntegerField('C8', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c9 = IntegerField('C9', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    c10 = IntegerField('C10', [validators.DataRequired(), validators.NumberRange(min=0, max=1000)])'''
    adicionar = SubmitField('Adicionar')


class FormularioPesquisar(FlaskForm):
    busca = StringField('Pesquisa', [validators.DataRequired(), validators.length(min=1, max=50)])

class FormularioFacebook(FlaskForm):
    facebook = StringField('Link Facebook', [validators.DataRequired(), validators.length(min=1, max=100)])

class FormularioUpload(FlaskForm):
    arquivo = FileField('Selecione um arquivo', validators=[validators.DataRequired()])
    enviar = SubmitField('Enviar')


