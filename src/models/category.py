from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from config import DEFAULT_IMG
from db.database import Base
from utils import image_to_byte_array


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    icon: Mapped[str] = mapped_column(default=str(image_to_byte_array(DEFAULT_IMG)))

    def __repr__(self):
        return f"{self.id} {self.title}"
