from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import status

from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_email = request.user.email
        end_idx = user_email.find('@')

        user_slug = user_email[:end_idx]
        #cat = request.data.get('cat')
        #print('cat is: ', cat)
        #cat_slug = cat.get('slug')
        #print('cat.get slug is', cat_slug)

        cat_slug = 'category2'

        data = {
            'name': request.data.get('name'),
            'slug': request.data.get('slug'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'image': request.data.get('image')
        }

        print('inside productlist post')
        print('data price is: ', request.data.get('price'))
        print('data image is: ', request.data.get('image'))

        if request.data.get('image'):
            image = request.data.get('image')
            print('yes')
            print(dir(image))
        else:
            print('no image')

        serializer = ProductSerializer(data=data, context={'user_slug': user_slug, 'cat_slug': cat_slug})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemsList(APIView):
    def get(self, request, format=None):
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)


class OrdersList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('Orders list')

        user_email = request.user.email
        end_idx = user_email.find('@')
        user_slug = user_email[:end_idx]
        #product_slug = request.data.get('product_slug')
        #quantity = request.data.get('quantity');

        print('before order serializer')
        #data = {'order_items': request.data.get('data.products')}

        products = request.data.get('products')
        print('products is: ')
        #print(products)



        data = {}
        serializer = OrderSerializer(data=data, context={
            'profile_slug': user_slug,
            'products': products
        })

        if serializer.is_valid():
            print('yes, serializer is valid')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print('Test')

        for i in range(0, len(serializer.data)):
            print(serializer.data[i].get('name'))



        #print(len(serializer.data))
        #print(serializer.data[0].get('name'))
        #print(serializer.data[1].get('name'))


        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
