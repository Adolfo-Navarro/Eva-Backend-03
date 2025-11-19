from django import forms
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Reserva, Sala


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['sala', 'rut_persona', 'fecha_hora_inicio']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo salas disponibles
        self.fields['sala'].queryset = Sala.objects.filter(disponible=True)
    
    def clean(self):
        cleaned_data = super().clean()
        sala = cleaned_data.get('sala')
        fecha_hora_inicio = cleaned_data.get('fecha_hora_inicio')
        
        if sala and fecha_hora_inicio:
            # Calcular la hora de término (se asume 2 horas por defecto)
            fecha_hora_termino = fecha_hora_inicio + timedelta(hours=2)
            
            # Verificar conflictos de horarios
            conflictos = Reserva.objects.filter(
                sala=sala,
                estado__in=['pendiente', 'confirmada'],
                fecha_hora_inicio__lt=fecha_hora_termino,
                fecha_hora_termino__gt=fecha_hora_inicio
            )
            
            if conflictos.exists():
                raise ValidationError(
                    f'La sala "{sala.nombre}" ya tiene una reserva en ese horario. '
                    f'Por favor, selecciona otro horario.'
                )
        
        return cleaned_data
