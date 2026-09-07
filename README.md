# Aplicaciones Web 2026 6to
# Esquema de Base de Datos - La Casa del Gordo
# Base de datos actualizado
erDiagram
    CLIENTES ||--o{ PEDIDOS : "realiza"
    MESAS ||--o{ PEDIDOS : "recibe"
    PEDIDOS ||--|| PAGOS : "genera"
    PEDIDOS ||--|{ DETALLES_PEDIDO : "contiene"
    PLATOS ||--o{ DETALLES_PEDIDO : "incluye"
    CATEGORIAS ||--|{ PLATOS : "clasifica"
    PLATOS ||--o{ MENUS_DIARIOS : "conforma"
    
    CLIENTES {
        UUID id PK
        VARCHAR nombre
        VARCHAR apellido
    }
    MESAS {
        UUID id PK
        INT numero_mesa
        VARCHAR estado
    }
    PEDIDOS {
        UUID id PK
        UUID cliente_id FK
        UUID mesa_id FK
        DECIMAL monto_total
    }
    PAGOS {
        UUID id PK
        UUID pedido_id FK
        DECIMAL monto_pagado
        VARCHAR metodo_pago
    }
    PLATOS {
        UUID id PK
        UUID categoria_id FK
        VARCHAR nombre
        DECIMAL precio
        VARCHAR disponibilidad
    }
    CATEGORIAS {
        UUID id PK
        VARCHAR nombre
    }
