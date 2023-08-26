from datetime import datetime, timedelta
import json
from celery import shared_task
from audit.models import OrderHistory, OrderTrackHistory


@shared_task
def update_status(order_id: str, status: OrderTrackHistory.Status):
    order_history: OrderHistory = OrderHistory.objects.select_related("track").get(
        id=order_id
    )

    tracking: OrderTrackHistory = order_history.track
    tracking.status = status

    current_time = datetime.now()

    if status == OrderTrackHistory.Status.ACCEPTED:
        tracking.accepted_at = current_time
        minute = datetime.utcnow() + timedelta(seconds=1)
        update_status.apply_async(
            (order_id, OrderTrackHistory.Status.PREPARING), eta=minute
        )
    elif status == OrderTrackHistory.Status.PREPARING:
        tracking.started_preparing_at = current_time
        two_minutes = datetime.utcnow() + timedelta(seconds=1)
        update_status.apply_async(
            (order_id, OrderTrackHistory.Status.DISPATCHED), eta=two_minutes
        )
    elif status == OrderTrackHistory.Status.DISPATCHED:
        tracking.dispatched_at = current_time
        two_minutes = datetime.utcnow() + timedelta(seconds=1)
        update_status.apply_async(
            (order_id, OrderTrackHistory.Status.DELIVERED), eta=two_minutes
        )
    elif status == OrderTrackHistory.Status.DELIVERED:
        tracking.delivered_at = current_time

    tracking.save()
    return json.dumps({"status": "SUCCESS", "message": f"Order Number #{order_id} is {status}"})
