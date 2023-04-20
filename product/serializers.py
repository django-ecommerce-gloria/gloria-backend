from rest_framework import serializers
from authuser.models import Profile

from .models import Category, Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "slug",
            "profile",
            "category",
            "image",
            "get_absolute_url",
            "get_category_url",
            "get_profile_url",
            "get_image",
            "get_thumbnail"
        )

    def create(self, validated_data):

        profile_slug = self.context.get('user_slug')
        profile = Profile.objects.get(slug=profile_slug)

        cat_slug = self.context.get('cat_slug')
        category = Category.objects.get(slug=cat_slug)

        product = Product.objects.create(profile=profile, category=category, **validated_data)

        return product


class CategorySerializer(serializers.ModelSerializer):

    #products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url"

        )


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = OrderItem
        depth = 2
        fields = ('id', 'order', 'product', 'quantity', 'owner',
                 'created_at', 'updated_at', )



class OrderSerializer(serializers.ModelSerializer):

    buyer = serializers.CharField(source='buyer.name', read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('id', 'buyer',
                  'order_items', 'created_at', 'updated_at')

    def create(self, validated_data):
        print('order serial create')

        #order_items = validated_data.pop('order_items')
        #print('order items is:')
        #print(order_items)

        profile_slug = self.context.get('profile_slug')
        profile = Profile.objects.get(slug=profile_slug)

        order = Order.objects.create(buyer=profile)

        products = self.context.get('products')

        for p in products:
            product_slug = p['product_slug']
            quantity = p['quantity']
            product = Product.objects.get(slug=product_slug)
            owner = product.profile
            print(p['product_slug'], ' ', p['quantity'], ' ', product)
            print('Owner is: ', owner)

            OrderItem.objects.create(order=order, product=product, quantity=quantity, owner=owner)

        return order

