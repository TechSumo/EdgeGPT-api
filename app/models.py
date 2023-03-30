from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    data: Mapped[Optional[str]] = mapped_column(JSON)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.id"))
    manufacturer: Mapped["Manufacturer"] = relationship(
        back_populates="products")


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    products: Mapped[List[Product]] = relationship(
        back_populates="manufacturer")
