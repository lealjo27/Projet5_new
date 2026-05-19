import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from pydantic import BaseModel, EmailStr

# Sécurisation 
SECRET_KEY = os.getenv("SECRET_KEY", "cle_de_secours_temporaire_pour_le_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 3. Indique à FastAPI que la route pour obtenir le jeton s'appellera "/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 4. Modèles pour structurer les Jetons (Tokens)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# 5. Modèles pour structurer un Utilisateur
class User(BaseModel):
    username: str
    email: EmailStr
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str




def get_password_hash(password: str) -> str:
    """Transforme un mot de passe en clair en un hash Bcrypt sécurisé (String)."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare le mot de passe en clair avec sa version hachée sécurisée."""
    try:
        pwd_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False

# 6. Fausse Base de données temporaire
# On y crée l'utilisateur "alice" avec le mot de passe "secret123" haché
fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": get_password_hash("secret123"),
        "disabled": False,
    }
}
# 8. Fonction pour fabriquer le jeton de sécurité (JWT)
def create_access_token(data: dict) -> str:
    """Génère un jeton JWT signé avec la SECRET_KEY qui expire après 30 min."""
    to_encode = data.copy()
    
    # On calcule l'heure d'expiration (heure actuelle + 30 minutes)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # On signe et on encode le jeton
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 9. Le douanier qui vérifie le jeton à chaque requête protégée
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Vérifie le jeton. S'il est valide, renvoie l'utilisateur, sinon bloque l'accès."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # On décode le jeton avec notre clé secrète
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except JWTError:
        # Si le jeton est corrompu ou expiré
        raise credentials_exception
        
    # On cherche l'utilisateur dans notre fausse BDD
    user_dict = fake_users_db.get(token_data.username)
    if user_dict is None:
        raise credentials_exception
        
    # On renvoie l'utilisateur sans son mot de passe
    return User(**user_dict)