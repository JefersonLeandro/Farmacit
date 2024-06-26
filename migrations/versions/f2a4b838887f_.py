"""empty message

Revision ID: f2a4b838887f
Revises: b38280d4b55a
Create Date: 2024-06-26 19:45:02.870556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f2a4b838887f'
down_revision = 'b38280d4b55a'
branch_labels = None
depends_on = None


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auditoria')
    op.drop_table('detallesfacturas')
    with op.batch_alter_table('carritocompras', schema=None) as batch_op:
        batch_op.drop_index('idProducto')

    op.drop_table('carritocompras')
    op.drop_table('marcasproductos')
    op.drop_table('facturas')
    op.drop_table('productos')
    op.drop_table('personas')
    with op.batch_alter_table('productosdeseados', schema=None) as batch_op:
        batch_op.drop_index('idProducto')

    op.drop_table('productosdeseados')
    op.drop_table('farmacias')
    op.drop_table('imagenes')
    op.drop_table('roles')
    # ### end Alembic commands ###


def  upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('idRol', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombreRol', mysql.VARCHAR(length=45), nullable=False),
    sa.PrimaryKeyConstraint('idRol'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('imagenes',
    sa.Column('idImagen', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombreImagen', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('tipoImagen', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=False),
    sa.Column('idProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idImagen'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('farmacias',
    sa.Column('idFarmacia', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nitFarmacia', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('nombreFarmacia', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('telefonoFarmacia', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('correoFarmacia', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('ubicacionFarmacia', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('idFarmacia'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('productosdeseados',
    sa.Column('idProductoDeseado', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('idPersona', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('idProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idProductoDeseado'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    with op.batch_alter_table('productosdeseados', schema=None) as batch_op:
        batch_op.create_index('idProducto', ['idProducto', 'idPersona'], unique=True)

    op.create_table('personas',
    sa.Column('idPersona', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombrePersona', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('apellidoPersona', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('identificacionPersona', mysql.VARCHAR(length=15), nullable=False),
    sa.Column('correoPersona', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('telefonoPersona', mysql.VARCHAR(length=15), nullable=False),
    sa.Column('contrasenaPersona', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('idRol', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idPersona'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('productos',
    sa.Column('idProducto', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombreProducto', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('descripcionUnidad', mysql.VARCHAR(length=45), nullable=False),
    sa.Column('descripcionProductoGeneral', mysql.VARCHAR(length=3000), nullable=False),
    sa.Column('stockProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('precioProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('idMarcaProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idProducto'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('facturas',
    sa.Column('idFactura', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('idPersona', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('totalCompra', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('fechaCompra', sa.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('idFactura'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('marcasproductos',
    sa.Column('idMarcaProducto', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nombreMarca', mysql.VARCHAR(length=45), nullable=False),
    sa.PrimaryKeyConstraint('idMarcaProducto'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('carritocompras',
    sa.Column('idCarrito', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('idPersona', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('idProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('cantidadCarrito', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idCarrito'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    with op.batch_alter_table('carritocompras', schema=None) as batch_op:
        batch_op.create_index('idProducto', ['idProducto', 'idPersona'], unique=True)

    op.create_table('detallesfacturas',
    sa.Column('idDetalleFactura', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('cantidadDetalleF', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('subtotalDetalleF', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('idProducto', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('idFactura', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('idDetalleFactura'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    op.create_table('auditoria',
    sa.Column('idAuditoria', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('accion', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('descripcion', mysql.VARCHAR(length=256), nullable=False),
    sa.PrimaryKeyConstraint('idAuditoria'),
    mysql_default_charset='latin1',
    mysql_engine='MyISAM'
    )
    # ### end Alembic commands ###
