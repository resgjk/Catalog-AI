from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from config import DEFAULT_IMG
from db.database import Base
from utils import image_to_byte_array


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(25))
    user_image: Mapped[str] = mapped_column(default=str(image_to_byte_array(DEFAULT_IMG)))

    def __repr__(self):
        return f"{self.id} {self.login} {self.password} {self.email}"
