from models.solutions import OrderList
from utils.logging import get_app_logger
from typing import List, Optional
import json
from fastapi import Body

logger = get_app_logger(name="FONOMA_BACKEND")

def say_hello(name: Optional[str] = None) -> str:
    try:
        msg = "Hello"
        if name:
            msg += f", {name}"

        logger.info(msg)
        return f"{msg} !!!"
    
    except Exception as e:
        logger.error(str(e))
        raise e

def process_orders (order_list: OrderList = Body(...)) -> float:
    try:
        total = 0
        criterion = order_list.criterion
        logger.info(f"criterion: {criterion}")

        for order in order_list.orders:
            if order.status == criterion or criterion == "all":
                total += order.price * order.quantity

        result = round(total, 2)
        logger.info(f"total: {result}")
        return result
    
    except Exception as e:
        logger.error(str(e))
        raise e