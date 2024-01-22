from django.shortcuts import render,redirect,get_object_or_404
from cursos.models import Curso
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

#Libreria que nos ayuda a condicionar el acceso a la pagina de checkt out
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import redirect

from accounts2.forms import UserProfileForm, UserForm
from accounts2.models import  UserProfile,Account




def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


@login_required
def add_cart(request, curso_id):
    curso = Curso.objects.get(id=curso_id)

    # Obtén o crea el carrito asociado al usuario actual
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'cart_id': request.session.session_key})

    try:
        cart_item = CartItem.objects.get(curso=curso, cart=cart)
        cart_item.quantity = 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            curso=curso,
            quantity=1,
            cart=cart,
            user=request.user,
            nota= 0
        )
        messages.success(request, f'Curso "{curso.nombre}" asignado correctamente.')

    return redirect('cart')


@login_required
def remove_cart_item(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Obtén el carrito asociado al usuario actual
    cart = Cart.objects.get(user=request.user)
    # Obtén el CartItem y elimínalo
    cart_item = get_object_or_404(CartItem, curso=curso, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart=Cart.objects.get(user=request.user)
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        #Saber el precio total de mis cursos
        for cart_item in cart_items:
                    # llamamos al campo 'curso' de mi clase CartItem
            total += cart_item.curso.costo
            #cantidad total de cursos
            quantity += cart_item.quantity   
    # si no encontramos los valores
    except ObjectDoesNotExist:
        print("error")
        pass #ignora la axception
    #dic indicar que  valores son los que se tiene que enviar al template cart  

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request, 'cursos/cursos_asignados.html', context)



#condicion para la funcion check_out
#@login_required(login_url='login')

def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        cart=Cart.objects.get(user=request.user)#cart_id=_get_cart_id(request)
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        user = request.user        
        # Verifica que el usuario sea autenticado y tiene el modelo Account
        if user.is_authenticated and hasattr(user, 'account'):
            # Llama al método para asignar cursos
            user.account.asignar_cursos()

        #Saber el precio total de mis cursos
        for cart_item in cart_items:
                    # llamamos al campo 'curso' de mi clase CartItem
            total += cart_item.curso.costo
            #cantidad total de cursos
            quantity += cart_item.quantity   
    # si no encontramos los valores
    except ObjectDoesNotExist:
        print("error")
        pass #ignora la axception
    #dic indicar que  valores son los que se tiene que enviar al template cart  
    try:
        userprofile = UserProfile.objects.get(user_id= request.user.id)
    except UserProfile.DoesNotExist:
        userprofile = None
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'userprofile':userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)



def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user= request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su informacion fue guardada con exito')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form= UserProfileForm(instance=userprofile)
    context ={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)



def dashboard_catedratico(request):
    # Obtener el catedrático que ha iniciado sesion
    try:
        user = request.user
        cursos_asociados = Curso.objects.filter(catedratico=user)

    except ObjectDoesNotExist:
        print("Error")
        pass
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None
    quantity = 1

    context = {     
        'quantity':quantity,
        'cursos_asociados': cursos_asociados,
        'userprofile':userprofile,
    }
    
    return render(request,'accounts/dashboard_catedratico.html',context)


'''def asignar_cursos(request):
    # Obtén el usuario actual
    user = request.user
    # Verifica que el usuario sea autenticado y tiene el modelo Account
    if user.is_authenticated and hasattr(user, 'account'):
        # Llama al método para asignar cursos
        user.account.asignar_cursos()

    return redirect('dashboard')'''
    




