""" migration of test

Revision ID: f38cca3d716c
Revises: 
Create Date: 2024-07-06 19:02:43.262423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f38cca3d716c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Farmacias',
    sa.Column('idFarmacia', sa.Integer(), nullable=False),
    sa.Column('nitFarmacia', sa.String(length=45), nullable=False),
    sa.Column('nombreFarmacia', sa.String(length=45), nullable=False),
    sa.Column('telefonoFarmacia', sa.String(length=45), nullable=False),
    sa.Column('correoFarmacia', sa.String(length=255), nullable=False),
    sa.Column('ubicacionFarmacia', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('idFarmacia')
    )
    op.create_table('MarcasProductos',
    sa.Column('idMarcaProducto', sa.Integer(), nullable=False),
    sa.Column('nombreMarca', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('idMarcaProducto')
    )
    op.create_table('Roles',
    sa.Column('idRol', sa.Integer(), nullable=False),
    sa.Column('nombreRol', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('idRol')
    )
    op.create_table('Personas',
    sa.Column('idPersona', sa.Integer(), nullable=False),
    sa.Column('nombrePersona', sa.String(length=45), nullable=False),
    sa.Column('apellidoPersona', sa.String(length=45), nullable=False),
    sa.Column('identificacionPersona', sa.String(length=15), nullable=False),
    sa.Column('correoPersona', sa.String(length=255), nullable=False),
    sa.Column('telefonoPersona', sa.String(length=15), nullable=False),
    sa.Column('contrasenaPersona', sa.String(length=256), nullable=False),
    sa.Column('idRol', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idRol'], ['Roles.idRol'], ),
    sa.PrimaryKeyConstraint('idPersona')
    )
    op.create_table('Productos',
    sa.Column('idProducto', sa.Integer(), nullable=False),
    sa.Column('nombreProducto', sa.String(length=45), nullable=False),
    sa.Column('descripcionUnidad', sa.String(length=45), nullable=False),
    sa.Column('descripcionProductoGeneral', sa.String(length=3000), nullable=False),
    sa.Column('stockProducto', sa.Integer(), nullable=False),
    sa.Column('precioProducto', sa.Integer(), nullable=False),
    sa.Column('idMarcaProducto', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idMarcaProducto'], ['MarcasProductos.idMarcaProducto'], ),
    sa.PrimaryKeyConstraint('idProducto')
    )
    op.create_table('CarritoCompras',
    sa.Column('idCarrito', sa.Integer(), nullable=False),
    sa.Column('idPersona', sa.Integer(), nullable=False),
    sa.Column('idProducto', sa.Integer(), nullable=False),
    sa.Column('cantidadCarrito', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idPersona'], ['Personas.idPersona'], ),
    sa.ForeignKeyConstraint(['idProducto'], ['Productos.idProducto'], ),
    sa.PrimaryKeyConstraint('idCarrito'),
    sa.UniqueConstraint('idProducto', 'idPersona')
    )
    op.create_table('Facturas',
    sa.Column('idFactura', sa.Integer(), nullable=False),
    sa.Column('idPersona', sa.Integer(), nullable=False),
    sa.Column('totalCompra', sa.Integer(), nullable=False),
    sa.Column('fechaCompra', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['idPersona'], ['Personas.idPersona'], ),
    sa.PrimaryKeyConstraint('idFactura')
    )
    op.create_table('Imagenes',
    sa.Column('idImagen', sa.Integer(), nullable=False),
    sa.Column('nombreImagen', sa.String(length=255), nullable=False),
    sa.Column('tipoImagen', sa.SmallInteger(), nullable=False),
    sa.Column('idProducto', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idProducto'], ['Productos.idProducto'], ),
    sa.PrimaryKeyConstraint('idImagen')
    )
    op.create_table('ProductosDeseados',
    sa.Column('idProductoDeseado', sa.Integer(), nullable=False),
    sa.Column('idPersona', sa.Integer(), nullable=False),
    sa.Column('idProducto', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idPersona'], ['Personas.idPersona'], ),
    sa.ForeignKeyConstraint(['idProducto'], ['Productos.idProducto'], ),
    sa.PrimaryKeyConstraint('idProductoDeseado'),
    sa.UniqueConstraint('idProducto', 'idPersona')
    )
    op.create_table('DetallesFacturas',
    sa.Column('idDetalleFactura', sa.Integer(), nullable=False),
    sa.Column('cantidadDetalleF', sa.Integer(), nullable=False),
    sa.Column('subtotalDetalleF', sa.Integer(), nullable=False),
    sa.Column('idProducto', sa.Integer(), nullable=False),
    sa.Column('idFactura', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idFactura'], ['Facturas.idFactura'], ),
    sa.ForeignKeyConstraint(['idProducto'], ['Productos.idProducto'], ),
    sa.PrimaryKeyConstraint('idDetalleFactura')
    )
    with op.batch_alter_table('productosdeseados', schema=None) as batch_op:
        batch_op.drop_index('idProducto')

    op.drop_table('productosdeseados')
    op.drop_table('detallesfacturas')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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

    op.drop_table('DetallesFacturas')
    op.drop_table('ProductosDeseados')
    op.drop_table('Imagenes')
    op.drop_table('Facturas')
    op.drop_table('CarritoCompras')
    op.drop_table('Productos')
    op.drop_table('Personas')
    op.drop_table('Roles')
    op.drop_table('MarcasProductos')
    op.drop_table('Farmacias')
    # ### end Alembic commands ###
