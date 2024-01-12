from django.db import models
from django.urls import reverse
# Create your models here.

class Categorias(models.Model):
    category_name=models.CharField(max_length=50)
    description= models.TextField(blank=True)
    category_slug =models.CharField(max_length=100,blank=True)
    cat_image=models.ImageField(upload_to= 'photos/categorias')
    class Meta:
        verbose_name='Categoria'
        verbose_name_plural = 'Categorias'
    #La data va a ser visible dentro del modulo de administracion de django
    #la data con valor representativo
    def get_url(self):
        return reverse('cursos_by_category',args=[self.category_slug])
        #genera la  url localhost:8000/cursos+slug ejutando el evento
        #para hacer la consulta en la base de datos dolviendo la lista de productos
    def __str__(self):
        return self.category_name
    
