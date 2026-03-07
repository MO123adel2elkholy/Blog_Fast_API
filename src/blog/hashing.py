from passlib.context import CryptContext

# use a backend without the 72‑byte restriction, or add a check
pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")
# pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        # optional length check/truncation if you stay with bcrypt
        pw_bytes = password.encode("utf-8")
        if len(pw_bytes) > 72:
            # either raise an error or truncate: pw_bytes = pw_bytes[:72]
            raise ValueError("password too long for bcrypt (max 72 bytes)")
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_ctx.verify(plain_password, hashed_password)
