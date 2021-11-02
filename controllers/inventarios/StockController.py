from productos.models import Productos
from inventarios.models import Stock
from configuraciones.models import Almacenes

from controllers.DefaultValues import DefaultValues

from django.db import transaction


class StockController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)

        self.table_name = 'registros'
        self.table_id = 'registro_id'

    def update_stock(self, user_perfil, almacen, producto, cantidad):
        """actualizamos el stock"""
        try:
            with transaction.atomic():
                # productos normales
                stock_filter = Stock.objects.filter(almacen_id=almacen, producto_id=producto)
                stock = stock_filter.first()
                if not stock:
                    # creamos el registro
                    stock = Stock.objects.create(almacen_id=almacen, producto_id=producto,
                                                 user_perfil_id=user_perfil, status_id=self.status_activo)

                cantidad_update = stock.cantidad + cantidad
                stock.cantidad = cantidad_update
                stock.save()

            return True

        except Exception as ex:
            print('Error update stock: ' + str(ex))
            self.error_operation = 'Error al actualizar stock, ' + str(ex)
            raise ValueError('Error al actualizar stock del producto, ' + str(ex))

    def stock_producto(self, producto_id, user_perfil, almacen_id):
        """devuelve el stock del producto"""
        try:
            almacen = Almacenes.objects.get(pk=almacen_id)
            producto = Productos.objects.get(pk=producto_id)

            filtros = {}
            filtros['almacen_id'] = almacen
            filtros['cantidad__gt'] = 0
            filtros['producto_id'] = producto
            stock_almacen = Stock.objects.filter(**filtros).order_by('almacen_id')

            return stock_almacen

        except Exception as ex:
            self.error_operation = 'Error al recuperar stock, ' + str(ex)
            raise ValueError('Error al recuperar stock del producto, ' + str(ex))
