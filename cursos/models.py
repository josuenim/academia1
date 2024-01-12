from django.db import models
from accounts2.models import Catedratico
from category.models import Categorias
from django.urls import reverse
# Create your models here.
class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    slug =models.CharField(max_length=100,blank=True)

    costo=models.PositiveIntegerField()
    horario=models.CharField(max_length=20) 
    cupo=models.PositiveIntegerField()
    cat_image=models.ImageField(upload_to= 'photos/cursos')
    descripcion = models.TextField(blank=True)
    is_available= models.BooleanField(default=True)
    creat_date=models.DateTimeField(auto_now_add=True)
    ##ForeignKey#
    profesor = models.ForeignKey(Catedratico, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Categorias,on_delete=models.SET_NULL,null=True)
    ##
    #modified_date=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name='Curso'
        verbose_name_plural = 'Cursos'
    #Manejo de url para los productos de mi catalogo cursos
    def get_url(self):
        #le pasamos a curso_detail lo siguientes argumentos 
        return reverse('curso_detail',args=[self.category.category_slug,self.slug])

    #La data va a ser visible dentro del modulo de administracion de django
    #la data con valor representativo
    def __str__(self):
        return self.nombre
    
# modelo para tallas y colores    
#class Variation(models.Model):
    #curso = models.foreing(Product, on_delete=CASCADE)
    
