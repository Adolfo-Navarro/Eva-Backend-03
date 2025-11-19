from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservaForm
from .models import Sala

# Create your views here.
def home(request):
    # Pasar dos listas separadas: disponibles y reservadas
    salas_disponibles = Sala.objects.filter(disponible=True).order_by('nombre')
    salas_reservadas = Sala.objects.filter(disponible=False).order_by('nombre')
    return render(request, 'home.html', {
        'salas_disponibles': salas_disponibles,
        'salas_reservadas': salas_reservadas,
    })

def detalle_sala(request, id):
    try:
        sala = Sala.objects.get(id=id)
    except Sala.DoesNotExist:
        sala = None
    return render(request, 'detalle_sala.html', {'sala': sala})


def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                reserva = form.save()
                messages.success(request, f'¡Reserva creada exitosamente! RUT: {reserva.rut_persona}, Sala: {reserva.sala.nombre}')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Error al crear la reserva: {str(e)}')
    else:
        form = ReservaForm()
    
    return render(request, 'crear_reserva.html', {'form': form})