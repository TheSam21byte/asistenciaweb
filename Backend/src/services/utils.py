import hashlib
import unicodedata

def strip_accents(s: str) -> str:
    if not s:
        return s
    nfkd = unicodedata.normalize('NFD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

def generar_hash_path(path: str) -> str:
    return hashlib.sha256(path.encode()).hexdigest()
