from fastapi import APIRouter
from routers.solution import controller

router = APIRouter(prefix='/fonoma/backend', tags=["solution"])
    
router.add_api_route(
    path="/example",
    endpoint=controller.say_hello,
    methods=["GET"],
)

router.add_api_route(
    path="/solution",
    endpoint=controller.process_orders,
    methods=["POST"],
)