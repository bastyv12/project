from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import LugarTuristico, Comentario
from .forms import  LugarForm, ComentarioForm
from django.contrib.auth import logout

def home(request):
    return render(request, 'turista/home.html')

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


@login_required
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
@login_required
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
@login_required
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
@login_required
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

