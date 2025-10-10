from pydantic import BaseModel

class LoginRequest(BaseModel):
    codigo: str

class EstudianteResponse(BaseModel):
    id_estudiante: int
    codigo: str
    nombres: str
    apellidos: str
    correo_institucional: str
