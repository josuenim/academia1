from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name,email,username,password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')
        if not username:
            raise ValueError('El usuario debe tener un username')
        #self.model, que generalmente se utiliza cuando el administrador se instancia
        user=self.model(
            email=self.normalize_email(email),
            username = username,
            first_name= first_name,
            last_name = last_name,                                                
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username,password):
        user=self.create_user(
            email = self.normalize_email(email),
            username =username,
            password = password,
            first_name=first_name,  
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.CharField(max_length=100,unique=True)
    phone_number= models.CharField(max_length=50,blank=True)
    dpi = models.CharField(max_length=15,null=True)
    #formato de fecha es "YYYY-MM-DD"
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    is_account =models.BooleanField(default=False)
    is_catedratico =models.BooleanField(default=False)
    asignado = models.BooleanField(default = False)


    #Campos Atributos de django
    
    date_joined =models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username','first_name','last_name']

    objects=MyAccountManager()

    # Métodos de la interfaz de permisos
    def get_all_permissions(self, obj=None):
        return set()
    def asignar_cursos(self):
        self.asignado = True
        self.save()
    
    def __str__(self):
        return f'{self.first_name}  {self.last_name}'
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
    

    
class CatedraticoManager(BaseUserManager):
    def create_user(self, nombre, apellido, email, username, password=None):
        if not email:
            raise ValueError('El catedrático debe tener un email')
        if not username:
            raise ValueError('El catedrático debe tener un username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            nombre=nombre,
            apellido=apellido,
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, nombre, apellido, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            nombre=nombre,
            apellido=apellido,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Catedratico(AbstractBaseUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, unique=True)
    dpi = models.CharField(max_length=15, unique=True)
    #curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null= True)

    is_account =models.BooleanField(default=False)
    is_catedratico =models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)  # Agrega este campo
    is_staff = models.BooleanField(default=False)  # Agrega este campo
    is_superadmin = models.BooleanField(default=False)  # Agrega este campo

    objects = CatedraticoManager() 


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido', 'dpi']

    #Al momento de llamar el modelo catedratico los parametros 
    #que se mostraran en el administrador seran nombre y apellido
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
    # Con esta funcion concedmos los permisos necesarios para que 
    # la libreria jazzmin no presente problemas.
    def get_all_permissions(self, obj=None):
        return set()
    

class UserProfile(models.Model):
    user =models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city =models.CharField(blank = True, max_length=20)
    state =models.CharField(blank = True, max_length=20)
    country =models.CharField(blank = True, max_length=20)

    def __str__(self):
        return self.user.first_name
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'