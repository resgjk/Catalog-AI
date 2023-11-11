from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class UserAIModel(Base):
    __tablename__ = "user_ai"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    ai_id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        return f"{self.user_id} {self.ai_id}"
