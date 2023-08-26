from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from audit.models import OrderHistory
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from audit.serializers import OrderStatusSerializer

class OrderStatusView(APIView):
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        order_history = OrderHistory.objects.select_related('track').get(id=pk)
        if (order_history.user != request.user):
            raise AuthenticationFailed('You are not allowed to track this order.')
        serializer = OrderStatusSerializer(order_history, many=False)
        return Response(serializer.data, HTTP_200_OK)
