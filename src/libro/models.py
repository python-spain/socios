from django.db import models
import datetime

CARGOS_JUNTA = (('-', 'Ninguno'),
                ('P', 'Presidente'),
                ('V', 'Vicepresidente'),
                ('T', 'Tesorero'),
                ('S', 'Secretario'),
                ('O', 'Vocal')
                )


class Socio(models.Model):
    """
    Definición del modelo de socios.
    Los campos se definenen a partir de la información que tenemos
    actualmente.
    """

    nsocio = models.CharField(max_length=10, unique=True)
    dni = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    mail = models.EmailField(max_length=75)
    fecha = models.DateField(blank=True, null=True,
                             help_text="Fecha solicitud")
    fecha_aprobacion = models.DateField(blank=True,
                                        null=True)
    is_junta = models.BooleanField(default=False)
    cargo = models.CharField(max_length=1,
                             choices=CARGOS_JUNTA,
                             default='-')
    is_fundador = models.BooleanField(default=False)
    is_activo = models.BooleanField(default=True)
    comentario = models.TextField(blank=True)

    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"

    def __str__(self):
        return self.nombre

    def ultimo_pago(self):
        cuota = self.cuota_set.order_by('-fecha').first()
        if cuota:
            return cuota.fecha.strftime('%d-%m-%y')
        else:
            return 'NA'

    def ultimo_aviso(self):
        dias = self.dias()
        if (type(dias) == str) or (dias < 30):
            ultimo_aviso = self.aviso_set.order_by('-fecha').first()
            if ultimo_aviso:
                return ultimo_aviso.fecha.strftime('%d-%m-%y')
            else:
                return 'NA'
        else:
            return ""

    def dias(self):
        ultima_cuota = self.cuota_set.order_by('-fecha').first()
        if ultima_cuota:
            delta = datetime.datetime.now() - datetime.datetime.fromordinal(
                ultima_cuota.fecha.toordinal())
            return 365 - delta.days
        else:
            return 'NA'

    def genera_aviso(self):
        Aviso.objects.create(socio=self)


class Aviso(models.Model):
    socio = models.ForeignKey(Socio)
    fecha = models.DateField(null=True, blank=True,
                             default=datetime.datetime.now)
    comentario = models.CharField(max_length=60, null=True, blank=True)


class Cuota(models.Model):
    socio = models.ForeignKey(Socio)
    fecha = models.DateField(blank=True)
    importe = models.DecimalField(max_digits=5, decimal_places=2,
                                  default="30.00")

    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"

    def __str__(self):
        return super(Cuota, self).__str__()
