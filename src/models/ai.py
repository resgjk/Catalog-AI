from sqlalchemy import ForeignKey, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class AIModel(Base):
    __tablename__ = "ai"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    shor_description: Mapped[str]
    icon: Mapped[str] = mapped_column(default=str(image_to_byte_array()))
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"{self.id=} {self.title=} {self.description=} \
            {self.short_description=} {self.category_id=}"
