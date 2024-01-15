from django.shortcuts import render,redirect
from .forms import RegistrationForm, RegistrationFormCatedratico
from .models import Account, Catedratico
#from cursos.models import Curso
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

#Importamos la funcion que me permite buscar el carrito de compras
from carts.views import _get_cart_id
from carts.models import Cart, CartItem


# Create your views here.
    #En la funcion register creamos un objeto form basado en 
    # el RegistrationForm(), desemos que se diriga hacia el template html
    # register: es la transaccion de registrar un nuevo usuario en la base de datos
    # utilizando el formulario registro.
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        #valor =0
        form = RegistrationForm(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['first_name']
            apellido = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            dpi = form.cleaned_data['dpi']
            fecha_de_nacimiento = form.cleaned_data['fecha_de_nacimiento']
            password = form.cleaned_data['password']
            user=Account.objects.create_user(first_name=nombre,last_name=apellido,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.dpi=dpi
            user.fecha_de_nacimiento = fecha_de_nacimiento
            user.is_account=True
            user.save()

            #Creacion de activacion del usuario enviando un correo electronico
            current_site= get_current_site(request) # comenzamos indicando cual es la url donde tiene que darle clic este usuario
            #cuando le llegue el contenido del correo electronico

            #titulo de correo electronico que se va a enviar
            mail_subject = 'Activa tu cuenta en la Academia USAC'

            #contenido del  correo electronico
                                    #creacion de template
            body = render_to_string('accounts/account_verificacion_email.html',{
                # Valores  que tienen que pintarse dinamicamente dentro del contenido del mensaje 
                #dentro del template
                'user': user,
                'domain': current_site, # url de mi pagina
                # Enviar identificador para saber que usuario se quiere dar de alta. 
                #Se cifra las clave primaria  urlsafe_base64_encode 
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                #Enviamos un token basado en el objeto user
                'token':default_token_generator.make_token(user),
            })
            #Envio de correo electronico
            to_email = email
            #objeto de que procesa mi correo electronico
            send_email = EmailMessage(mail_subject,body, to = [to_email])
            #send() funcion de envio de email
            send_email.send()

            #messages.success(request,'Se registro el usuario exitosamente')
            #Cuando se registre el usuario y envie el correo electronico
            # se redireccione a la pagina de login con dos valores (command y email)
            return redirect('/accounts2/login/?command=verification&email='+email)
            # Esto acultara el formulario de login
            # indicando que revise mi correo electronico    
            #valor =1
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html',context)




def register_1(request):
    form_1 = RegistrationFormCatedratico()
    #valor = 0
    if request.method == 'POST':
        form_1 = RegistrationFormCatedratico(request.POST)
        #valor = 1
        if form_1.is_valid():
            nombre=form_1.cleaned_data['first_name']
            apellido = form_1.cleaned_data['last_name']
            email = form_1.cleaned_data['email']
            dpi = form_1.cleaned_data['dpi']
            password = form_1.cleaned_data['password']
            #User creado para que se guarde en mi model Catedratico
            username = email.split("@")[0]
            #curso = Curso.objects.get(nombre='Pendiente')
            # create_user crea una instancia del usuario
            user=Catedratico.objects.create_user(nombre=nombre,apellido=apellido,email=email,username=username,password=password)
            user.dpi=dpi
            user.is_catedratico=True
            #user.phone_number='0'
            #user.curso=curso
            user.save()
            #valor = 2
            messages.success(request, 'Se ha enviado la solicitud')
            return redirect('/accounts2/login/?command=verification-catedratico')
        else:
            messages.error(request, 'Formulario no valido')

    context = {
        'form_1': form_1,
        }
    return render(request, 'accounts/register_1.html', context)


def eleccion_usuario(request):
    return render(request, 'accounts/Registro.html')

def pagina_catedratico(request):
    return render(request,'dashboard/catedratico.html')




# Nota: Se debe activar la cuenta (is_active = True) para poder usar el login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_get_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    #Devuelve un arreglo de la coleccion de todos los items
                    #elementos que contiene el carrito de compras
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user= user 
                        item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'Has iniciado sesion exitosamente' )
        #Falta solucionar el is_catedratico
            if user.is_catedratico:  # atributo 'is_catedratico'  modelo Catedratico
                return redirect('home')#pagina_catedratico
            elif user.is_staff:  #  'is_staff' indica administrador
                return redirect('admin:index') #'admin:index'
            elif user.is_account:  # atributo 'is_account'  modelo Account
                return redirect('dashboard')#'pagina_estudiante'
            else:
                return redirect('Home') 

        else:
            messages.error(request, 'Las credenciales son incorrectas')
            return redirect('login')

    return render(request, 'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Has salido de sesion')
    return redirect('login')    


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Felicidades, tu cuenta esta activa!')
        return redirect('login')
    else:
        messages.error(request,'La activacion es invalida')
        return redirect('register')
    


@login_required(login_url ='login')
def pagina_estudiante(request):
    return render(request,'dashboard/estudiante.html')


@login_required(login_url ='login')
def pagina_estudiante(request):
    return render(request,'dashboard/estudiante.html')

@login_required(login_url ='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        #Caputer el parametro email que viene del formulario
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            #Si el usuario existe,obtenemos el usuario de la base de datos
            user=Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Resetear Password'
            body =  render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                # Identificado
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            # indicamos cual es el email el cual va recibir este correo electronico
            to_email= email
            send_email = EmailMessage(mail_subject,body, to=[to_email])
            send_email.send()
            # Generar un mensaje a la pagina disiendo que este correo esta llegando a tu bandeja de entrada
            messages.success(request, 'Un email fue enviado a tu bandeja de entrada para resetear tu password')
            return redirect('login')
        else: 
            messages.error(request, 'La cuenta de usuario no existe')
            return redirect('forgotPassword')


    return render(request,'accounts/forgotPassword.html')

#cuando el usuario reciba un correo electronico dentro del body de este correo
#va a aperecer un link, cuando le de clic a ese link es que se va a ejecutar esta funcion resetpassword_validate
def resetpassword_validate(request, uidb64, token):
    #crear un metodo para poder capturar el uid el parametro  decodificado y tambien el user
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk= uid)
    except (TypeError,ValueError,OverflowError, Account.DoesNotExist):
        user:None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] =uid
        messages.success(request,'Por favor resetea tu Password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'El link ha expirado')
        return redirect('login')
    
#funcion que procese el resetpassword
def resetPassword(request):
    if request.method == 'POST':
        password =request.POST['password']
        confirm_password =request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'El password se reseteo correctamente')
            return redirect('login')
        else:
            messages.erro(request,'El password de confirmacion no concuerda')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')




