from fastapi import FastAPI
from backend.routes.login import router as login_router
from backend.routes.account import router as account_router
from backend.routes.products import router as products_router
from backend.routes.contact import router as contact_router
from backend.routes.products import router as products_router
from backend.routes.new_product import router as new_product_router
from backend.routes.update_product import router as update_product_router
from backend.routes import new_sale
from backend.routes.delete_product import router as delete_product_router
from backend.routes.recompute_brand import router as recompute_brand_router

app = FastAPI()

# Register routers
app.include_router(login_router)
app.include_router(account_router)
app.include_router(products_router)
app.include_router(contact_router)
app.include_router(products_router)
app.include_router(new_product_router)
app.include_router(update_product_router)
app.include_router(new_sale.router)
app.include_router(delete_product_router)
app.include_router(recompute_brand_router)


@app.get("/")
def root():
    return {"message": "🚀 Welcome to Dynamic Pricing App"}
