from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    title: Mapped[str]
    full_content: Mapped[str]
    ai_summary: Mapped[str]
    nlp_summary: Mapped[str]
