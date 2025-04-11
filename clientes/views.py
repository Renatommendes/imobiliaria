from .forms import ClienteForm
from .models import Cliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserEditForm  # Criamos esse formulário abaixo
from .models import Contrato
from .forms import ContratoForm
from .models import OrdemContrato, EtapaContrato
from .forms import OrdemContratoForm, UploadContratoForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from .forms import EditarArquivoForm
from .forms import FaseProcessoForm
from .models import FaseProcesso, ItemFaseProcesso
from django.db.models import Q
from .forms import ItemFaseProcessoForm




@login_required
def cadastrar_cliente(request, pk=None):
    # Verifica se o usuário é o administrador
    if request.user.username != 'administrador':
        return redirect('home')  # Redireciona para a página inicial se não for administrador

    if pk:
        cliente = get_object_or_404(Cliente, pk=pk)
    else:
        cliente = None

    if request.method == "POST":
        if 'delete' in request.POST:
            cliente.delete()
            return redirect('listar_clientes')
        else:
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)

    clientes = Cliente.objects.all()
    return render(request, 'cadastrar_cliente.html', {'form': form, 'clientes': clientes})

@login_required
def listar_clientes(request):
    # Verifica se o usuário é o administrador
    if request.user.username != 'administrador':
        return redirect('home')  # Redireciona para a página inicial se não for administrador

    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

@login_required
def home(request):
    return render(request, 'home.html')  # Permite que todos acessem a home


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Criptografando a senha
            user.save()
            login(request, user)  # Faz login automaticamente após o cadastro
            return redirect("home")  # Redireciona para a página inicial
    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})


@login_required
def excluir_cliente(request, pk):
    if request.user.username != 'administrador':
        return redirect('home')  # Apenas o administrador pode excluir

    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('listar_clientes')


# Verifica se o usuário é administrador
def is_admin(user):
    print(f"Usuário autenticado: {user.is_authenticated}, Nome: {user.username}")  # TESTE
    return user.is_authenticated and user.username == "administrador"


@login_required
@user_passes_test(is_admin)
def user_list(request):
    print("Acessando a página de usuários...")  # TESTE
    usuarios = User.objects.all()
    return render(request, 'usuarios/user_list.html', {'usuarios': usuarios})

@login_required
@user_passes_test(is_admin)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        usuario.username = request.POST.get("username")
        usuario.email = request.POST.get("email")
        usuario.save()
        return redirect("user_list")
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(is_admin)
def excluir_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        usuario.delete()
        return redirect("user_list")
    return render(request, 'usuarios/excluir_usuario.html', {'usuario': usuario})

def user_list_test(request):
    return HttpResponse("Página de listagem de usuários funcionando")



def contratos(request):
    tipo_contrato = request.GET.get('tipo', '')  # Pega o tipo do contrato da URL (se houver)
    
    if tipo_contrato in ['venda', 'locacao']:
        contratos = Contrato.objects.filter(tipo=tipo_contrato)
    else:
        contratos = Contrato.objects.none()  # Retorna uma lista vazia se não houver seleção
    
    return render(request, 'contratos/contratos.html', {'contratos': contratos, 'tipo_contrato': tipo_contrato})



def listar_contratos(request):
    if request.user.username == "administrador":
        # Se for admin, vê todos os contratos
        contratos = Contrato.objects.all()
    else:
        # Usuário comum vê apenas seus contratos
        contratos = Contrato.objects.filter(usuario=request.user)

    return render(request, "contratos/listar_contratos.html", {"contratos": contratos})

@login_required
@user_passes_test(is_admin)
def adicionar_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos')
    else:
        form = ContratoForm()

    return render(request, 'contratos/adicionar_contrato.html', {'form': form})

