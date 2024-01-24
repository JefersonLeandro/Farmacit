# from sqlalchemy import create_engine, Column, Integer, String, Sequence
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Definir el modelo (una tabla en la base de datos)
# Base = declarative_base()

# class Usuario(Base):
#     __tablename__ = 'usuarios'
#     id = Column(Integer, Sequence('usuario_id_seq'), primary_key=True)
#     nombre = Column(String(50))
#     edad = Column(Integer)

# # Modificar la URL de conexión para MySQL
# # Sustituye 'usuario', 'contraseña', 'localhost' y 'nombre_de_base_de_datos' con tus propios valores
# engine = create_engine('mysql+pymysql://root:2hefbFfDEc-HFd1fhc2DhBCCgh-HCB65@monorail.proxy.rlwy.net:20020/Libreria3')

# # Crear las tablas en la base de datos
# Base.metadata.create_all(engine)

# # Crear una sesión de SQLAlchemy
# Session = sessionmaker(bind=engine)
# session = Session()

# # Operaciones CRUD (igual que en el ejemplo anterior)

# # Cerrar la sesión
# session.close()
