import bcrypt 

def hash_password(password:str)->str:
    salt = bcrypt.gensalt(15)
    encoded_password = password.encode('utf-8') # encoding the password before hashing
    return bcrypt.hashpw(encoded_password, salt).decode('utf-8')

def verify_password(password:str,hashed_password:str)->bool:
    encoded_password = password.encode('utf-8')
    return bcrypt.checkpw(encoded_password,hashed_password.encode('utf-8'))



#Rules
# In order to save password in database we have to save them in  hashed format
# Hashing Password Logic
# Creating a function that takes password from the user and  returns the password that will be string
# Creates a salt variable and provide the values  bcrypt.salt(15)
#Now from the user password you  convert into utf-8  format since its take only byte format
# Hashing password = bcrypt.hashpw(userpassword.encode('utf-8')(byteformat),gensalt)
#Once the password is Hashed and you will return the password in string format
#Since the password on MongoDb will be saved in string format so you will decode it
#return bcrypt.hashpw(encoded_password,salt).decode('utf-8')


#Verifying Password Logic
# Creating a function that verify password
#function take two paramerter user_password(string) , hashedpasswordfrom mongodb(string)
# Now convert the user-entered password into UTF-8 format
# because bcrypt.checkpw() only accepts bytes.
# Also convert the hashed password from the database into UTF-8 so both inputs are in byte format.
# return bcrypt.check