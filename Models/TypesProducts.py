from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import String, Column, DateTime, Integer

from Tools.Database.Conn import Base


class TypesProductsModel(Base):

    __tablename__ = 'types_products'

    type_product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):

        self.type_product_id = kwargs['type_product_id']
        self.name = kwargs['name']
        self.description = kwargs['description']
        self.active = kwargs['active']
