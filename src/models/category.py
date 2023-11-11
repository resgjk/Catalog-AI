from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    icon: Mapped[str] = mapped_column(default=str(image_to_byte_array()))

    def __repr__(self):
        return f"{self.id=} {self.title=}"
