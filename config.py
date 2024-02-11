
class Config:
    
    # Conexión local  
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/DbFarmacit'
    
    # Conexion en linea 
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:d5HaBfE6EDGCHCgFh62agBceGedeGbDE@roundhouse.proxy.rlwy.net:42758/ProyectoFormativoF'
    
    #hacer el local
    SQLALCHEMY_TRACK_MODIFICATIONS = False
