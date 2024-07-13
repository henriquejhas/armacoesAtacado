import json

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
import requests
import time
from PIL import Image

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
ALLOWED_EXTENSIONS2 = {'jpg', 'jpeg', 'png'}



@app.route('/painel/catalogo')
def painel_catalogo():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':
        try:
            armacoes = []
            produtos = ref.child(f'estoques/{cookie["uid"]}/produtos').get()
            for produto in produtos:
                armacao = produtos[produto]
                armacoes.append((produto, armacao))

            loja = ref.child('estoques').child(f'{cookie["uid"]}').child('loja').get()

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

                    loja = ref.child('estoques').child(f'{cookie["uid"]}').child('loja').get()
                    nomeLoja= (loja['nomeLoja']).replace(' ', '').lower()
                except:
                    return redirect(url_for('painel_catalogo'))
                else:
                    return redirect(url_for('catalogo', nome=nomeLoja))


            else:
                session['usuario_logado'] = None
                return redirect(url_for('logout', mensagem=mensagem))
        else:
            return render_template('catalogo_nao_encontrado.html',mensagem='Erro ao ler os dados do catálogo!')


@app.route('/historia', methods=['POST'])
def add_historia():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'sobre': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/sobre').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "historia"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/whatsapp', methods=['POST'])
def add_whatsapp():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'whatsapp': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/whatsapp').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "whatsapp"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/instagram', methods=['POST'])
def add_instagram():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'instagram': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/instagram').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "instagram"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/facebook', methods=['POST'])
def add_facebook():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'facebook': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/facebook').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "facebook"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/youtube', methods=['POST'])
def add_youtube():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'youtube': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/youtube').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "youtube"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/endereco', methods=['POST'])
def add_endereco():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'endereco': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/endereco').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "endereco"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/funcionamento', methods=['POST'])
def add_funcionamento():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'aberto': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/aberto').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "funcionamento"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/cor', methods=['POST'])
def add_cor():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'cor': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/cor').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "cor"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/fonte', methods=['POST'])
def add_fonte():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
        dadoJson = request.get_json()
        dados = dadoJson.get('dado')
        try:
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'fonte': dados})
        except:
            return jsonify({'mensagem': False})
        else:
            if ref.child(f'estoques/{cookie["uid"]}/loja/fonte').get() == dados:
                return jsonify({'mensagem': True, "dados": dados, "tipo": "fonte"})
            else:
                return jsonify({'mensagem': False})
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/logo', methods=['POST'])
def add_logo():
    global url
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
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
                            local = f'estoques/{cookie["uid"]}/{timestamp}.jpg'
                            blob = bucket.blob(local)
                            blob.upload_from_filename('somepic.jpg', content_type='image/jpg')
                            url = firebase.storage().child(local).get_url(token)
                        elif tipo in 'png':
                            imagem.save('somepic.png')
                            timestamp = time.time()
                            local = f'estoques/{cookie["uid"]}/{timestamp}.png'
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
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'logo': url})
            return redirect(url_for('painel_catalogo', mensagem="Imagem salva com sucesso!!"))
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/banner', methods=['POST'])
def add_banner():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
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
                        local = f'estoques/{cookie["uid"]}/{timestamp}.jpg'
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
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'banner': url})
            return redirect(url_for('painel_catalogo', mensagem="Imagem salva com sucesso!!"))
    else:
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/foto', methods=['POST'])
def add_foto():
    cookie, mensagem = conferir_cookie()
    if cookie and mensagem == '':
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
                        local = f'estoques/{cookie["uid"]}/{timestamp}.jpg'
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
            ref.child(f'estoques/{cookie["uid"]}/loja').update({'foto': url})
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
            if 'pedidos' not in ref.child(f'estoques/{chave}').get():
                ref.child(f'estoques/{chave}/pedidos').set({'contador': 0})
            resNumero = ref.child(f'estoques/{chave}/pedidos').child('contador').get()
            if resNumero != None:
                ref.child(f'estoques/{chave}/pedidos').update({'contador': (resNumero + 1)})
                dadoJson['numero'] = ('0' * (5 - len(str((resNumero + 1))))) + str((resNumero + 1))
                dadoJson['ativo'] = True
                dadoJson['desconto'] = 0.0
                res = ref.child(f'estoques/{chave}/pedidos').push(dadoJson)
            else:
                ref.child(f'estoques/{chave}/pedidos').update({'contador': 1})
                dadoJson['numero'] = ('0' * (5 - len(str(1)))) + str(1)
                dadoJson['ativo'] = True
                res = ref.child(f'estoques/{chave}/pedidos').push(dadoJson)

        except Exception as erro:
            print(erro)
            return jsonify({'mensagem': False,'erro': str(erro)})
        else:
            if res.key in ref.child(f'estoques/{chave}/pedidos').get():
                return jsonify({'mensagem': True, 'dados': dadoJson})
            else:
                return jsonify({'mensagem': False,'erro': '1'})
    else:
        return jsonify({'mensagem': False,'erro': '2'})


