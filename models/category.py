from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    icon: Mapped[bytes] = mapped_column(LargeBinary())

    def __repr__(self):
        return f"{self.id=} {self.title=}"
