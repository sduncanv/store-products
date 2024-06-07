from Classes.Products import Products
from Tools.Utils.Helpers import exception_decorator


@exception_decorator
def products(event, context):

    products_class = Products()

    methods = {
        "POST": products_class.create_product,
        "GET": products_class.get_product,
        # "PUT": products_class.update_product,
    }

    executed = methods.get(event['httpMethod'])
    return executed(event)


@exception_decorator
def types_products(event, context):

    products_class = Products()

    methods = {
        "POST": products_class.create_type_product,
        "GET": products_class.descargar,
        # "GET": products_class.get_type_product,
        # "PUT": products_class.update_product,
    }

    executed = methods.get(event['httpMethod'])
    return executed(event)
