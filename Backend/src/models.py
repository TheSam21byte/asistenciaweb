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
    codigo: str
    id_aula: int
    id_periodo: int
    validado: int
    direccion: str
