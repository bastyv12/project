from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CustomUserCreationForm
from .models import LugarTuristico, Comentario
from .forms import  LugarForm, ComentarioForm
from django.contrib.auth import logout
from django.contrib import messages
from .models import LugarTuristico, AgendaViajes
from django.utils import timezone
from .forms import AgendaForm
from .models import CATEGORIAS

def home(request):
    return render(request, 'turista/home.html')

def error403(request):
    return render(request, 'turista/error403.html')


# Registro de usuario
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

def exit(request):
    logout(request)
    return redirect('home')
    request.session.set_expiry(-1)
   
def cerrar_sesion(request):
    logout(request)
    return redirect('login')    


def catalogo_lugares(request):
    categoria = request.GET.get('categoria')
    if categoria:
        lugares = LugarTuristico.objects.filter(categoria=categoria)
    else:
        lugares = LugarTuristico.objects.all()
    return render(request, 'turista/catalogo.html', {
        'lugares': lugares,
        'categoria_activa': categoria
    })

# Agregar lugar
@permission_required('turista.add_post', login_url='error_403')
def agregar_lugar(request):
    if request.method == 'POST':
        form = LugarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo')
    else:
        form = LugarForm()
    return render(request, 'turista/agregar_lugar.html', {'form': form})

# Ver detalles del lugar + comentarios
def lugar_detalle(request, id):
    lugar = get_object_or_404(LugarTuristico, id=id)
    comentarios = lugar.comentarios.order_by('-creado_el')

    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.lugar = lugar
            comentario.save()
            return redirect('lugar_detalle', id=lugar.id)
    else:
        form = ComentarioForm()

    return render(request, 'turista/lugar_detalle.html', {
        'lugar': lugar,
        'comentarios': comentarios,
        'form': form
    })

# Editar lugar
@permission_required('turista.change_post', login_url='error_403')
def editar_lugar(request, id):
    lugar = get_object_or_404(LugarTuristico, id=id)
    if request.method == 'POST':
        form = LugarForm(request.POST, request.FILES, instance=lugar)
        if form.is_valid():
            form.save()
            return redirect('catalogo')
    else:
        form = LugarForm(instance=lugar)
    return render(request, 'turista/editar_lugar.html', {'form': form})

# Eliminar lugar
@permission_required('turista.delete_post', login_url='error_403')
def eliminar_lugar(request, id):
    lugar = get_object_or_404(LugarTuristico, id=id)
    if request.method == 'POST':
        lugar.delete()
        return redirect('catalogo')
    return render(request, 'turista/eliminar_lugar.html', {'lugar': lugar})

def acerca(request):
    return render(request, 'turista/acerca.html')

def contacto(request):
    return render(request, 'turista/contacto.html')

def blog(request):
    return render(request, 'turista/blog.html')

@login_required
def mi_agenda(request):
    agenda = AgendaViajes.objects.filter(usuario=request.user).order_by('fecha_planificada')
    return render(request, 'turista/mi_agenda.html', {'agenda': agenda})

# ⭐ Vista de lugares favoritos
@login_required
def lugares_favoritos(request):
    favoritos = AgendaViajes.objects.filter(usuario=request.user, es_favorito=True)
    return render(request, 'turista/favoritos.html', {'favoritos': favoritos})

# 📆 Vista de próximos viajes
@login_required
def proximos_viajes(request):
    hoy = timezone.now().date()
    proximos = AgendaViajes.objects.filter(usuario=request.user, fecha_planificada__gte=hoy)
    return render(request, 'turista/proximos.html', {'proximos': proximos})

# ➕ Agregar lugar a agenda
@login_required
def agregar_a_agenda(request, lugar_id):
    lugar = get_object_or_404(LugarTuristico, id=lugar_id)

    if AgendaViajes.objects.filter(usuario=request.user, lugar=lugar).exists():
        messages.info(request, "Este lugar ya está en tu agenda.")
    else:
        AgendaViajes.objects.create(
            usuario=request.user,
            lugar=lugar,
            fecha_planificada=timezone.now().date()
        )
        messages.success(request, "Lugar agregado a tu agenda.")

    return redirect('mi_agenda')

# ✅ Marcar o desmarcar favorito
@login_required
def marcar_favorito(request, agenda_id):
    agenda = get_object_or_404(AgendaViajes, id=agenda_id, usuario=request.user)
    agenda.es_favorito = not agenda.es_favorito
    agenda.save()
    return redirect('mi_agenda')

@login_required
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(AgendaViajes, id=agenda_id, usuario=request.user)

    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            messages.success(request, "Fecha actualizada correctamente.")
            return redirect('mi_agenda')
    else:
        form = AgendaForm(instance=agenda)

    return render(request, 'turista/editar_agenda.html', {'form': form})

@login_required
def eliminar_agenda(request, agenda_id):
    agenda = get_object_or_404(AgendaViajes, id=agenda_id, usuario=request.user)

    if request.method == 'POST':
        agenda.delete()
        messages.success(request, "Lugar eliminado de tu agenda.")
        return redirect('mi_agenda')

    return render(request, 'turista/eliminar_agenda.html', {'agenda': agenda})

def filtrar_lugares(request):
    categoria = request.GET.get('categoria')
    ubicacion = request.GET.get('ubicacion')
    lugares = LugarTuristico.objects.all()

    if categoria:
        lugares = lugares.filter(categoria=categoria)
    if ubicacion:
        lugares = lugares.filter(ubicacion__icontains=ubicacion)

    return render(request, 'turista/catalogo_filtrado.html', {
        'lugares': lugares,
        'categorias': CATEGORIAS,
        'categoria': categoria,
        'ubicacion': ubicacion
    })