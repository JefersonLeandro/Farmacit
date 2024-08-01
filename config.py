
class Config:
    
    # # Conexión local  
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/db_f'
   
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://id21904228_jeferson:1002723384Je.@files.000webhost.com/id21904228_mysql'

    
     
    # Conexion en linea 
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cEf6g3afc6DgHh5gAfBeFgBeFe333aFh@monorail.proxy.rlwy.net:14502/dbFarmacit'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
