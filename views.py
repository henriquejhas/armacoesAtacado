from main import app, ref, firebase, bucket
from flask import Flask, Response
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db,auth, storage
from flask_wtf import CSRFProtect
import pyrebase
from formularios import FormularioUpload
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify, make_response
from config import config
from datetime import timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
import time
from PIL import Image

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
ALLOWED_EXTENSIONS2 = {'jpg', 'jpeg', 'png'}



@app.route('/painel/catalogo')
def painel_catalogo():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie:
        try:
            armacoes = []
            produtos = ref.child(f'estoques/{cookie['uid']}/produtos').get()
            for produto in produtos:
                armacao = produtos[produto]
                armacoes.append((produto, armacao))

            loja = ref.child('estoques').child(f"{cookie['uid']}").child('loja').get()

        except:
            return render_template('painel_catalogo.html', loja=loja, mensagem='Erro ao ler os dados do catálogo!')
        else:
            form = FormularioUpload()
            mensagem = request.args.get('mensagem')
            return render_template('painel_catalogo.html', loja=loja,armacoes=armacoes, mensagem=mensagem, form=form)
    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/catalogo/<string:nome>')
def catalogo(nome):
    global loja
    lojas = ref.child('lojas').get()
    if nome in lojas:
        chave = lojas[nome]

        try:
            armacoes = []
            produtos = ref.child(f'estoques/{chave}/produtos').get()
            for produto in produtos:
                armacao = produtos[produto]
                armacoes.append((produto, armacao))

            loja = ref.child('estoques').child(f"{chave}").child('loja').get()

        except:
            return render_template('catalogo.html', loja=loja, mensagem='Erro ao ler os dados do catálogo!')
        else:
            form = FormularioUpload()
            mensagem = request.args.get('mensagem')
            return render_template('catalogo.html', loja=loja,armacoes=armacoes, mensagem=mensagem, form=form, nome=nome)
    else:
        return render_template('catalogo_nao_encontrado.html',mensagem='Erro ao ler os dados do catálogo!')


