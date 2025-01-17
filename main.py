import os

from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db, auth, exceptions, storage
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
import pyrebase
from formularios import FormularioUsuario, FormularioCadastro
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from config import config
from datetime import timedelta
import datetime
from flask_bcrypt import generate_password_hash
import requests
import json

#from flask_sslify import SSLify

if not firebase_admin._apps:
    cred = credentials.Certificate('./ServiceAccountKey.json')
    default_app = firebase_admin.initialize_app(cred, {
        "databaseURL": "https://estoque-armacoes-default-rtdb.firebaseio.com/",
        "storageBucket": "estoque-armacoes.appspot.com"
    })


firebase = pyrebase.initialize_app(config)

bucket = storage.bucket()

ref = db.reference('/')

app = Flask(__name__)

#sslify = SSLify(app)

CORS(app)
app.config.from_pyfile('config.py')
app.config['CSRF_SESSION_TIMEOUT'] = 3600 * 10
csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    print('erro csrf', e)
    return render_template('errocsrf.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

@app.route('/')
def index():
    form = FormularioUsuario()
    mensagem = request.args.get('mensagem')
    return render_template('index.html', form=form, mensagem=mensagem)


@app.route('/autenticar', methods=['POST', 'GET'])
def autenticar():
    global email, senha
    if request.method == "GET":
        return redirect(url_for('index', mensagem='Caminho não autorizado!'))
    elif request.method == 'POST':
        form = FormularioUsuario()
        email = form.email.data
        senha = form.senha.data

    try:

        user = firebase.auth().sign_in_with_email_and_password(email, senha)
        print("assinou")
        usuario = auth.get_user(user["localId"])
        if usuario.email_verified:
            print("verificou")
            session['usuario_logado'] = auth.create_session_cookie(user["idToken"], timedelta(minutes=600))
            print(session['usuario_logado'])
            return redirect(url_for('dashboard'))
        else:
            session['usuario_logado'] = None
            firebase.auth().send_email_verification(user["idToken"])
            return redirect(url_for('index', mensagem="Confirme sua conta clicando no link enviado para o seu email!"))



    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        mensagem = ''

        if error == "INVALID_LOGIN_CREDENTIALS":
            mensagem = 'Email ou senha inválido!'
        else:
            print(e)
        return redirect(url_for('index', mensagem=mensagem))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.route('/sair')
def logout():
    mensagem = request.args.get('mensagem')
    if not mensagem:
        mensagem = 'Sessão encerrada pelo usuário!'
    session['usuario_logado'] = None
    return redirect(url_for('index', mensagem=mensagem))


@app.route('/cadastro')
def cadastro():
    form = FormularioCadastro()

    return render_template('cadastro.html', form=form)


@app.route('/cadastrar', methods=['POST', "GET"])
def cadastrar():
    if request.method == "GET":
        return redirect(url_for('index', mensagem='Caminho não autorizado!'))
    elif request.method == 'POST':

        form = FormularioCadastro(request.form)
        if form.validate_on_submit():

            data_atual = datetime.date.today()
            data = data_atual.strftime("%d/%m/%Y")
            validade = data_atual + datetime.timedelta(days=15)
            validade = validade.strftime("%d/%m/%Y")

            nome = (form.nome.data).strip()
            loja = (form.loja.data).strip()
            endereco = (form.endereco.data).strip()
            cep = (form.cep.data).strip()
            cnpj = (form.cnpj.data).strip()
            celular = (form.celular.data).strip()
            email = (form.email.data).strip()
            senha = (form.senha.data).strip()
            senha2 = (form.senha2.data).strip()

            if loja.lower().replace(" ", "") in ref.child('lojas').get():
                return render_template('cadastro.html', form=form, mensagem='O nome da loja já está em uso!')

            if senha == senha2:
                try:
                    usuario = auth.create_user(email=email, password=senha)
                except auth.EmailAlreadyExistsError:
                    return render_template('cadastro.html', form=form, mensagem='O email já está em uso!')
                except Exception as e:
                    mensagem = ''
                    print(str(e))
                    if 'Invalid password string' in str(e):
                        mensagem = 'A senha deve ter pelo menos 6 caracteres'

                    return render_template('cadastro.html', form=form, mensagem=mensagem)
                else:

                    chave = ref.child('cadastros').push({
                        'dados': {
                            'nome': nome,
                            'loja': loja,
                            'endereco': endereco,
                            'cep': cep,
                            'cnpj': cnpj,
                            'celular': celular,
                            'email': email,
                            'id': generate_password_hash(usuario.uid).decode('utf-8'),
                            'plano':{
                                'ativo': True,
                                'data': data,
                                'pago': True,
                                'tipo': 'teste',
                                'validade': validade,
                                'valor': 0.0
                            }
                        }
                    })

                    ref.child('estoques').update({
                        f'{usuario.uid}': {
                            "cadastro": generate_password_hash(chave.key).decode('utf-8'),
                            'loja': {
                                "aberto": "Segunda a sexta das 8h às 18h. Sábado das 8h às 12h",
                                "banner": "https://firebasestorage.googleapis.com/v0/b/estoque-armacoes.appspot.com/o/bannersite.jpg?alt=media&token=6cb77f95-dd47-4790-b0fd-c992385ab1c7",
                                "cep": cep,
                                "cor": "009c99",
                                "endereco": "Rua alexandrino da Silva 407 ",
                                "facebook": "https://www.facebook.com/profile.php?id=61563400382967",
                                "fonte": "ffffff",
                                "foto": "https://firebasestorage.googleapis.com/v0/b/estoque-armacoes.appspot.com/o/foto.jpg?alt=media&token=228fff58-7a5c-4734-8c71-73b274b9f55d",
                                "instagram": " https://www.instagram.com/armacaoatacado_/",
                                "logo": "https://firebasestorage.googleapis.com/v0/b/estoque-armacoes.appspot.com/o/armaccaoatacado.png?alt=media&token=78708bf7-211f-40a2-8b25-4b53b931361b",
                                "minimo": 100,
                                "nomeLoja": loja.lower().replace(" ", ""),
                                "sobre": "Armação Atacado é uma loja online especializada em armações de óculos no atacado, com foco em oferecer produtos de alta qualidade a preços competitivos. Estamos no mercado há 2 anos, construindo uma reputação de confiança e excelência no atendimento. Nossa missão é Empoderar os nossos clientes com uma seleção diversificada de armações de óculos de alta qualidade, garantindo um atendimento personalizado e preços imbatíveis no atacado.",
                                "whatsapp": "82987333558",
                                "youtube": ""
                            }
                        }

                    })

                    ref.child('lojas').update({f'{loja.lower().replace(" ", "")}':usuario.uid})

                    if usuario.uid in ref.child('estoques').get() and chave.key in ref.child('cadastros').get():
                        user = firebase.auth().sign_in_with_email_and_password(email, senha)

                        firebase.auth().send_email_verification(user["idToken"])
                        session['usuario_logado'] = None
                        return redirect(url_for('confirmacao', nome=nome.split()[0]))
                    else:
                        return render_template('cadastro.html', form=form,
                                               mensagem='Algo deu errado ao conferir seus dados, entre em contato com o suporte!')

            else:
                return render_template('cadastro.html', form=form, mensagem='A senha de confirmação não está igual!')
        else:
            mensagem = ''
            for field, errors in form.errors.items():
                for error in errors:
                    mensagem = f'{field}: inválido!'
            return render_template('cadastro.html', form=form, mensagem=mensagem)


@app.route('/confirmacao')
def confirmacao():
    nome = request.args.get('nome')
    return render_template('confirmacao.html', nome=nome)


from crud import *

from views import *


if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/jhas.armacaoatacado.com/fullchain.pem', '/etc/letsencrypt/live/jhas.armacaoatacado.com/privkey.pem')
    #app.run(ssl_context=context, host='0.0.0.0')
    app.run(host='0.0.0.0')