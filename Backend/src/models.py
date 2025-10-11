from pydantic import BaseModel

class LoginRequest(BaseModel):
    codigo: str

class EstudianteResponse(BaseModel):
    id_estudiante: int
    codigo: str
    nombres: str
    apellidos: str
    correo_institucional: str

class AccesoData(BaseModel):
    codigo_estudiante: str
    direccion: str
    distancia_s1: float
    distancia_s2: float