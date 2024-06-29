from main import app, ref, firebase, bucket
from flask import Flask
import firebase_admin
from firebase_admin import credentials, db,auth, storage
from flask_wtf import CSRFProtect
import pyrebase
from formularios import FormularioUsuario, FormularioCadastro, FormularioAdicionar, FormularioPesquisar
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from config import config
from datetime import timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
import time
from PIL import Image


ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


@app.route('/inicio')
def dashboard():
    cookie, mensagem = conferir_cookie()
    emProcesso = []
    esgotados = []
    if cookie and mensagem == '':
        pedidos = None
        try:
            pedidos = ref.child(f'estoques/{cookie['uid']}/pedidos').get()
            produtos = ref.child(f'estoques/{cookie['uid']}/produtos').get()
            for pedido in pedidos:

                if pedido != 'contador' and pedidos[pedido]['ativo'] == True:
                    emProcesso.append([pedido, pedidos[pedido]])
            for armacao in produtos:
                for cor in produtos[armacao]['cores']:
                    if produtos[armacao]['cores'][cor] <= 0:
                        esgotados.append([armacao, produtos[armacao]])
                        continue
        except:
            return render_template('dashboard.html',mensagem="Erro ao carregar dados!")
        else:
            print(pedidos)
            return render_template('dashboard.html', pedidos=emProcesso, produtos=esgotados, mensagem=mensagem)
    else:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem=mensagem))

@app.route('/adicionar', methods=['POST', 'GET'])
def adicionar():
    try:

        token = session['usuario_logado']
        cookie = auth.verify_session_cookie(token, clock_skew_seconds=5)

    except auth.ExpiredSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie de sessão expirou'))
    except auth.RevokedSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie foi revogado'))
    except auth.InvalidSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão inválido'))
    except auth.CertificateFetchError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='erro ao buscar os certificados de chave pública'))
    except auth.UserDisabledError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Registro do usuário desabilitado'))
    except ValueError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão ilegal'))
    else:

        if request.method == "GET":
            mensagem = request.args.get('mensagem')
            form = FormularioAdicionar()
            return render_template('adicionar.html', armacao={},form=form, mensagem=mensagem)
        elif request.method == 'POST':
            cores = {}
            form = FormularioAdicionar(request.form)

            if form.validate_on_submit():
                codigo = form.codigo.data
                secao = request.form['secao']
                dimensoes = form.dimensoes.data
                preco = form.preco.data
                descricao = form.descricao.data
                c = []
                cores = {}

                c.append(int(request.form['c1'] if request.form['c1'] != "" else 0))
                c.append(int(request.form['c2'] if request.form['c2'] != "" else 0))
                c.append(int(request.form['c3'] if request.form['c3'] != "" else 0))
                c.append(int(request.form['c4'] if request.form['c4'] != "" else 0))
                c.append(int(request.form['c5'] if request.form['c5'] != "" else 0))
                c.append(int(request.form['c6'] if request.form['c6'] != "" else 0))
                c.append(int(request.form['c7'] if request.form['c7'] != "" else 0))
                c.append(int(request.form['c8'] if request.form['c8'] != "" else 0))
                c.append(int(request.form['c9'] if request.form['c9'] != "" else 0))
                c.append(int(request.form['c10'] if request.form['c10'] != "" else 0))

                for i in range(0, 10):
                    if c[i] > 0:
                        cores[f'C{i + 1}'] = c[i]

                if len(cores) == 0:
                    cores['secao'] = secao
                    return render_template('adicionar.html',
                                           mensagem="Quantidade inválida, pelo menos uma cor deve ser preenchida!",
                                           form=form, armacao=cores)

                cores['secao'] = secao

                usuario = cookie['uid']
                if usuario:

                    try:

                        arquivo = request.files['arquivo']

                        if str(arquivo.filename) != '' :
                            if allowed_file(arquivo.filename):
                                imagem = Image.open(arquivo)
                                imagem = imagem.resize((700, 700))
                                imagem.save('somepic.jpg')
                                timestamp = time.time()
                                local = f'estoques/{usuario}/{timestamp}.jpg'
                                blob = bucket.blob(local)
                                print(blob.upload_from_filename('somepic.jpg', content_type='image/jpg'))
                                url = firebase.storage().child(local).get_url(token)
                            else:
                                return render_template('adicionar.html',
                                                       mensagem="Formato da imagem inválido!",
                                                       form=form, armacao=cores)
                        else:
                            return render_template('adicionar.html',
                                                   mensagem="A imagem não foi selecionada!",
                                                   form=form, armacao=cores)
                    except:
                        print("************ 4 deu ruim")
                        return render_template('adicionar.html',
                                               mensagem="Tivemos um problema com a imagem, fale com o suporte!",
                                               form=form, armacao=cores)
                    else:
                        del cores['secao']

                        chave = ref.child('estoques').child(f'{usuario}').child('produtos').push({
                            'codigo': codigo,
                            'secao': secao,
                            'dimensoes': dimensoes,
                            'preco': preco,
                            'cores': cores,
                            'descricao': descricao,
                            'imagem': url
                        })

                        if chave.key in ref.child(f'estoques/{usuario}/produtos').get():
                            return redirect(url_for('adicionar', mensagem='Armação adicionada com sucesso!'))
                        else:

                            return render_template('adicionar.html',
                                                   mensagem="Banco de dados não confirmado, fale com o suporte!",
                                                   form=form, armacao=cores)

                else:
                    session['usuario_logado'] = None
                    return redirect(url_for('logout', mensagem='Sessão encerrada!'))
            else:
                print('passou aqui deu ruim')

                return render_template('adicionar.html', form=form, armacao=cores, mensagem='Há algum campo inválido!')