def editar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    if request.method == "POST":
        form = ContratoForm(request.POST, request.FILES, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect("listar_contratos")  # Redireciona para a lista após salvar
    else:
        form = ContratoForm(instance=contrato)

    return render(request, "contratos/editar_contrato.html", {"form": form})

def excluir_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    if request.method == "POST":
        contrato.delete()
        return redirect("listar_contratos")  # Redireciona para a lista após exclusão

    return render(request, "contratos/excluir_contrato.html", {"contrato": contrato})


@login_required
def criar_ordem_contrato(request):
    if request.method == "POST":
        form = OrdemContratoForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')
            nome = form.cleaned_data.get('nome')
            tipo = form.cleaned_data.get('tipo')
            arquivo = form.cleaned_data.get('arquivo')
            status = form.cleaned_data.get('status')
            etapa_form = form.cleaned_data.get('etapa')
            tipo_envio = form.cleaned_data.get('tipo_envio', 'envio')

            numero_etapa = etapa_form.numero

            # Verifica se a etapa já existe para o usuário
            etapa, criada = EtapaContrato.objects.get_or_create(
                usuario=usuario,
                numero=numero_etapa,
            )

            if criada:
                if numero_etapa == "1":
                    etapa.habilitada = True
                else:
                    numero_anterior = str(int(numero_etapa) - 1)
                    try:
                        etapa_anterior = EtapaContrato.objects.get(usuario=usuario, numero=numero_anterior)
                        # A nova etapa só será habilitada se a anterior estiver concluída
                        etapa.habilitada = etapa_anterior.concluida
                    except EtapaContrato.DoesNotExist:
                        etapa.habilitada = False  # Não habilita se não encontrar a anterior

                etapa.save()

            # Cria a ordem de contrato associada à etapa
            OrdemContrato.objects.create(
                usuario=usuario,
                nome=nome,
                tipo=tipo,
                arquivo=arquivo,
                status=status,
                etapa=etapa,
                tipo_envio=tipo_envio
            )

            messages.success(request, "Ordem de contrato criada com sucesso!")
            return redirect('listar_ordens_contrato')
        else:
            print("Erro no formulário:", form.errors)
    else:
        form = OrdemContratoForm()

    return render(request, 'contratos/criar_ordem_contrato.html', {'form': form})





@login_required
def listar_ordens_contrato(request):
    usuarios = []
    usuario_id = None
    etapas_ordenadas = []

    # 🔹 Se for administrador, pode selecionar usuários
    if request.user.username == "administrador":
        usuarios = User.objects.all()
        usuario_id = request.GET.get("usuario")
    else:
        usuario_id = request.user.id

    # 🔹 Lógica para usuários comuns
    if request.user.username != "administrador":
        usuario = request.user

        # 🔹 Garante que a etapa 1 sempre exista e esteja habilitada
        etapa_1, created = EtapaContrato.objects.get_or_create(
            usuario=usuario,
            numero=1,
            defaults={"habilitada": True}
        )
        if not etapa_1.habilitada:
            etapa_1.habilitada = True
            etapa_1.save()

        # 🔹 Busca todas as etapas do usuário, em ordem
        etapas = EtapaContrato.objects.filter(usuario=usuario).order_by("numero")

        for i, etapa in enumerate(etapas):
            ordens_na_etapa = OrdemContrato.objects.filter(usuario=usuario, etapa=etapa)

            # 🔹 Remove etapas vazias (exceto a etapa 1)
            if not ordens_na_etapa.exists() and etapa.numero != 1:
                etapa.delete()
                continue

            # 🔹 Verifica se pode liberar próxima etapa
            todas_concluidas = all(ordem.status == "Concluído" for ordem in ordens_na_etapa)
            if todas_concluidas and i + 1 < len(etapas):
                proxima_etapa = etapas[i + 1]
                if not proxima_etapa.habilitada:
                    proxima_etapa.habilitada = True
                    proxima_etapa.save()

            # 🔹 Verifica se TODAS as ordens são do tipo 'visualizacao'
            somente_visualizacao = all(ordem.tipo_envio == "visualizacao" for ordem in ordens_na_etapa)

            # 🔹 Adiciona ordens para exibição
            ordens_info = []
            for ordem in ordens_na_etapa:
                ordens_info.append({
                    "ordem": ordem,
                    "pode_enviar": etapa.habilitada,
                })

            etapas_ordenadas.append({
                "etapa": etapa,
                "ordens": ordens_info,
                "somente_visualizacao": somente_visualizacao,
            })

        return render(request, "contratos/listar_ordens_contrato.html", {
            "usuarios": usuarios,
            "usuario_selecionado": usuario_id,
            "etapas_ordenadas": etapas_ordenadas,
        })

    # 🔹 Lógica para administrador
    ordens = []
    etapas_agrupadas = {}

    if usuario_id:
        ordens = OrdemContrato.objects.filter(usuario_id=usuario_id).order_by("etapa__numero", "-id")

        for ordem in ordens:
            if ordem.etapa not in etapas_agrupadas:
                etapas_agrupadas[ordem.etapa] = []
            etapas_agrupadas[ordem.etapa].append(ordem)

    return render(request, "contratos/listar_ordens_contrato.html", {
        "usuarios": usuarios,
        "usuario_selecionado": usuario_id,
        "ordens": ordens,
        "etapas_agrupadas": etapas_agrupadas,
    })





# Usuário faz o upload do contrato solicitado
@login_required
def upload_contrato(request, ordem_id):
    ordem = get_object_or_404(OrdemContrato, id=ordem_id, usuario=request.user)

    if request.method == "POST":
        form = UploadContratoForm(request.POST, request.FILES, instance=ordem)
        if form.is_valid():
            ordem.status = "Concluído"
            ordem.save()
            messages.success(request, "Contrato enviado com sucesso!")
            return redirect('listar_ordens_contrato')
    else:
        form = UploadContratoForm(instance=ordem)

    return render(request, 'contratos/upload_contrato.html', {'form': form, 'ordem': ordem})

def editar_ordem_contrato(request, id):
    ordem = get_object_or_404(OrdemContrato, id=id)
    
    if request.method == 'POST':
        form = OrdemContratoForm(request.POST, instance=ordem)
        if form.is_valid():
            form.save()
            return redirect('listar_ordens_contrato')  # Redireciona após salvar
    else:
        form = OrdemContratoForm(instance=ordem)
    
    return render(request, 'contratos/editar_ordem_contrato.html', {'form': form, 'ordem': ordem})




def excluir_ordem_contrato(request, ordem_id):
    if request.user.username != "administrador":
        messages.error(request, "Você não tem permissão para excluir ordens.")
        return redirect('listar_ordens_contrato')

    ordem = get_object_or_404(OrdemContrato, id=ordem_id)
    etapa = ordem.etapa  # Guarda a etapa antes de excluir a ordem
    ordem.delete()

    # Verifica se a etapa ficou sem nenhuma ordem associada
    if not etapa.ordens.exists():  # 'ordens' é o related_name
        etapa.delete()

    messages.success(request, "Ordem excluída com sucesso.")
    return redirect('listar_ordens_contrato')



def visualizar_ordem_contrato(request, ordem_id):
    ordem = get_object_or_404(OrdemContrato, id=ordem_id)

    # Verifica se o usuário tem permissão para acessar essa ordem
    if request.user != ordem.usuario and not request.user.is_superuser:
        return redirect('listar_ordens_contrato')

    if request.method == 'POST':
        form = UploadContratoForm(request.POST, request.FILES, instance=ordem)
        if form.is_valid():
            ordem.status = 'concluido'  # Atualiza o status para concluído
            form.save()
            return redirect('listar_ordens_contrato')

    else:
        form = UploadContratoForm(instance=ordem)

    return render(request, 'contratos/visualizar_ordem_contrato.html', {'ordem': ordem, 'form': form})

def editar_upload_contrato(request, ordem_id):
    ordem = get_object_or_404(OrdemContrato, id=ordem_id)

    if request.method == 'POST':
        form = UploadContratoForm(request.POST, request.FILES, instance=ordem)
        if form.is_valid():
            form.save()
            return redirect('visualizar_ordem_contrato', ordem_id=ordem.id)
    else:
        form = UploadContratoForm(instance=ordem)

    return render(request, 'contratos/editar_upload_contrato.html', {'form': form, 'ordem': ordem})



@login_required
def criar_etapa(request, usuario_id):
    if request.user.username == 'administrador':
        usuario = User.objects.get(id=usuario_id)

        # Obtém a maior etapa do usuário e cria a próxima
        maior_etapa = OrdemContrato.objects.filter(usuario=usuario).order_by('-etapa').first()
        nova_etapa = maior_etapa.etapa + 1 if maior_etapa else 1

        # Criar uma ordem genérica para indicar a nova etapa
        OrdemContrato.objects.create(
            usuario=usuario,
            nome=f"Ordem Inicial da Etapa {nova_etapa}",
            tipo="Padrão",
            status="pendente",
            etapa=nova_etapa
        )

    return redirect('listar_ordens_contrato')



def avancar_etapa(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    # Obtém a etapa atual do usuário
    etapa_atual = EtapaContrato.objects.filter(usuario=usuario, concluida=False).order_by('numero').first()

    if not etapa_atual:
        messages.error(request, "Não há etapas disponíveis para avançar.")
        return redirect('listar_ordens_contrato')

    # Verifica se todas as ordens dessa etapa estão concluídas
    ordens_pendentes = OrdemContrato.objects.filter(usuario=usuario, etapa=etapa_atual).exclude(status='concluido')

    if ordens_pendentes.exists():
        messages.error(request, "Você ainda tem ordens pendentes nesta etapa. Conclua todas antes de avançar.")
        return redirect('listar_ordens_contrato')

    # Marca a etapa atual como concluída
    etapa_atual.concluida = True
    etapa_atual.save()

    # Habilita a próxima etapa, se existir
    proxima_etapa = EtapaContrato.objects.filter(usuario=usuario, numero=etapa_atual.numero + 1).first()
    
    if proxima_etapa:
        proxima_etapa.habilitada = True
        proxima_etapa.save()

    messages.success(request, "Etapa avançada com sucesso!")
    return redirect('listar_ordens_contrato')

@login_required
def listar_ordens_usuario(request):
    # 🔹 Se for admin, vê todas as ordens. Se não, vê só as dele.
    if request.user.is_superuser:
        ordens = OrdemContrato.objects.all().order_by('-id')
        eh_admin = True  # Sinaliza que é admin
    else:
        ordens = OrdemContrato.objects.filter(usuario=request.user).order_by('-id')
        eh_admin = False  # Sinaliza que não é admin

    # 🔹 Se for um POST (upload de arquivo) e o usuário comum estiver enviando
    if request.method == "POST" and not request.user.is_superuser:
        ordem_id = request.POST.get("ordem_id")
        ordem = OrdemContrato.objects.get(id=ordem_id, usuario=request.user)  # Garante que só altera dele
        form = OrdemContratoForm(request.POST, request.FILES, instance=ordem)

        if form.is_valid():
            ordem.arquivo = form.cleaned_data['arquivo']
            ordem.status = "Concluído"  # 🔹 Atualiza o status
            ordem.save()
            return redirect('listar_ordens_usuario')

    return render(request, 'contratos/listar_ordens_usuario.html', {'ordens': ordens, 'eh_admin': eh_admin})


@login_required
def submeter_arquivo(request, ordem_id):
    ordem = get_object_or_404(OrdemContrato, id=ordem_id)

    # 🔹 Apenas o usuário dono da ordem pode enviar o arquivo
    if request.user != ordem.usuario:
        return HttpResponseForbidden("Você não tem permissão para enviar este arquivo.")

    if request.method == "POST" and request.FILES.get("arquivo"):
        ordem.arquivo = request.FILES["arquivo"]
        ordem.status = "Concluído"  # 🔹 Atualiza o status automaticamente
        ordem.save()
        return redirect("listar_ordens_contrato")  # 🔹 Redireciona para a listagem após o envio

    return redirect("listar_ordens_contrato")


@login_required
def editar_arquivo_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemContrato, id=ordem_id, usuario=request.user)

    if request.method == "POST":
        form = EditarArquivoForm(request.POST, request.FILES, instance=ordem)
        if form.is_valid():
            form.save()
            return redirect("listar_ordens_contrato")  # 🔹 Redireciona para a listagem após salvar
    else:
        form = EditarArquivoForm(instance=ordem)

    return render(request, "contratos/editar_arquivo_ordem.html", {"form": form, "ordem": ordem})

@login_required
def processos(request):
    return render(request, 'processos/pagina_processos.html')


@login_required
def adicionar_fase(request):
    if request.user.username != 'administrador':
        return redirect('pagina_processos')  # Ou outra página que preferir

    if request.method == 'POST':
        form = FaseProcessoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_processos')  # Redireciona após adicionar
    else:
        form = FaseProcessoForm()

    return render(request, 'processos/adicionar_fase.html', {'form': form})


@login_required
def pagina_processos(request):
    usuarios = User.objects.all()
    usuario_id = request.GET.get('usuario')
    fases = []

    if usuario_id:
        fases = FaseProcesso.objects.filter(usuario_id=usuario_id).order_by('numero')

    return render(request, 'processos/pagina_processos.html', {
        'usuarios': usuarios,
        'usuario_id': usuario_id,
        'fases': fases,
    })


@login_required
def adicionar_item_fase(request):
    if request.user.username != 'administrador':
        return redirect('pagina_processos')

    fase_id = request.GET.get('fase_id')
    fase = get_object_or_404(FaseProcesso, id=fase_id)

    if request.method == 'POST':
        form = ItemFaseProcessoForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.fase = fase
            item.save()
            return redirect('pagina_processos')
    else:
        form = ItemFaseProcessoForm()

    return render(request, 'processos/adicionar_item.html', {'form': form, 'fase': fase})




def validar_etapa(request, etapa_id):
    if request.user.username == "administrador":
        messages.error(request, "Somente o usuário comum pode validar etapas.")
        return redirect('listar_ordens_contrato')

    etapa = get_object_or_404(EtapaContrato, id=etapa_id)

    # Verifica se há ordens associadas à etapa
    ordens_da_etapa = etapa.ordens.all()
    if not ordens_da_etapa:
        messages.error(request, "Não há ordens associadas a esta etapa.")
        return redirect('listar_ordens_contrato')

    # Atualiza o status de todas as ordens da etapa para "Concluído"
    try:
        for ordem in ordens_da_etapa:
            ordem.status = 'Concluído'  # Verifique se o status "Concluído" está correto
            ordem.save()

        # Verifica se todas as ordens da etapa estão concluídas
        if all(ordem.status == 'Concluído' for ordem in ordens_da_etapa):
            # Se todas as ordens da etapa estiverem concluídas, libera a próxima etapa
            proxima_etapa = EtapaContrato.objects.filter(numero=etapa.numero + 1).first()
            if proxima_etapa:
                proxima_etapa.habilitada = True  # Certifique-se de que o campo 'habilitada' existe
                proxima_etapa.save()
                messages.success(request, f"A etapa {etapa.numero} foi concluída. A próxima etapa foi liberada.")
            else:
                messages.success(request, f"A etapa {etapa.numero} foi concluída. Não há mais etapas para liberar.")
        else:
            messages.error(request, "Não é possível liberar a próxima etapa, pois algumas ordens ainda não foram concluídas.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao validar a etapa: {str(e)}")
        return redirect('listar_ordens_contrato')

    return redirect('listar_ordens_contrato')

