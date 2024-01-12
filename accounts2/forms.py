from django import forms
from .models import Account, Catedratico
import re #Modulo de expresiones regulares

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Password',
        'class': 'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','dpi',
                  'fecha_de_nacimiento','phone_number','username','email','password']
        
    def __init__(self, *args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        #Cada field representa cada caja de texto componente que se tiene registrado
        # mostrar etiquestas en los campos
        self.fields['first_name'].widget.attrs['placeholder']='Ingrese nombre'
        self.fields['last_name'].widget.attrs['placeholder']='Ingrese Apellido'
        self.fields['phone_number'].widget.attrs['placeholder']='Ingrese Telefono' 
        self.fields['email'].widget.attrs['placeholder']='Ingrese email'
        self.fields['fecha_de_nacimiento'].widget.attrs['placeholder']='00/00/00'
        #colocar estilos a los campos
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("El password no coincide!")
        
        if password:
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("La contraseña debe contener al menos 1 dígito.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("La contraseña debe contener al menos 1 letra mayúscula.")
            if not re.search(r'[!@#$%^&*]', password):
                raise forms.ValidationError("La contraseña debe contener al menos 1 símbolo (!@#$%^&*).")


class RegistrationFormCatedratico(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        #               Erro me solicita Username en el formulario,solucion no usarlo aunque este en el model
        #fields = ['nombre','apellido','dpi','email','password']
        fields = ['first_name','last_name','dpi','email','password']
        
    def __init__(self, *args,**kwargs):
        super(RegistrationFormCatedratico,self).__init__(*args,**kwargs)
        #Cada field representa cada caja de texto componente que se tiene registrado
        # mostrar etiquestas en los campos
        self.fields['first_name'].widget.attrs['placeholder']='Ingrese nombre'
        self.fields['last_name'].widget.attrs['placeholder']='Ingrese Apellido'
        self.fields['dpi'].widget.attrs['placeholder']='Ingrese dpi' 
        self.fields['email'].widget.attrs['placeholder']='Ingrese email'
        #colocar estilos a los campos
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
    def clean(self):
        cleaned_data=super(RegistrationFormCatedratico,self).clean()
        password = cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("El password no coincide!")
        
        if password:
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("La contraseña debe contener al menos 1 dígito.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("La contraseña debe contener al menos 1 letra mayúscula.")
            if not re.search(r'[!@#$%^&*]', password):
                raise forms.ValidationError("La contraseña debe contener al menos 1 símbolo (!@#$%^&*).")