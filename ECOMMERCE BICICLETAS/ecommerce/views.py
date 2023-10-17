from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Product
from django.db import models
from .forms import MyValidationForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate


def is_none(*args):
    r = []
    for a in args:
        if a.strip() == '':
            r.append(None)
        else:
            r.append(a)
    return r[0], r[1], r[2], r[3]


def productos(request):

    productos_filtrados = Product.objects.all()

    if request.method == "POST":
        form = MyValidationForm(request.POST)
        if form.is_valid():
            sub_categoria_codigo = request.POST.get('sub_categoria_codigo')
            sub_categoria_nombre = request.POST.get('sub_categoria_nombre')
            producto_codigo = request.POST.get('producto_codigo')
            producto_nombre = request.POST.get('producto_nombre')

            sub_categoria_codigo, sub_categoria_nombre, producto_codigo, producto_nombre = is_none(
                sub_categoria_codigo, sub_categoria_nombre, producto_codigo, producto_nombre)

            copia_productos = productos_filtrados
            mensaje_agregado = False
            try:
                if sub_categoria_codigo:
                    copia_productos = copia_productos.filter(
                        productsubcategoryid__productsubcategoryid=sub_categoria_codigo)
                if sub_categoria_nombre:
                    copia_productos = copia_productos.filter(
                        productsubcategoryid__name=sub_categoria_nombre)
                if producto_codigo:
                    copia_productos = copia_productos.filter(
                        productnumber=producto_codigo)
                if producto_nombre:
                    copia_productos = copia_productos.filter(
                        name=producto_nombre)
            except ValueError:
                mensaje_error = "Datos inválidos"
                if not mensaje_agregado:
                    messages.error(request, mensaje_error)
                    mensaje_agregado = True

                copia_productos = []

            num_registros_filtrados = len(copia_productos)
            if num_registros_filtrados > 0:
                productos_filtrados = copia_productos
                messages.success(
                    request, f"Se han obtenido {num_registros_filtrados} registros")
            else:
                if not mensaje_agregado:
                    messages.error(request, "Datos inválidos")

    productos_con_subcategoria = productos_filtrados.annotate(
        subcategoria_name=models.F('productsubcategoryid__name'))

    context = {'productos': productos_con_subcategoria}
    return render(request, 'ecommerce/datos.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Se ha registrado satisfactoriamente")
            return HttpResponseRedirect("/productos/")
        else:
            messages.error(
                request, "Registro inválido, algunos datos creados no son correctos")
        return HttpResponseRedirect("/register/")

    form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'ecommerce/register.html', context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f'Iniciaste sesión como {username}.')
                return HttpResponseRedirect('/productos/')
            else:
                messages.error(
                    request, 'Nombre de usuario y/o contraseña incorrecta')
                return HttpResponseRedirect('/login/')
        else:
            messages.error(
                request, 'Nombre de usuario y/o contraseña incorrecta')
            return HttpResponseRedirect('/login/')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'ecommerce/login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, "Se ha cerrado la sesión correctamente")
    return HttpResponseRedirect('/login/')
