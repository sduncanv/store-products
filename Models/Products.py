from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import String, Column, DateTime, Integer

from Tools.Database.Conn import Base


class ProductsModel(Base):

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer)
    type_product_id = Column(Integer)
    description = Column(String(250))
    user_id = Column(Integer)
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):

        self.product_id = kwargs['product_id']
        self.name = kwargs['name']
        self.price = kwargs['price']
        self.type_product_id = kwargs['type_product_id']
        self.description = kwargs['description']
        self.user_id = kwargs['user_id']
        self.active = kwargs['active']