@app.route('/salvar', methods=['POST'])
def salvar():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':
        global loja, res
        dadoJson = request.get_json()

        try:
            resNumero = ref.child(f'estoques/{cookie["uid"]}/pedidos').child('contador').get()
            if resNumero != None:
                ref.child(f'estoques/{cookie["uid"]}/pedidos').update({'contador': (resNumero + 1)})
                dadoJson['numero'] = ('0' * (5 - len(str((resNumero + 1))))) + str((resNumero + 1))
                dadoJson['ativo'] = True
                res = ref.child(f'estoques/{cookie["uid"]}/pedidos').push(dadoJson)
            else:
                ref.child(f'estoques/{cookie["uid"]}/pedidos').update({'contador': 1})
                dadoJson['numero'] = ('0' * (5 - len(str(1)))) + str(1)
                dadoJson['ativo'] = True
                res = ref.child(f'estoques/{cookie["uid"]}/pedidos').push(dadoJson)

        except Exception as erro:
            print(erro)
            return jsonify({'mensagem': False,'erro': str(erro)})
        else:
            if res.key in ref.child(f'estoques/{cookie["uid"]}/pedidos').get():
                return jsonify(dadoJson)
            else:
                return jsonify({'mensagem': False,'erro': '1'})

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/pedidos', methods=['POST', 'GET'])
def pedidos():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'GET':
            mensagem = request.args.get('mensagem')
            try:
                listaPedidos = []
                pedidos = ref.child(f'estoques/{cookie["uid"]}/pedidos').get()
            except:
                return render_template('pedidos.html', pedidos=[], mensagem='Erro ao ler os pedidos!')

            else:
                if pedidos:
                    for chave in pedidos:
                        if chave != 'contador':
                            pedido = pedidos[chave]
                            listaPedidos.append((chave, pedido))

                listaPedidos.reverse()
                return render_template('pedidos.html', pedidos=listaPedidos, mensagem=mensagem)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/novo-pedido', methods=['GET'])
def novo_pedido():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'GET':
                try:
                    loja = ref.child('estoques').child(f'{cookie["uid"]}').child('loja').get()
                    lista = ref.child(f'estoques/{cookie["uid"]}/produtos').get()
                    produtos = []
                    for produto in lista:
                        produtos.append(lista[produto]['codigo'])
                except:
                    return render_template('novo_pedido.html', mensagem='Erro ao carregar lista de produtos')
                else:
                    return render_template('novo_pedido.html',mensagem=mensagem, produtos=produtos, loja=loja)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/visualizar/<string:chave>', methods=['GET', 'POST'])
def visualizar(chave):
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'GET':
            try:
                loja = ref.child('estoques').child(f'{cookie["uid"]}').child('loja').get()
                pedido = ref.child(f'estoques/{cookie["uid"]}/pedidos').child(chave).get()
                lista = ref.child(f'estoques/{cookie["uid"]}/produtos').get()
                produtos = []
                for produto in lista:
                    produtos.append(lista[produto]['codigo'])
            except:
                return render_template('visualizarPedido.html', pedido=[], mensagem='Erro ao ler os pedidos!')

            else:
                return render_template('visualizarPedido.html', pedido=pedido, chave=chave, produtos=produtos, loja=loja)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/carregar-codigos/', methods=['GET', 'POST'])
def carregar_codigos():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'GET':
            try:
                lista = ref.child(f'estoques/{cookie["uid"]}/produtos').get()
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

    if cookie and mensagem == '':

        if request.method == 'GET':
            try:
                pedido = ref.child(f'estoques/{cookie["uid"]}/pedidos').child(chave).get()
            except:
                return jsonify({'chave': False})

            else:
                print(pedido)
                return jsonify(pedido)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/adicionar-item', methods=['POST'])
