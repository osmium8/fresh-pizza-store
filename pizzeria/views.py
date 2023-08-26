from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAdminUser
from django.db import transaction
from rest_framework.exceptions import APIException

from pizzeria.serializers import CategorySerializer, ItemSerializer, OrderItemResponseSerializer, OrderItemSerializer, PizzaSerializer
from pizzeria.models import Category, Item, OrderItem, OrderSession, Pizza
from audit.models import OrderHistory, OrderTrackHistory
from audit.serializers import OrderedHistoryDetailSerializer

from audit.tasks import update_status

class PlaceOrderView(APIView):

    def post(self, request):
        order_items = (
            OrderItem.objects.filter(order_session__user__id=request.user.id)
            .prefetch_related("customization")
            .select_related("pizza")
        )

        if (order_items.exists() == False):
            return Response({'status': 'Failed', 'message': 'No Order Item.'}, HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                order_history = OrderHistory.objects.create_order_history(request.user, order_items)
                OrderSession.objects.clear(request.user.id)

                minute = datetime.utcnow() + timedelta(seconds=1)
                transaction.on_commit(lambda: update_status.apply_async((order_history.id, OrderTrackHistory.Status.ACCEPTED), eta=minute))

                serializer = OrderedHistoryDetailSerializer(order_history)
                return Response(serializer.data, HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))
        

class OrderView(APIView):
    serializer_class = OrderItemResponseSerializer

    def get(self, request):
        order_items = OrderItem.objects.filter(order_session__user__id=request.user.id)
        data = OrderItemResponseSerializer(order_items, many=True).data
        return Response(data, HTTP_200_OK)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

class PizzaViewSet(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
