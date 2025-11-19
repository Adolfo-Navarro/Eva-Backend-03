from django.contrib import admin
from .models import Sala, Reserva


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_maxima', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nombre',)
    list_editable = ('disponible',) 
    actions = ['habilitar_salas', 'deshabilitar_salas']
    
    def habilitar_salas(self, request, queryset):
        updated = queryset.update(disponible=True)
        self.message_user(request, f'{updated} sala(s) habilitada(s).')
    habilitar_salas.short_description = "Habilitar salas seleccionadas"
    
    def deshabilitar_salas(self, request, queryset):
        updated = queryset.update(disponible=False)
        self.message_user(request, f'{updated} sala(s) deshabilitada(s).')
    deshabilitar_salas.short_description = "Deshabilitar salas seleccionadas"


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('rut_persona', 'sala', 'fecha_hora_inicio', 'fecha_hora_termino', 'estado')
    list_filter = ('estado', 'sala', 'fecha_hora_inicio')
    search_fields = ('rut_persona',)
    readonly_fields = ('fecha_hora_termino',)