@app.route('/pesquisar', methods=['POST', 'GET'])
def pesquisar():
    mensagem = request.args.get('mensagem')
    try:
        token = session['usuario_logado']
        cookie = auth.verify_session_cookie(token, clock_skew_seconds=5)
    except auth.ExpiredSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie de sessão expirou'))
    except auth.RevokedSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie foi revogado'))
    except auth.InvalidSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão inválido'))
    except auth.CertificateFetchError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='erro ao buscar os certificados de chave pública'))
    except auth.UserDisabledError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Registro do usuário desabilitado'))
    except ValueError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão ilegal'))
    else:
        if request.method == "GET":
            if cookie['uid']:
                form = FormularioPesquisar()
                return render_template('pesquisar.html',form=form, mensagem=mensagem)
            else:
                session['usuario_logado'] = None
                return redirect(url_for('logout', mensagem='Sessão encerrada!'))
        elif request.method == 'POST':
            if cookie['uid']:
                form = FormularioPesquisar(request.form)
                if form.validate_on_submit():

                    busca = form.busca.data
                    tipo = request.form['tipo']
                    armacoes = []
                    produtos = ref.child(f'estoques/{cookie['uid']}/produtos').get()
                    for produto in produtos:
                        armacao = produtos[produto]
                        if tipo != 'todos':
                            if tipo in armacao:
                                if busca in armacao[tipo]:
                                    armacoes.append((produto, armacao))
                        else:
                            armacoes.append((produto, armacao))

                    return render_template('pesquisaResultado.html', cookie=cookie, form=form, armacoes=armacoes)
                else:
                    return redirect(url_for('pesquisar.html', form=form, mensagem='Há algum campo inválido!'))

            else:
                session['usuario_logado'] = None
                return redirect(url_for('logout', mensagem='Sessão encerrada!'))

