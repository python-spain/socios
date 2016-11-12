from django.contrib import admin
from .models import Socio, Cuota, Aviso
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.db import connection


class SocioResource(resources.ModelResource):
    ultimo_pago = fields.Field()
    dias = fields.Field()

    class Meta:
        model = Socio
        skip_unchanged = True
        report_skipped = True
        fields = ('nsocio', 'dni', 'nombre', 'telefono', 'mail', 'fecha', )
        import_id_fields = ['nsocio', ]
        widgets = {
            'fecha': {'format': '%Y-%m-%d'},
        }

    def dehydrate_ultimo_pago(self, socio):
        return socio.ultimo_pago()

    def dehydrate_dias(self, socio):
        return "{}".format(socio.dias())

    def before_import_row(self, row, **kwargs):
        """
        Suponemos que si no tiene fecha es por que es
        socio fundador
        """
        f = row['fecha'].split('-')
        if len(f) != 3:
            row['fecha'] = '2013-12-07'


class CuotaInline(admin.TabularInline):
    model = Cuota
    extra = 0


class AvisoInline(admin.TabularInline):
    model = Aviso
    extra = 0


def genera_aviso(modeladmin, request, queryset):
    for obj in queryset:
        obj.genera_aviso()
genera_aviso.short_description = 'Genera aviso'


class AvisosFilter(admin.SimpleListFilter):
    """
    Filtro para controlar los vencimientos de las
    cuotas de socio
    """

    title = "Próximas caducidades"

    parameter_name = "dias"

    def lookups(self, request, model_admin):
        return (
            ("-1", "Caducados"),
            ("30", "Próximos"),
            ('NA', "Sin pagos")
        )

    def queryset(self, request, queryset):
        """
        Filtro para controlar los vencimientos de cuotas
        """
        time_range = None

        if self.value() == '-1':
            # Ya vencidos
            time_range = '12 months'
        elif self.value() == '30':
            # Vencidos o a punto de vencer
            time_range = '11 months'
        elif self.value() == 'NA':
            # Socios que no han pagado nunca
            with connection.cursor() as cursor:
                cursor.execute("""select distinct socio_id from libro_cuota""")
                ids = [row[0] for row in cursor.fetchall()]
            return queryset.exclude(id__in=ids)

        if time_range:
            with connection.cursor() as cursor:
                cursor.execute("""select socio_id from libro_cuota group by socio_id
                               having date('now') > date(max(fecha), %s)""", [time_range])
                ids = [row[0] for row in cursor.fetchall()]
            return queryset.filter(id__in=ids)
        else:
            return queryset


@admin.register(Socio)
class SocioAdmin(ImportExportModelAdmin):

    def fecha_alta(self, obj):
        try:
            return obj.fecha.strftime('%b, %Y')
        except AttributeError:
            return 'NA'

    fecha_alta.admin_order_field = 'fecha'
    fecha_alta.short_description = 'Fecha Alta'

    resource_class = SocioResource
    date_hierarchy = 'fecha'
    list_display = ('nsocio', 'nombre', 'mail', 'fecha_alta', 'is_junta',
                    'is_fundador', 'is_activo', 'ultimo_pago', 'dias', 'ultimo_aviso')
    list_filter = ('is_activo', 'is_junta', 'is_fundador', AvisosFilter)
    list_editable = ('is_activo',)
    search_fields = ['nsocio', 'nombre', 'mail']
    inlines = [
        CuotaInline,
        AvisoInline,
    ]
    actions = [genera_aviso, ]