def adicionar_item():
    global item
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'POST':
            dadoJson = request.get_json()
            print(dadoJson)
            itens = None
            try:
                produtos = ref.child(f'estoques/{cookie["uid"]}/produtos').get()
                codigo = (dadoJson['codigo']).strip()
                cores = dadoJson['cor']
                for armacao in produtos:
                    if produtos[armacao]['codigo'] == codigo:
                        itens = {
                            'chave': armacao,
                            'codigo': produtos[armacao]['codigo'],
                            'cores': {},
                            'img': produtos[armacao]['imagem'],
                            'preco': produtos[armacao]['preco'],
                            'add': []
                        }
                        for cor in cores:
                            if cor in produtos[armacao]['cores']:
                                if produtos[armacao]['cores'][cor] > 0:
                                    itens['cores'][cor] = [1, produtos[armacao]['cores'][cor], False]
                                else:
                                    itens['add'].append([cor,'esgotada'])
                            else:
                                itens['add'].append([cor, 'não encontrada'])
            except:
                return jsonify({'chave': False})

            else:
                print(itens)
                if itens != None:
                    return jsonify(itens)
                else:
                    return jsonify({'chave':'vazia', 'erro':'3', 'msg': 'Código não encontrado!'})

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


@app.route('/baixa', methods=['POST'])
def dar_baixa():
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'POST':
            pedido = request.get_json()

            try:
                pedido['ativo'] = False
                for armacao in pedido['carrinho']:
                    if armacao['chave'] in ref.child(f'estoques/{cookie["uid"]}/produtos').get():
                        local = ref.child(f'estoques/{cookie["uid"]}/produtos/{armacao["chave"]}').child('cores')
                        for cor in armacao['cores']:
                            if armacao['cores'][cor][2] == True:
                                local.update({cor: (local.child(cor).get() - armacao['cores'][cor][0])})
                if 'chave' in pedido:
                    ref.child(f'estoques/{cookie["uid"]}/pedidos/{pedido["chave"]}').update(pedido)
                else:
                    resNumero = ref.child(f'estoques/{cookie["uid"]}/pedidos').child('contador').get()
                    if resNumero != None:
                        ref.child(f'estoques/{cookie["uid"]}/pedidos').update({'contador': (resNumero + 1)})
                        pedido['numero'] = ('0' * (5 - len(str((resNumero + 1))))) + str((resNumero + 1))

                    else:
                        ref.child(f'estoques/{cookie["uid"]}/pedidos').update({'contador': 1})
                        pedido['numero'] = ('0' * (5 - len(str(1)))) + str(1)

                    pedido['ativo'] = False
                    res = ref.child(f'estoques/{cookie["uid"]}/pedidos').push(pedido)
                    pedido['chave'] = res.key
                    ref.child(f'estoques/{cookie["uid"]}/pedidos').child(res.key).update(pedido)
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

    if cookie and mensagem == '':


        try:
            referenciaDeletado = ref.child(f'estoques/{cookie["uid"]}/pedidos/{chave}')
            referenciaDeletado.delete()

        except:
            mensagem = 'Algo deu errado ao Excluir os dados do pedido!'
            return redirect(url_for('carregar', chave=chave, mensagem=mensagem))
        else:

            return redirect(url_for('pedidos', mensagem='Pedido excluído com sucesso!'))


    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Sessão encerrada!'))


