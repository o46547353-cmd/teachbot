from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="student") # student, tutor, admin
    
    # Сегментация
    age_group: Mapped[str] = mapped_column(String(20), nullable=True) # kids, teens, adults
    english_level: Mapped[str] = mapped_column(String(5), nullable=True) # A1, A2, B1, B2, C1
    universe_id: Mapped[int] = mapped_column(ForeignKey("universes.id"), nullable=True)
    
    # Репетиторская привязка
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Отношения (self-referential для репетиторов)
    students: Mapped[list["User"]] = relationship("User", backref="tutor", remote_side=[id])
    homeworks: Mapped[list["Homework"]] = relationship("Homework", back_populates="student")

class Universe(Base):
    __tablename__ = "universes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100)) # e.g. "Гарри Поттер"
    category: Mapped[str] = mapped_column(String(50)) # movies, games, niches

class Homework(Base):
    __tablename__ = "homeworks"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quest_name: Mapped[str] = mapped_column(String(100))
    answer_text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending") # pending, accepted, revise
    tutor_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped["User"] = relationship("User", back_populates="homeworks")