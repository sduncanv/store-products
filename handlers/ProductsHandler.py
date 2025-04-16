from Products.Classes.Products import Products
from Tools.Utils.Helpers import exception_decorator


@exception_decorator
def products(event, context):

    method = event['httpMethod']
    products_class = Products()

    functions = {
        "POST": products_class.create_product,
        "GET": products_class.get_product,
    }

    return functions[method](event)


@exception_decorator
def types_products(event, context):

    method = event['httpMethod']
    products_class = Products()

    functions = {
        "POST": products_class.create_type_product,
        "GET": products_class.get_type_product,
    }

    return functions[method](event)
