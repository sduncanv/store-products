import os
import base64
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
from sqlalchemy import select, insert, and_

from Users.Classes.Users import Users
from Users.Models.Users import UserModel
from Tools.Database.Conn import Database
from Tools.Utils.Helpers import get_input_data
from Tools.Classes.BasicTools import BasicTools
from Tools.Classes.AwsTools import AwsTools
from Tools.Classes.CustomError import CustomError
from Products.Models.Products import ProductsModel
from Products.Models.ProductsTypes import ProductsTypesModel
from Products.Models.ProductsFiles import ProductsFilesModel


class Products:

    def __init__(self) -> None:
        self.tools = BasicTools()
        self.users = Users()
        self.aws_tools = AwsTools()
        self.db = Database(
            db=os.getenv('DATABASE_NAME'),
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD')
        )

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
            raise CustomError(is_valid['errors'][0])

        self.validate_type_product({'type_product_id': type_product_id})

        data_user = self.users.get_user_info({'user_id': user_id})

        if data_user['statusCode'] == 404:
            raise CustomError(
                message='The specified user does not exist.', status_code=400
            )

        statement = insert(ProductsModel).values(
            name=name,
            price=price,
            type_product_id=type_product_id,
            description=description,
            user_id=user_id
        )

        result_statement = self.db.insert_statement(statement)

        data_file = {
            'product_id': result_statement['product_id'],
            'model': ProductsFilesModel
        }

        if file:
            data_file.update({
                'image': image,
                'filename': filename
            })

        # This line is for uploading images to S3:
        # result_insert = self.insert_images(**data_file)

        # This line is for uploading images to Cloudinary:
        result_insert = self.upload_image(**data_file)

        if result_insert['statusCode'] == 200:
            data = result_statement
            status_code = 200

        else:
            raise CustomError('Error al crear el producto')

        return {'statusCode': status_code, 'data': data}

    def get_product(self, event):

        input_data = get_input_data(event)

        conditions = [ProductsModel.active == 1]

        product_id = input_data.get('product_id', '')
        user_id = input_data.get('user_id', '')

        if product_id:
            conditions.append(ProductsModel.product_id == product_id)

        if user_id:
            conditions.append(ProductsModel.user_id == user_id)

        statement = select(
            ProductsModel,
            ProductsFilesModel.url,
            ProductsTypesModel.name.label('product_type_name'),
            UserModel.username,
            UserModel.name,
            UserModel.phone_number,
        ).join(
            ProductsFilesModel,
            and_(
                ProductsFilesModel.product_id == ProductsModel.product_id,
                ProductsFilesModel.active == 1
            ),
            isouter=True
        ).join(
            ProductsTypesModel,
            and_(
                ProductsTypesModel.type_product_id == ProductsModel.type_product_id,
                ProductsTypesModel.active == 1
            )
        ).join(
            UserModel,
            and_(
                UserModel.user_id == ProductsModel.user_id,
                UserModel.active == 1
            )
        ).where(*conditions)

        result_statement = self.db.select_statement(statement)

        # for start in result_statement:

        #     if start['url'] is None:
        #         continue

        #     s3_client = boto3.client('s3')
        #     start['url'] = s3_client.generate_presigned_url(
        #         ClientMethod='get_object',
        #         Params={
        #             'Bucket': 'bucket-store-app',
        #             'Key': start['url']
        #         },
        #         ExpiresIn=7200
        #     )

        status_code = 200
        data = result_statement

        if not result_statement:
            status_code = 404
            data = []

        return {'statusCode': status_code, 'data': data}

    def validate_type_product(self, kwargs: dict):

        conditions = {'active': 1}

        for key, value in kwargs.items():
            conditions.update({key: value})

        statement = select(ProductsTypesModel).filter_by(**conditions)

        result_statement = self.db.select_statement(statement)

        if result_statement:
            return result_statement[0]

        raise CustomError(
            'The specified product type does not exist.'
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
            raise CustomError(is_valid['errors'][0])

        statement = insert(ProductsTypesModel).values(
            name=name,
            description=description
        )

        result_statement = self.db.insert_statement(statement)

        if result_statement:
            data = result_statement
            status_code = 200

        else:
            status_code = 400
            data = 'No se pudo crear el tipo de producto'

        return {'statusCode': status_code, 'data': data}

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

        status_code = 200
        data = result_statement

        if not result_statement:
            status_code = 404
            data = []

        return {'statusCode': status_code, 'data': data}

    def insert_images(self, **kwargs):

        bucket_name = os.getenv('BUCKET_NAME')

        file = base64.b64decode(kwargs['image'])
        filename = f"product-images/{kwargs['filename']}.png"

        upload_result = self.aws_tools.upload_file(
            data={
                'filename': filename,
                'file': file,
                'bucket_name': bucket_name
            }
        )

        if upload_result['statusCode'] != 200:
            raise CustomError('Error al cargar imagen a S3.')

        result = self.db.insert_statement(
            insert(kwargs['model']).values(
                product_id=kwargs['product_id'],
                url=filename
            )
        )

        if result:
            status_code = 200
            data = result

        else:
            status_code = 400
            data = ''

        return {'statusCode': status_code, 'data': data}

    def upload_image(self, **data):

        try:
            cloudinary.config(
                cloud_name=os.getenv('CLOUD_NAME'),
                api_key=os.getenv('API_KEY'),
                api_secret=os.getenv('API_SECRET'),
                secure=True
            )

            base64_image = f"data:image/jpg;base64,{data['image']}"

            cloudinary.uploader.upload(
                base64_image,
                public_id=data['filename'],
                unique_filename=False,
                overwrite=True
            )

            url = CloudinaryImage(data['filename']).build_url()

            result = self.db.insert_statement(
                insert(data['model']).values(
                    product_id=data['product_id'],
                    url=url
                )
            )

            status_code = 200
            data = result

        except cloudinary.exceptions.Error as e:
            status_code = 400
            data = str(e)

        return {'statusCode': status_code, 'data': data}
