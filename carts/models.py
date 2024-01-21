from django.db import models
from cursos.models import Curso
# Create your models here.
from accounts2.models import Account
from django.contrib.auth import get_user_model

#Estructura del carrito de compra. Padre de Cart_item
class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    cart_id= models.CharField(max_length=250, blank=True)
    date_added= models.DateField(auto_now_add=True)
    asignado =models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user}   ({self.cart_id})"#self.cart_id

 
#Cart_Id o producto selecciona que sera seleccionado y comprado
class CartItem(models.Model):

    #solucion problema de desconexion 
    #Necesitamos que el cartItem tenga una relacion con el usurio
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    #Esto garantiza que no puedas tener duplicados en tu carrito para el mismo curso.
    class Meta:
        unique_together = ('cart', 'curso')

    def sub_total(self):
        return self.curso.costo * self.quantity
    #funcion _str_ devuelve un objeto de tipo strig pero el tipo
    #de objeto que necesitamos es de tipo curso
    def __unicode__(self):
        return self.curso

