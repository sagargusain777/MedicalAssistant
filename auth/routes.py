from fastapi import APIRouter , HTTPException ,Depends
from fastapi import security
from fastapi.security import HTTPBasic ,HTTPBasicCredentials

from usersmodels import SignUpRequest
from hashpasswords import hash_password ,verify_password
from config.database import users_collection


router = APIRouter()
security = HTTPBasic()