@app.route('/frete', methods=['POST'])
def frete():
    global response
    dados = request.get_json()
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        try:
            url = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"

            altura = dados['altura']
            largura = dados['largura']
            comprimento = dados['comprimento']
            peso = dados['peso']
            origem = dados['origem']
            destino = dados['destino']

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOThmYWFhZWJlZTFkMzBkZTk3NmM0Y2E3ZTIwNWU5MDRjZGEzNzJjNjdlZWRmMWYxYTU2MzVhOTc5NTA0NjE1NzA5YTdiZTEzNDIzNThmMGIiLCJpYXQiOjE3MTkwOTExNzQuMDcxNTk3LCJuYmYiOjE3MTkwOTExNzQuMDcxNTk5LCJleHAiOjE3NTA2MjcxNzQuMDU3MzEsInN1YiI6IjljNTliMDgxLWYwZGQtNGY2NC1iOTU3LTljMDBlNWI0OTI4NCIsInNjb3BlcyI6WyJzaGlwcGluZy1jYWxjdWxhdGUiXX0.4i6wlI-6L6cESW9coWwsXIyivRzEPtwvcjbgV_56uJtdpW3CIUq4wtZedrEttwlOdglCFRCcmG8besdcKFbe1xIEg5C8jS7sOfp2gYf7ZU3KXHOR6kBIUjse3uvqEe4IEfj_X_NaeAmlh4LBC6__tGIiNw4QKnoaTeT0E3izZRCqTes4Z5JumRLvlcut02B-xUKF-EvsUR9wftiWkcBvx6gtRHJHoJVSffpAbhfKdo45s2Q4Qsa9ucqFkIVnot2CgZdOJ43h65K9WSyXU6RQKJKJdDzVCglB3XmS4ly2hYiyofuBIbcfcfQXVle6qTDf-pkjAxKNHGqvxuyCxCsMtg6AYrpm3pHvxfs5Ye-iu4XrhRBXobsDUMg9dzc9Kq2KVjy43O61FokANa_LGkoiIybyGs3sZqk03DAU1C89bP3rprzDkUGpm1h9HP8tSV8yCQrhAglupp1TMPzWWDW_MNl2DwIZAtV7d10WVA2v9JKCE2Ayfe1Hmhl8fUGbwTNSAfqpNX_Y3L7h8gcIPlz1Q7vU-EX60PqIilDw_j9wg9TgMYLHI6k_fWdTbr--rYOu3o67UqNAC0YtVfc6U8S-k-svt5in9QOiKKjUQm5pZVYxooHOowH4X2cFzx32XqeY_ksHYuwVxxLlytdrgVmHprof-y2CfzJN1prfGPDjarU",
                "User-Agent": "Aplicação henrique._jh@hotmail.com"
            }

            payload = {
                "from": {"postal_code": origem},
                "to": {"postal_code": destino},
                "package": {
                    "height": altura,
                    "width": largura,
                    "length": comprimento,
                    "weight": peso
                }
            }

            response = requests.post(url, json=payload, headers=headers)

        except:
            mensagem = 'Algo deu errado ao Excluir os dados do pedido!'
            return jsonify(response.json())
        else:

            print(response.text)
            return jsonify(response.json())


    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Sessão encerrada!'))


@app.route('/pagamento', methods=['POST'])
def pagamento():
    url = "https://sandbox.api.pagseguro.com/orders"

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer f6e70f44-7176-4707-bf10-440194f5faf7131fe88343f3adc865ef6fd4368f24aabc13-bb59-46b2-aa4b-d4c1704252b7",
        "content-type": "application/json"
    }

    payload = {
        "reference_id": "ex-00001",
        "customer": {
            "name": "Jose da Silva",
            "email": "email@test.com",
            "tax_id": "12345678909",
            "phones": [
                {
                    "country": "55",
                    "area": "11",
                    "number": "999999999",
                    "type": "MOBILE"
                }
            ]
        },
        "items": [
            {
                "reference_id": "referencia do item",
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 500
            }
        ],
        "shipping": {"address": {
            "street": "Avenida Brigadeiro Faria Lima",
            "number": "1384",
            "complement": "apto 12",
            "locality": "Pinheiros",
            "city": "São Paulo",
            "region_code": "SP",
            "country": "BRA",
            "postal_code": "01452002"
        }},
        "notification_urls": ["https://meusite.com/notificacoes"],
        "charges": [
            {
                "reference_id": "referencia da cobranca",
                "description": "descricao da cobranca",
                "amount": {
                    "value": 500,
                    "currency": "BRL"
                },
                "payment_method": {
                    "type": "CREDIT_CARD",
                    "installments": 1,
                    "capture": True,
                    "card": {
                        "number": "4111111111111111",
                        "exp_month": "12",
                        "exp_year": "2026",
                        "security_code": "123",
                        "holder": {
                            "name": "Jose da Silva",
                            "tax_id": "65544332211"
                        },
                        "store": False
                    }
                }
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


    return render_template("pagamento_sucesso.html", response=response.text)


@app.route('/planos', methods=['POST', 'GET'])
def planos():
    global loja
    cookie, mensagem = conferir_cookie()

    if cookie and mensagem == '':

        if request.method == 'GET':
            try:
                loja = ref.child('estoques').child(f'{cookie["uid"]}').child('loja').get()
                publickey = getPublicKey()
            except:
                return render_template('planos.html', mensagem='Erro ao ler dados da loja!')

            else:
                form = FormularioUpload()
                return render_template('planos.html', loja=loja, publickey=publickey, form=form)

    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))


def getPublicKey():
    url = "https://sandbox.api.pagseguro.com/public-keys"

    payload = {"type": "card"}
    headers = {
        "accept": "*/*",
        "Authorization": "Bearer f6e70f44-7176-4707-bf10-440194f5faf7131fe88343f3adc865ef6fd4368f24aabc13-bb59-46b2-aa4b-d4c1704252b7",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    return response.json()['public_key']

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






