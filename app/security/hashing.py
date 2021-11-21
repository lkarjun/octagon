from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password,plain_password):
        return pwd_context.verify(plain_password,hashed_password)


def get_unique_id(username: str) -> str:
    '''
    get a unique key based on username.
    desc: when a hod or teacher appoint, he/she get a mail to upload 
          his/her photo for login verfication for that the application
          need a unique id based on username
    '''
    key_ = hashlib.sha1(username.encode())
    return key_.hexdigest()

if __name__ == "__main__":
    admin_pass = '$2b$12$PMcz2cegebsN7r7WFcwR1elyaGZf/hZdlwREF5pzsVPHy86e7UwO2'
    print(Hash.verify(admin_pass, 'admin1234'))