from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Sala(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    capacidad_maxima = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
    
    def __str__(self):
        return f"{self.nombre} (Capacidad: {self.capacidad_maxima})"


class Reserva(models.Model):
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    rut_validator = RegexValidator(regex=r'^[0-9\-.]+$', message='RUT sólo puede contener dígitos, guion (-) o punto (.)')
    rut_persona = models.CharField(max_length=12, validators=[rut_validator])
    fecha_hora_inicio = models.DateTimeField(default=timezone.now)
    fecha_hora_termino = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_hora_inicio']
    
    def clean(self):
        
        if self.fecha_hora_termino and self.fecha_hora_inicio:
            duracion = self.fecha_hora_termino - self.fecha_hora_inicio
            if duracion > timedelta(hours=2):
                raise ValidationError('La reserva no puede durar más de 2 horas.')
            if duracion < timedelta(0):
                raise ValidationError('La hora de término debe ser posterior a la hora de inicio.')
    
    def save(self, *args, **kwargs):
        # Calcular fecha_hora_termino automáticamente si no está especificada
        if not self.fecha_hora_termino:
            self.fecha_hora_termino = self.fecha_hora_inicio + timedelta(hours=2)
        
        # Validar las reservas
        self.clean()
        
        # Guardar reservas
        super().save(*args, **kwargs)
        
        # Marcaremos la sala como no disponible si la reserva está activa (pendiente o confirmada)
        if self.estado in ['pendiente', 'confirmada']:
            self.sala.disponible = False
            self.sala.save()
        # Si la reserva se cancela o completa, marcar la sala como disponible nuevamente
        elif self.estado in ['cancelada', 'completada']:
            self.sala.disponible = True
            self.sala.save()
    
    def __str__(self):
        return f"Reserva {self.rut_persona} - {self.sala.nombre} ({self.fecha_hora_inicio})"
