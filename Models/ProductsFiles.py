from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import String, Column, DateTime, Integer

from Tools.Database.Conn import Base


class ProductsFilesModel(Base):

    __tablename__ = 'products_files'

    product_file_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    url = Column(String(500))
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):

        self.product_file_id = kwargs['product_file_id']
        self.product_id = kwargs['product_id']
        self.url = kwargs['url']
        self.active = kwargs['active']
