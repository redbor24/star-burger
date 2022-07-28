from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderLines, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_data = request.data

    response_msg = ''
    if 'products' not in order_data:
        response_msg = 'No "Products" key'
    else:
        order_data_products = order_data['products']
        if order_data_products is None:
            response_msg = '"Products" is not present'
        elif type(order_data_products) != list:
            response_msg = '"Products" is not a list'
        elif not order_data_products:
            response_msg = '"Products" list is empty'

    if response_msg:
        answer = {'message': response_msg}
        response_status = status.HTTP_406_NOT_ACCEPTABLE
    else:
        new_order = Order.objects.create(
            order_num=Order.get_new_order_num(),
            first_name=order_data['firstname'],
            last_name=order_data['lastname'],
            phone_number=order_data['phonenumber'],
            delivery_address=order_data['address']
        )
        for num, product in enumerate(order_data['products'], start=1):
            OrderLines.objects.create(
                order=new_order,
                position_num=num,
                product=Product.objects.get(id=product['product']),
                quantity=product['quantity']
            )

        answer = {'order_num': new_order.order_num}
        response_status = status.HTTP_200_OK

    return Response(answer, status=response_status)
