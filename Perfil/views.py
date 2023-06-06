from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


# Create your views here.
    
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None and user.is_superuser:
#             login(request, user)
#             return redirect('/admin')
#         elif user is not None:
#             login(request, user)
#             return redirect('Perfil/perfil.html')  # Redirigir a la página de perfil después del inicio de sesión
        
#         messages.error(request, 'Credenciales de inicio de sesión inválidas')

#     return render(request, 'Perfil/login.html')

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(label='Email', validators=[validate_email])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class VRegistro(View):
#     def get(self, request):
#         form = UserCreationFormWithEmail()
#         return render(request, 'Perfil/crear_usuario.html', {'form': form})
    
#     def post(self, request):
#         form = UserCreationFormWithEmail(request.POST)
#         if form.is_valid():
#             usuario = form.save()
#             login(request, usuario)
#             return redirect('home')  # Redirige a la página del perfil
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#             return render(request, 'Perfil/crear_usuario.html', {'form': form})

class VRegistro(View):
    def get(self, request):
        form = UserCreationFormWithEmail()
        return render(request, 'Perfil/crear_usuario.html', {'form': form})
    
    def post(self, request):
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = False  # Desactiva el usuario hasta que se verifique
            usuario.save()

            # Envío del correo de confirmación
            current_site = get_current_site(request)
            mail_subject = 'Verificación de cuenta'
            message = render_to_string('Perfil/confirmar_cuenta_email.html', {
                'user': usuario,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token': default_token_generator.make_token(usuario),
            })
            send_mail(mail_subject, message, 'eventiketweb@gmail.com', [usuario.email])

            return redirect('vregistro')  # Redirige a la página de confirmación de cuenta
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'Perfil/crear_usuario.html', {'form': form})

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

def perfil(request):
    # Obtén el usuario actual
    usuario = request.user

    # Verifica si se envió el formulario
    if request.method == 'POST':
        # Crea una instancia del formulario con los datos enviados
        formulario = PerfilForm(request.POST, instance=usuario)

        # Valida el formulario
        if formulario.is_valid():
            # Guarda los cambios en el usuario
            formulario.save()
    else:
        # Crea una instancia del formulario con los datos del usuario actual
        formulario = PerfilForm(instance=usuario)

    # Renderiza la plantilla con el formulario y el usuario
    return render(request, "Perfil/perfil.html", {'formulario': formulario, 'usuario': usuario})

def cerrar_sesion(request):
    logout(request)

    return redirect('home')

def logear(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contra=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario,password=contra)
            if usuario is not None and usuario.is_superuser:
                login(request, usuario)
                return redirect('/admin')
            if usuario is not None:
                login(request,usuario)
                return redirect('home')
            else:
                messages.error(request,'Usuario o contraseña incorrectos')
        else:
            messages.error(request,'Usuario o contraseña incorrectos')

    form=AuthenticationForm()
    return render(request, 'Perfil/login.html', {'form':form})

def verificar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('confirmar_cuenta')
    else:
        return render(request, 'verification/verificacion_fallida.html')


def confirmar_cuenta(request):
    return render(request, 'verification/confirmar_cuenta.html')