@app.route('/editar', methods=['POST', 'GET'])
def editar():
    chaveArmacao = request.args.get('chave')
    try:

        token = session['usuario_logado']
        cookie = auth.verify_session_cookie(token, clock_skew_seconds=5)

    except auth.ExpiredSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie de sessão expirou'))
    except auth.RevokedSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie foi revogado'))
    except auth.InvalidSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão inválido'))
    except auth.CertificateFetchError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='erro ao buscar os certificados de chave pública'))
    except auth.UserDisabledError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Registro do usuário desabilitado'))
    except ValueError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão ilegal'))
    else:

        if request.method == "GET":

            mensagem = request.args.get('mensagem')
            form = FormularioAdicionar()

            try:
                produto = ref.child(f'estoques/{cookie['uid']}/produtos/{chaveArmacao}').get()
                if produto == None:
                    mensagem = 'Modelo não encontrado!'
                    return redirect(url_for('editar', chave=chaveArmacao, form=form, mensagem=mensagem))
            except:
                mensagem = 'Algo deu errado ao buscar as informações no banco de dados!'
                return render_template('editar.html', chave=chaveArmacao, form=form, mensagem=mensagem)
            else:
                armacao = {}
                try:
                    if 'codigo' in produto:
                        form.codigo.data = produto['codigo']
                    if 'dimensoes' in produto:
                        form.dimensoes.data = produto['dimensoes']
                    if 'preco' in produto:
                        form.preco.data = produto['preco']
                    if 'preco' in produto:
                        form.descricao.data = produto['descricao']
                    if 'cores' in produto:
                        armacao= dict(produto['cores'])
                    else:
                        armacao = {}
                    print(armacao)
                    print(type(armacao))

                    if 'secao' in produto:
                        armacao['secao'] = produto['secao']
                    if 'imagem' in produto:
                        armacao['imagem'] = produto['imagem']
                except TypeError:
                    return render_template('editar.html', chave=chaveArmacao, form=form, mensagem="Erro na leitura do modelo",
                                           armacao=armacao)
                else:
                    return render_template('editar.html', chave=chaveArmacao, form=form, mensagem=mensagem, armacao=armacao)
        elif request.method == 'POST':

            form = FormularioAdicionar(request.form)

            if form.validate_on_submit():
                codigo = form.codigo.data
                secao = request.form['secao']
                dimensoes = form.dimensoes.data
                preco = form.preco.data
                descricao = form.descricao.data
                c = []
                cores = {}

                c.append(int(request.form['c1'] if request.form['c1'] != "" else 0))
                c.append(int(request.form['c2'] if request.form['c2'] != "" else 0))
                c.append(int(request.form['c3'] if request.form['c3'] != "" else 0))
                c.append(int(request.form['c4'] if request.form['c4'] != "" else 0))
                c.append(int(request.form['c5'] if request.form['c5'] != "" else 0))
                c.append(int(request.form['c6'] if request.form['c6'] != "" else 0))
                c.append(int(request.form['c7'] if request.form['c7'] != "" else 0))
                c.append(int(request.form['c8'] if request.form['c8'] != "" else 0))
                c.append(int(request.form['c9'] if request.form['c9'] != "" else 0))
                c.append(int(request.form['c10'] if request.form['c10'] != "" else 0))

                for i in range(0, 10):
                    if c[i] > 0:
                        cores[f'C{i + 1}'] = c[i]

                usuario = cookie['uid']
                if usuario:

                    try:

                        arquivo = request.files['arquivo']
                        if arquivo.filename != '':
                            if allowed_file(arquivo.filename):
                                imagem = Image.open(arquivo)
                                imagem = imagem.resize((700, 700))
                                imagem.save('somepic.jpg')
                                timestamp = time.time()
                                local = f'estoques/{usuario}/{timestamp}.jpg'
                                blob = bucket.blob(local)
                                blob.upload_from_filename('somepic.jpg', content_type='image/jpg')
                                url = firebase.storage().child(local).get_url(token)
                                try:
                                    urlAntiga = request.form['imagem']
                                    imagemAntiga = urlAntiga.split('?')[0]
                                    imagemAntiga = imagemAntiga.split('%2F')[2]
                                    localAntigo = f'estoques/{cookie['uid']}/{imagemAntiga}'
                                    bucket.blob(localAntigo).delete()
                                except:
                                    print('Erro ao excluir imagem antiga!')
                            else:
                                return render_template('editar.html',
                                                       mensagem="Formato da imagem inválido!",
                                                       form=form, armacao=cores)
                        else:
                            url = request.form['imagem']

                    except:
                        return render_template('editar.html',
                                               mensagem="Tivemos um problema com a imagem, fale com o suporte!",
                                               form=form)
                    else:
                        print('chave2: ', chaveArmacao)
                        ref.child('estoques').child(f'{usuario}').child(f'produtos/{chaveArmacao}').update({
                            'codigo': codigo,
                            'secao': secao,
                            'dimensoes': dimensoes,
                            'preco': preco,
                            'cores': cores,
                            'descricao': descricao,
                            'imagem': url
                        })

                        if chaveArmacao in ref.child(f'estoques/{usuario}/produtos').get():
                            return redirect(url_for('editar', chave=chaveArmacao,mensagem='Alterações salvas com sucesso!'))

                        else:
                            return redirect(
                                url_for('editar', chave=chaveArmacao, mensagem='Banco de dados não confirmado, fale com o suporte!' ))

                else:
                    session['usuario_logado'] = None
                    return redirect(url_for('logout', mensagem='Sessão encerrada!'))
            else:
                print('passou aqui deu ruim')
                return redirect(url_for('editar', chave=chaveArmacao, mensagem='Há algum campo inválido!'))

@app.route('/deletar')
def deletar():
    chave = request.args.get('chave')
    try:

        token = session['usuario_logado']
        cookie = auth.verify_session_cookie(token, clock_skew_seconds=5)

    except auth.ExpiredSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie de sessão expirou'))
    except auth.RevokedSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='O cookie foi revogado'))
    except auth.InvalidSessionCookieError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão inválido'))
    except auth.CertificateFetchError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='erro ao buscar os certificados de chave pública'))
    except auth.UserDisabledError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Registro do usuário desabilitado'))
    except ValueError:
        session['usuario_logado'] = None
        return redirect(url_for('logout', mensagem='Cookie de sessão ilegal'))
    else:

        if cookie['uid']:


            try:
                referenciaDeletado = ref.child(f'estoques/{cookie['uid']}/produtos/{chave}')
                url = referenciaDeletado.get()['imagem']
                referenciaDeletado.delete()
                try:
                    imagem = url.split('?')[0]
                    imagem = imagem.split('%2F')[2]
                    local = f'estoques/{cookie['uid']}/{imagem}'
                    bucket.blob(local).delete()
                except:
                    print('Erro ao excluir imagem antiga!')

            except:
                mensagem = 'Algo deu errado ao Excluir os dados do modelo!'
                return redirect(url_for('editar', chave=chave, mensagem=mensagem))
            else:

                return redirect(url_for('pesquisar', mensagem='Modelo excluído com sucesso!'))


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


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS