from os import getenv
import boto3
import base64
from botocore.exceptions import ClientError
from sqlalchemy import select, insert, and_

# from Users.Classes.Users import Users
from Tools.Database.Conn import Database
from Tools.Utils.Helpers import get_input_data
from Tools.Classes.BasicTools import BasicTools
from Tools.Classes.AwsTools import AwsTools
from Tools.Classes.CustomError import CustomError
from Models.Products import ProductsModel
from Models.ProductsTypes import ProductsTypesModel
from Models.ProductsFiles import ProductsFilesModel


class Products:

    def __init__(self) -> None:
        self.user_pool = getenv('USER_POOL')
        self.client_id = getenv('CLIENT_ID')
        self.tools = BasicTools()
        self.db = Database()
        # self.users = Users()
        self.aws_tools = AwsTools()

    def create_product(self, event):

        input_data = get_input_data(event)

        name = input_data.get('name', '')
        price = input_data.get('price', '')
        type_product_id = input_data.get('type_product_id', '')
        description = input_data.get('description', '')
        user_id = input_data.get('user_id', '')
        file = input_data.get('file', '')

        values = [
            self.tools.params('name', str, name),
            self.tools.params('type_product_id', int, type_product_id),
            self.tools.params('price', int, price),
            self.tools.params('description', str, description),
            self.tools.params('user_id', int, user_id),
        ]

        if file:

            image = file.get('image', '')
            filename = file.get('filename', '')

            values.extend([
                self.tools.params('file', dict, file),
                self.tools.params('image', str, image),
                self.tools.params('filename', str, filename),
            ])

        is_valid = self.tools.validate_input_data(values)
        if not is_valid['is_valid']:
            raise CustomError(is_valid['data'][0])

        self.validate_type_product({
            'type_product_id': type_product_id
        })

        self.users.get_user_id(**{
            'user_id': user_id
        })

        statement = insert(ProductsModel).values(
            name=name,
            price=price,
            type_product_id=type_product_id,
            description=description,
            user_id=user_id
        )

        result_statement = self.db.insert_statement(statement)
        # print(f'{result_statement} <---- result_statement')

        data_file = {
            'product_id': result_statement['product_id'],
            'model': ProductsFilesModel,
            'image': image,
            'filename': filename
        }

        # if file:
        #     data_file.update({
        #         'image': image,
        #         'filename': filename
        #     })

        result_insert = self.insert_images(**data_file)
        print(f'{result_insert} <---- result_insert')

        result_statement.update({"message": "Product was created."})
        data = result_statement

        status_code = 200

        return {
            'statusCode': status_code, 'data': data
        }

    def get_product(self, event):

        input_data = get_input_data(event)

        conditions = [
            ProductsModel.active == 1
        ]

        product_id = input_data.get('product_id', '')
        user_id = input_data.get('user_id', '')

        if product_id:
            conditions.append(ProductsModel.product_id == product_id,)

        if user_id:
            conditions.append(ProductsModel.user_id == user_id)

        statement = select(
            ProductsModel,
            ProductsFilesModel.url
        ).join(
            ProductsFilesModel,
            and_(
                ProductsFilesModel.product_id == ProductsModel.product_id,
                ProductsFilesModel.active == 1
            ),
            isouter=True
        ).where(*conditions)

        result_statement = self.db.select_statement(statement)
        print(f'{result_statement} ----- result_statement')

        for start in result_statement:

            if start['url'] is None:
                continue

            s3_client = boto3.client('s3')
            start['url'] = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'bucket-store-app',
                    'Key': start['url']
                },
                ExpiresIn=7200
            )

        status_code = 200
        data = result_statement

        if not result_statement:
            status_code = 404

        # status_code = 200
        # data = ''

        return {
            'statusCode': status_code, 'data': data
        }

    def validate_type_product(self, kwargs):

        conditions = {'active': 1}

        for key, value in kwargs.items():
            conditions.update({key: value})

        statement = select(ProductsTypesModel).filter_by(**conditions)

        result_statement = self.db.select_statement(statement)

        if result_statement:
            return result_statement[0]

        raise CustomError(
            'The specified product does not exist.'
        )

    def create_type_product(self, event):

        input_data = get_input_data(event)

        name = input_data.get('name', '')
        description = input_data.get('description', '')

        values = [
            self.tools.params('name', str, name),
            self.tools.params('description', str, description)
        ]

        is_valid = self.tools.validate_input_data(values)
        if not is_valid['is_valid']:
            raise CustomError(is_valid['data'][0])

        statement = insert(ProductsTypesModel).values(
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

        statement = select(ProductsTypesModel).filter_by(**conditions)

        result_statement = self.db.select_statement(statement)

        if not result_statement:
            raise CustomError(
                'The specified type product does not exist.'
            )

        status_code = 200
        data = result_statement

        return {
            'statusCode': status_code, 'data': data
        }

    def insert_images(self, **kwargs):

        bucket_name = getenv('BUCKET_NAME')
        print(bucket_name)

        file = base64.b64decode(kwargs['image'])
        filename = f"product-images/{kwargs['filename']}.png"

        upload_result = self.aws_tools.upload_file(
            data={
                'filename': filename,
                'file': file,
                'bucket_name': bucket_name
            }
        )

        print(upload_result)

        if upload_result['statusCode'] != 200:
            raise CustomError('Error al cargar imagen a S3.')

        result = self.db.insert_statement(
            insert(kwargs['model']).values(
                product_id=kwargs['product_id'],
                url=filename,
            )
        )

        print(result)

        # result.update({"message": "Product was created."})
        # data = result

        status_code = 200

        return {
            'statusCode': status_code, 'data': 'data'
        }

    def upload_file(self, data, object_name=None):

        s3_client = boto3.client('s3')

        try:
            response = s3_client.put_object(
                Body=data['file'],
                Bucket=data['bucket_name'],
                Key=data['filename']
            )
            print(f'{response} ....')

        except ClientError as e:
            print(f'error: {e}')
            raise CustomError(
                f'Error: {e}'
            )

        return {
            'statusCode': 201, 'data': 'data'
        }

    def descargar(self, event):

        s3_client = boto3.client('s3')

        try:
            # response = s3_client.get_object(
            #     Bucket='bucket-store-app',
            #     Key='product-images/archivo2.png'
            # )

            response = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'bucket-store-app',
                    'Key': 'product-images/archivo2.png'
                },
                ExpiresIn=7200
            )

            print(f'{response} ....')

        except ClientError as e:
            print(f'error: {e}')
            raise CustomError(
                f'Error: {e}'
            )

        return {
            'statusCode': 201, 'data': response
        }
