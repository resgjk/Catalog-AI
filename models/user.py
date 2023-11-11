from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from default import image_to_byte_array


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(25))
    user_image: Mapped[bytes] = mapped_column(LargeBinary, default=image_to_byte_array)

    def __repr__(self):
        return f"{self.id=} {self.login=} {self.password=} \
            {self.email=}"
