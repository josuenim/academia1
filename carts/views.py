from django.shortcuts import render,redirect,get_object_or_404
from cursos.models import Curso
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

#Libreria que nos ayuda a condicionar el acceso a la pagina de checkt out
from django.contrib.auth.decorators import login_required


#Funcion para realizar la busqueda de la sesion del usuario actual dentro del browser
# _cart.. guion bajo indicando que es una funcion privada

#Funcion que me permite buscar en mi carrito de compras
#Utilizando como parametro el objeto request.   
def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key  # Deberías actualizar el valor de cart aquí
    return cart

def add_cart(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    
    # Obtén o crea el carrito
    cart_id = _get_cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    try:
        cart_item = CartItem.objects.get(curso=curso, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            curso=curso,
            quantity=1,
            cart=cart,
        )

    return redirect('cart')


def remove_cart_item(request,curso_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    curso =get_object_or_404(Curso,id=curso_id)
    cart_item=CartItem.objects.get(curso=curso,cart=cart)
    cart_item.delete()
    return redirect('cart')     


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        valor=1
        #Saber el precio total de mis cursos
        for cart_item in cart_items:
                    # llamamos al campo 'curso' de mi clase CartItem
            total += cart_item.curso.costo
            #cantidad total de cursos
            quantity += cart_item.quantity   
    # si no encontramos los valores
    except ObjectDoesNotExist:
        valor=0
        print("error")
        pass #ignora la axception
    #dic indicar que  valores son los que se tiene que enviar al template cart  

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'prueba':valor,
    }
    return render(request, 'cursos/cursos_asignados.html', context)


#condicion para la funcion check_out
#@login_required(login_url='login')

def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        valor=1
        #Saber el precio total de mis cursos
        for cart_item in cart_items:
                    # llamamos al campo 'curso' de mi clase CartItem
            total += cart_item.curso.costo
            #cantidad total de cursos
            quantity += cart_item.quantity   
    # si no encontramos los valores
    except ObjectDoesNotExist:
        valor=0
        print("error")
        pass #ignora la axception
    #dic indicar que  valores son los que se tiene que enviar al template cart  

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'prueba':valor,
    }
    return render(request, 'accounts/dashboard.html', context)
    




