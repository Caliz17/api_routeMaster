from .user import User
from .role import Role
from .permission import Permission
from .cliente import Cliente
from .producto import Producto
from .ruta import Ruta
from .ruta_cliente import RutaCliente
from .ruta_asignada import RutaAsignada
from .pedido import Pedido
from .detalle_pedido import DetallePedido
from .entrega import Entrega
from .cobro import Cobro

# Esto asegura que SQLAlchemy conozca todos los modelos
__all__ = ["User", "Role", "Permission", "Cliente", "Producto", "Ruta", "RutaCliente", "RutaAsignada", "Pedido", "DetallePedido", "Entrega", "Cobro"]