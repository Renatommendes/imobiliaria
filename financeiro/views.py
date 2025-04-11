from django.shortcuts import render, get_object_or_404, redirect
from .forms import BoletoForm
from .models import Boleto
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from clientes.models import Cliente

@login_required
def boletos(request):
    if request.method == "POST":
        form = BoletoForm(request.POST, request.FILES)
        if form.is_valid():
            boleto = form.save(commit=False)
            boleto.save()
            messages.success(request, "Boleto cadastrado com sucesso!")
            return redirect("boletos")
        else:
            messages.error(request, "Erro ao salvar o boleto. Verifique os campos abaixo.")
    else:
        form = BoletoForm()

    # Se for administrador, vê todos os boletos. Se não, vê só os próprios.
    if request.user.username == "administrador":
        boletos = Boleto.objects.all()
    else:
        boletos = Boleto.objects.filter(usuario=request.user)

    return render(request, "boletos.html", {"form": form, "boletos": boletos})




@login_required
def editar_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)

    if request.user.username != 'administrador':
        messages.error(request, "Você não tem permissão para editar este boleto.")
        return redirect('boletos')

    if request.method == 'POST':
        form = BoletoForm(request.POST, request.FILES, instance=boleto)
        if form.is_valid():
            form.save()
            messages.success(request, "Boleto atualizado com sucesso!")
            return redirect('boletos')
    else:
        form = BoletoForm(instance=boleto)

    return render(request, 'editar_boleto.html', {'form': form, 'boleto': boleto})

@login_required
def excluir_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)

    if request.user.username != 'administrador':
        messages.error(request, "Você não tem permissão para excluir este boleto.")
        return redirect('boletos')

    boleto.delete()
    messages.success(request, "Boleto excluído com sucesso!")
    return redirect('boletos')
