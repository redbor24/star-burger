from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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
# @permission_classes((permissions.AllowAny,))
def register_order(request):
    order_data = request.data
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

    answer = {
        'success': True,
        'order_num': new_order.order_num
    }
    return Response(answer)
