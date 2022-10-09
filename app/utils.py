''' 
    6:09:15
    comes with main_24.py
'''

from  passlib.context import CryptContext #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # telling passlib which hashing algorithm we are using

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)