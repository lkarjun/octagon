from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password,plain_password):
        return pwd_context.verify(plain_password,hashed_password)


if __name__ == "__main__":
    admin_pass = '$2b$12$PMcz2cegebsN7r7WFcwR1elyaGZf/hZdlwREF5pzsVPHy86e7UwO2'
    print(Hash.verify(admin_pass, 'admin1234'))