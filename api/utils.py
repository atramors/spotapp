from passlib.context import CryptContext


class PasswordHasher:
    pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pass_context.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.pass_context.hash(password)


class UserExistException(BaseException):
    pass
