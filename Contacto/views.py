from django.shortcuts import redirect, render
from .forms import FormularioContacto
from django.core.mail import EmailMessage

# Create your views here.
def contacto(request):
    if request.user.is_authenticated:
        initial_data = {'email': request.user.email, 'nombre': request.user.username}
    else:
        initial_data = {}

    form = FormularioContacto(initial=initial_data)

    if request.method == 'POST':
        form = FormularioContacto(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            email_message = EmailMessage(
                "Mensaje desde EventiketWeb",
                f"El usuario con nombre {nombre} con la dirección {email}, escribe lo siguiente:\n\n{mensaje}",
                "", ["eventiketweb@gmail.com"],
                reply_to=[email]
            )
            try:
                email_message.send()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?error")

    return render(request, "Contacto/contacto.html", {'miFormulario': form})
