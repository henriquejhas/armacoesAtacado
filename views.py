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
        if nome == '0':
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
                    return render_template('catalogo.html', loja=loja, mensagem='Erro ao ler os dados do catálogo!')
                else:
                    form = FormularioUpload()
                    mensagem = request.args.get('mensagem')
                    return render_template('catalogo.html', loja=loja, armacoes=armacoes, mensagem=mensagem, form=form,
                                           nome=nome)


            else:
                session['usuario_logado'] = None
                return redirect(url_for('logout', mensagem=mensagem))
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

    global loja, res
    dadoJson = request.get_json()
    lojas = ref.child('lojas').get()
    nome = dadoJson['loja']

    if nome in lojas:
        chave = lojas[nome]

        try:
            resNumero = ref.child(f'estoques/{chave}/pedidos').child('contador').get()
            if resNumero != None:
                ref.child(f'estoques/{chave}/pedidos').update({'contador': (resNumero + 1)})
                dadoJson['numero'] = ('0' * (5 - len(str((resNumero + 1))))) + str((resNumero + 1))
                dadoJson['ativo'] = True
                res = ref.child(f'estoques/{chave}/pedidos').push(dadoJson)
            else:
                resNumero = 0
                ref.child(f'estoques/{chave}/pedidos').update({'contador': 1})
                dadoJson['numero'] = ('0' * (5 - len(str(1)))) + str(1)
                dadoJson['ativo'] = True
                res = ref.child(f'estoques/{chave}/pedidos').push(dadoJson)

        except Exception as erro:
            print(erro)
            return jsonify({'mensagem': False,'erro': str(erro)})
        else:
            if res.key in ref.child(f'estoques/{chave}/pedidos').get():
                return jsonify({'mensagem': True, 'numero': dadoJson['numero']})
            else:
                return jsonify({'mensagem': False,'erro': '1'})
    else:
        return jsonify({'mensagem': False,'erro': '2'})


@app.route('/pedidos', methods=['POST', 'GET'])
def pedidos():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie:

        if request.method == 'GET':
            mensagem = request.args.get('mensagem')
            try:
                listaPedidos = []
                pedidos = ref.child(f'estoques/{cookie['uid']}/pedidos').get()
            except:
                return render_template('pedidos.html', pedidos=[], mensagem='Erro ao ler os pedidos!')

            else:
                for chave in pedidos:
                    if chave != 'contador':
                        pedido = pedidos[chave]
                        listaPedidos.append((chave, pedido))

                return render_template('pedidos.html', pedidos=listaPedidos, mensagem=mensagem)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/visualizar/<string:chave>', methods=['GET', 'POST'])
def visualizar(chave):
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie:

        if request.method == 'GET':
            try:
                pedido = ref.child(f'estoques/{cookie['uid']}/pedidos').child(chave).get()
                lista = ref.child(f'estoques/{cookie['uid']}/produtos').get()
                produtos = []
                for produto in lista:
                    produtos.append(lista[produto]['codigo'])
            except:
                return render_template('visualizarPedido.html', pedido=[], mensagem='Erro ao ler os pedidos!')

            else:
                return render_template('visualizarPedido.html', pedido=pedido, chave=chave, produtos=produtos)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/carregar-codigos/', methods=['GET', 'POST'])
def carregar_codigos():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie:

        if request.method == 'GET':
            try:
                lista = ref.child(f'estoques/{cookie['uid']}/produtos').get()
                produtos = []
                for produto in lista:
                    produtos.append(lista[produto]['codigo'])
            except:
                return jsonify({'chave': False})

            else:
                return jsonify(produtos)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/carregar/<string:chave>', methods=['GET', 'POST'])
def carregar_pedido(chave):
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie:

        if request.method == 'GET':
            try:
                pedido = ref.child(f'estoques/{cookie['uid']}/pedidos').child(chave).get()
            except:
                return jsonify({'chave': False})

            else:
                return jsonify(pedido)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/adicionar-item', methods=['POST'])
def adicionar_item():
    global item
    cookie, mensagem = conferir_cookie()

    if cookie:

        if request.method == 'POST':
            dadoJson = request.get_json()
            print(dadoJson)
            item = None
            try:
                produtos = ref.child(f'estoques/{cookie['uid']}/produtos').get()
                codigo = (dadoJson['codigo']).strip()
                cor = (dadoJson['cor']).strip()
                for armacao in produtos:
                    if produtos[armacao]['codigo'] == codigo :
                        if cor in produtos[armacao]['cores']:
                            if produtos[armacao]['cores'][dadoJson['cor']] > 0:
                                item = {
                                    'chave': armacao,
                                    'codigo': produtos[armacao]['codigo'],
                                    'cores': {dadoJson['cor']:[1, produtos[armacao]['cores'][dadoJson['cor']], False]},
                                    'img': produtos[armacao]['imagem'],
                                    'preco': produtos[armacao]['preco']
                                }
                            else:
                                item = {
                                    'chave': 'vazia', 'erro': '1', 'msg': 'Cor esgotada!'
                                }
                        else:
                            item = {
                                'chave':'vazia', 'erro': '2', 'msg': 'Cor não encontrada!'
                            }
            except:
                return jsonify({'chave': False})

            else:
                print(item)
                if item != None:
                    return jsonify(item)
                else:
                    return jsonify({'chave':'vazia', 'erro':'3', 'msg': 'Modelo não encontrado!'})

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/baixa', methods=['POST'])
def dar_baixa():
    cookie, mensagem = conferir_cookie()

    if cookie:

        if request.method == 'POST':
            pedido = request.get_json()

            try:
                pedido['ativo'] = False
                for armacao in pedido['carrinho']:
                    if armacao['chave'] in ref.child(f'estoques/{cookie['uid']}/produtos').get():
                        local = ref.child(f'estoques/{cookie['uid']}/produtos/{armacao['chave']}').child('cores')
                        for cor in armacao['cores']:
                            if armacao['cores'][cor][2] == True:
                                local.update({cor: (local.child(cor).get() - armacao['cores'][cor][0])})

                ref.child(f'estoques/{cookie['uid']}/pedidos/{pedido['chave']}').update(pedido)
            except Exception as e:
                print(e)
                return jsonify({'chave': False})

            else:

                return jsonify(pedido)


    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/deletar-pedido')
def deletar_pedido():
    chave = request.args.get('chave')
    cookie, mensagem = conferir_cookie()

    if cookie:


        try:
            referenciaDeletado = ref.child(f'estoques/{cookie['uid']}/pedidos/{chave}')
            referenciaDeletado.delete()

        except:
            mensagem = 'Algo deu errado ao Excluir os dados do pedido!'
            return redirect(url_for('carregar', chave=chave, mensagem=mensagem))
        else:

            return redirect(url_for('pedidos', mensagem='Pedido excluído com sucesso!'))


    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Sessão encerrada!'))


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






