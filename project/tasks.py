from datetime import datetime
from celery import shared_task
import audit.models 
# import OrderHistory, OrderTrackHistory

@shared_task
def update_status(order_id: str, status: audit.models.OrderTrackHistory.Status):
    order_history = audit.models.OrderHistory.objects.get(id=order_id).select_related('track')

    tracking: audit.models.OrderTrackHistory = order_history.tracking
    tracking.status = status

    current_time = datetime.now()

    if (status == audit.models.OrderTrackHistory.Status.ACCEPTED):
        tracking.accepted_at = current_time
    elif (status == audit.models.OrderTrackHistory.Status.PREPARING):
        tracking.started_preparing_at = current_time
    elif (status == audit.models.OrderTrackHistory.Status.DISPATCHED):
        tracking.dispatched_at = current_time
    elif (status == audit.models.OrderTrackHistory.Status.DELIVERED):
        tracking.delivered_at = current_time

    tracking.save()
    return 'Success'
