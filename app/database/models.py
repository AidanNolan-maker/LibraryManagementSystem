from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
    )

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    isbn: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    publication_year: Mapped[int | None]

    genre: Mapped[str | None] = mapped_column(
        String(100),
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False,
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    author: Mapped["Author"] = relationship(
        back_populates="books",
    )

    copies: Mapped[list["BookCopy"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )

class BookCopy(Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="AVAILABLE",
    )

    book: Mapped["Book"] = relationship(
        back_populates="copies",
    )

    loans: Mapped[list["Loan"]] = relationship(
        back_populates="book_copy"
    )

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
    )

    membership_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today,
    )

    loans: Mapped[list["Loan"]] = relationship(
        back_populates="member"
    )

class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    copy_id: Mapped[int] = mapped_column(
        ForeignKey("book_copies.id"),
        nullable=False,
    )

    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id"),
        nullable=False,
    )

    checkout_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today,
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    return_date: Mapped[date | None] = mapped_column(
        Date,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    book_copy: Mapped["BookCopy"] = relationship(
        back_populates="loans",
    )

    member: Mapped["Member"] = relationship(
        back_populates="loans",
    )