@app.route('/historia', methods=['POST'])
def add_historia():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'sobre': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/sobre').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "historia"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/whatsapp', methods=['POST'])
def add_whatsapp():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'whatsapp': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/whatsapp').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "whatsapp"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/instagram', methods=['POST'])
def add_instagram():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'instagram': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/instagram').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "instagram"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/facebook', methods=['POST'])
def add_facebook():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'facebook': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/facebook').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "facebook"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/youtube', methods=['POST'])
def add_youtube():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'youtube': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/youtube').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "youtube"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/endereco', methods=['POST'])
def add_endereco():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'endereco': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/endereco').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "endereco"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/funcionamento', methods=['POST'])
def add_funcionamento():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'aberto': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/aberto').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "funcionamento"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/cor', methods=['POST'])
def add_cor():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'cor': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/cor').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "cor"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/fonte', methods=['POST'])
def add_fonte():
    cookie, mensagem = conferir_cookie()
    if cookie:
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'fonte': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie['uid']}/loja/fonte').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "fonte"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/logo', methods=['POST'])
def add_logo():
    global url
    cookie, mensagem = conferir_cookie()
    if cookie:
        try:
            token = session['usuario_logado']
            form = FormularioUpload()
            if form.validate_on_submit():
                file = form.arquivo.data
                if file:
                    if allowed_file_png(file.filename):
                        imagem = Image.open(file)
                        imagem = imagem.resize((600, 200))
                        tipo = file.filename.rsplit('.', 1)[1].lower()
                        if tipo in ALLOWED_EXTENSIONS:
                            imagem.save('somepic.jpg')
                            timestamp = time.time()
                            local = f'estoques/{cookie['uid']}/{timestamp}.jpg'
                            blob = bucket.blob(local)
                            blob.upload_from_filename('somepic.jpg', content_type='image/jpg')
                            url = firebase.storage().child(local).get_url(token)
                        elif tipo in 'png':
                            imagem.save('somepic.png')
                            timestamp = time.time()
                            local = f'estoques/{cookie['uid']}/{timestamp}.png'
                            blob = bucket.blob(local)
                            blob.upload_from_filename('somepic.png', content_type='image/png')
                            url = firebase.storage().child(local).get_url(token)
                    else:
                        return redirect(url_for('painel_catalogo', mensagem="Formato da imagem inválido!"))
                else:
                    return redirect(url_for('painel_catalogo', mensagem="Imagem não selecionada!"))
            else:
                return redirect(url_for('painel_catalogo', mensagem="Formulário inválido!"))
        except:
            return redirect(url_for('painel_catalogo', mensagem="Tivemos um problema com a imagem, fale com o suporte!"))
        else:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'logo': url})
            return redirect(url_for('painel_catalogo', mensagem="Imagem salva com sucesso!!"))
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/banner', methods=['POST'])
def add_banner():
    cookie, mensagem = conferir_cookie()
    if cookie:
        try:
            token = session['usuario_logado']
            form = FormularioUpload()
            if form.validate_on_submit():
                file = form.arquivo.data
                if file:
                    if allowed_file_jpg(file.filename):
                        imagem = Image.open(file)
                        print("ok1")
                        imagem = imagem.resize((1000, 400))
                        print("ok2")
                        imagem.save('somepic.jpg')
                        print("ok3")
                        timestamp = time.time()
                        local = f'estoques/{cookie['uid']}/{timestamp}.jpg'
                        blob = bucket.blob(local)
                        blob.upload_from_filename('somepic.jpg', content_type='image/jpg')
                        url = firebase.storage().child(local).get_url(token)
                    else:
                        return redirect(url_for('painel_catalogo', mensagem="Formato da imagem inválido!"))
                else:
                    return redirect(url_for('painel_catalogo', mensagem="Imagem não selecionada!"))
            else:
                return redirect(url_for('painel_catalogo', mensagem="Formulário inválido!"))
        except:
            return redirect(url_for('painel_catalogo', mensagem="Tivemos um problema com a imagem, fale com o suporte!"))
        else:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'banner': url})
            return redirect(url_for('painel_catalogo', mensagem="Imagem salva com sucesso!!"))
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/foto', methods=['POST'])
def add_foto():
    cookie, mensagem = conferir_cookie()
    if cookie:
        try:
            token = session['usuario_logado']
            form = FormularioUpload()
            if form.validate_on_submit():
                file = form.arquivo.data
                if file:
                    if allowed_file_jpg(file.filename):
                        imagem = Image.open(file)
                        imagem = imagem.resize((700, 300))
                        imagem.save('somepic.jpg')
                        timestamp = time.time()
                        local = f'estoques/{cookie['uid']}/{timestamp}.jpg'
                        blob = bucket.blob(local)
                        blob.upload_from_filename('somepic.jpg', content_type='image/jpg')
                        url = firebase.storage().child(local).get_url(token)
                    else:
                        return redirect(url_for('painel_catalogo', mensagem="Formato da imagem inválido!"))
                else:
                    return redirect(url_for('painel_catalogo', mensagem="Imagem não selecionada!"))
            else:
                return redirect(url_for('painel_catalogo', mensagem="Formulário inválido!"))
        except:
            return redirect(url_for('painel_catalogo', mensagem="Tivemos um problema com a imagem, fale com o suporte!"))
        else:
            ref.child(f'estoques/{cookie['uid']}/loja').update({'foto': url})
            return redirect(url_for('painel_catalogo', mensagem="Imagem salva com sucesso!!"))
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/carrinho', methods=['POST'])
def carrinho():
    print('passou aqui1')
    global loja
    lojas = ref.child('lojas').get()
    dadoJson = request.get_json()
    nome = dadoJson['loja']
    print('passou aqui1')
    if nome in lojas:
        print('passou aqui2')
        chave = lojas[nome]
        carrinho = dadoJson['carrinho']
        print(carrinho)
        try:

            res = ref.child(f'estoques/{chave}/pedidos').push(dadoJson)
        except:
            return jsonify({'mensagem': False})
        else:
            if res in ref.child(f'estoques/{chave}/pedidos').get():
                return jsonify(dadoJson)
            else:
                return jsonify({'mensagem': False})
    else:
        print('passou aqui3')
        return jsonify({'mensagem': False})


def conferir_cookie():
    global cookie
    cookie = False
    try:
        if 'usuario_logado' in session:
            token = session['usuario_logado']
            cookie = auth.verify_session_cookie(token, clock_skew_seconds=5)
        else:
            return 'Usuário não logado!'

    except auth.ExpiredSessionCookieError:

        return cookie, 'O cookie de sessão expirou'
    except auth.RevokedSessionCookieError:

        return cookie, 'O cookie foi revogado'
    except auth.InvalidSessionCookieError:

        return cookie, 'Cookie de sessão inválido'
    except auth.CertificateFetchError:

        return cookie, 'erro ao buscar os certificados de chave pública'
    except auth.UserDisabledError:

        return cookie, 'Registro do usuário desabilitado'
    except ValueError:

        return cookie, 'Cookie de sessão ilegal'
    except Exception as e:
        return cookie, f"Ocorreu um erro: {e}"
    else:
        return cookie, ''


def allowed_file_jpg(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_png(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2






