from fastapi import APIRouter
from src.endpoints import item,customer,product,deposit,bought,entry,preparedSale,sale,deposit,province,report,producttype
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

router = APIRouter()

router.include_router(item.router)
router.include_router(product.router)
router.include_router(customer.router)
router.include_router(deposit.router)
router.include_router(bought.router)
router.include_router(preparedSale.router)
router.include_router(sale.router)
router.include_router(entry.router)
router.include_router(deposit.router)
router.include_router(province.router)
router.include_router(item.router)
router.include_router(producttype.router)
router.include_router(report.router)
