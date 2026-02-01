from fastapi import APIRouter , HTTPException ,Depends
from fastapi import security
from fastapi.security import HTTPBasic ,HTTPBasicCredentials

from .usersmodels import SignUpRequest
from .hashpasswords import hash_password ,verify_password
from ..config.database import users_collection


router = APIRouter()
security = HTTPBasic()


def authenticate(credentials:HTTPBasicCredentials = Depends(security)):
    # finding the user from the database
    user=users_collection.find_one({"username" : credentials.username})
    # Checking that if user does not exist than thorw error
    if not user:
        raise HTTPException(status_code=401,detail= "User does not exist")
    # Checking that if the password of user matches with the password in the database
    if not verify_password(credentials.password,user["password"]):
        raise HTTPException(status_code=401,detail= "Invalid credentials")
    return {"username ":user["username"],"role":user["role"]}

  


@router.post("/signup")
def signup(request:SignUpRequest):
    # Checking if the user already exists in the database
     user=users_collection.find_one({"username" : request.username})
     if user:
        raise HTTPException(status_code=400,detail = "User already exists")
    # Inserting the user into the database by hashing the password 
     users_collection.insert_one({"username":request.username,
                                   "password":hash_password(request.password),
                                   "role":request.role
                          })
     return {"message": "User created successfullly"}
    

    
@router.get("/login")
def login(user = Depends(authenticate)):
        return {"message": f"Welcome user {user["username"]}" ,"role":user["role"]}

    
  