import os
from sqlalchemy import select, insert

from Tools.Database.Conn import Database
from Tools.Utils.Helpers import get_input_data
from Tools.Classes.BasicTools import BasicTools
from Tools.Classes.CustomError import CustomError
from Models.Products import ProductsModel
from Models.TypesProducts import TypesProductsModel


class Products:

    def __init__(self) -> None:
        self.user_pool = os.getenv('USER_POOL')
        self.client_id = os.getenv('CLIENT_ID')
        self.tools = BasicTools()
        self.db = Database()

    def create_product(self, event):

        input_data = get_input_data(event)
        print(f'{input_data} <----- input_data')

        name = input_data.get('name', '')
        price = input_data.get('price', '')
        type_product_id = input_data.get('type_product_id', '')
        description = input_data.get('description', '')

        values = [
            self.tools.params('name', str, name),
            self.tools.params('type_product_id', int, type_product_id),
            self.tools.params('price', int, price),
            self.tools.params('description', str, description)
        ]

        is_valid = self.tools.validate_input_data(values)
        if not is_valid['is_valid']:
            raise CustomError(is_valid['data'][0])

        type_product_data = self.validate_type_product({
            'type_product_id': type_product_id
        })

        print(f'{type_product_data} <---- type_product_data')

        statement = insert(ProductsModel).values(
            name=name,
            price=price,
            type_product_id=type_product_id,
            description=description
        )

        result_statement = self.db.insert_statement(statement)

        result_statement.update({"message": "Product was created."})
        data = result_statement

        status_code = 200
        # data = ''

        return {
            'statusCode': status_code, 'data': data
        }

    def get_product(self, event):

        input_data = get_input_data(event)
        conditions = {'active': 1}

        product_id = input_data.get('product_id', '')

        if product_id:
            conditions.update({
                'product_id': product_id
            })

        statement = select(ProductsModel).filter_by(**conditions)

        result_statement = self.db.select_statement(statement)

        if not result_statement:
            raise CustomError(
                'The specified product does not exist.'
            )
            # return result_statement[0]

        status_code = 200
        data = result_statement
        # data = ''

        return {
            'statusCode': status_code, 'data': data
        }

    def validate_type_product(self, kwargs):

        conditions = {'active': 1}

        for key, value in kwargs.items():
            conditions.update({key: value})

        statement = select(TypesProductsModel).filter_by(**conditions)

        result_statement = self.db.select_statement(statement)

        if result_statement:
            return result_statement[0]

        raise CustomError(
            'The specified product does not exist.'
        )

    def create_type_product(self, event):

        input_data = get_input_data(event)
        print(f'{input_data} <----- input_data')

        name = input_data.get('name', '')
        description = input_data.get('description', '')

        values = [
            self.tools.params('name', str, name),
            self.tools.params('description', str, description)
        ]

        is_valid = self.tools.validate_input_data(values)
        if not is_valid['is_valid']:
            raise CustomError(is_valid['data'][0])

        statement = insert(TypesProductsModel).values(
            name=name,
            description=description
        )

        result_statement = self.db.insert_statement(statement)

        result_statement.update({"message": "Type product was created."})
        data = result_statement

        status_code = 200
        # data = ''

        return {
            'statusCode': status_code, 'data': data
        }

    def get_type_product(self, event):

        input_data = get_input_data(event)
        conditions = {'active': 1}

        type_product_id = input_data.get('type_product_id', '')

        if type_product_id:
            conditions.update({
                'type_product_id': type_product_id
            })

        statement = select(TypesProductsModel).filter_by(**conditions)

        result_statement = self.db.select_statement(statement)

        if not result_statement:
            raise CustomError(
                'The specified type product does not exist.'
            )
            # return result_statement[0]

        status_code = 200
        data = result_statement
        # data = ''

        return {
            'statusCode': status_code, 'data': data
        }
