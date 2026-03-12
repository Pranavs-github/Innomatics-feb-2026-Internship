from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# -----------------------------
# SAMPLE PRODUCT DATABASE
# -----------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Keyboard", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": True},
]

feedback_list = []

orders = []


# -------------------------------------------------
# Q1 — FILTER PRODUCTS (QUERY PARAMETERS)
# -------------------------------------------------

@app.get("/products/filter")
def filter_products(
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        category: Optional[str] = None):

    result = products

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if category is not None:
        result = [p for p in result if p["category"].lower() == category.lower()]

    return result


# -------------------------------------------------
# Q2 — GET PRODUCT PRICE USING PATH PARAMETER
# -------------------------------------------------

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return {
                "name": p["name"],
                "price": p["price"]
            }

    return {"error": "Product not found"}


# -------------------------------------------------
# Q3 — CUSTOMER FEEDBACK (PYDANTIC + POST)
# -------------------------------------------------

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


@app.post("/feedback")
def submit_feedback(feedback: CustomerFeedback):

    feedback_list.append(feedback)

    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback,
        "total_feedback": len(feedback_list)
    }


# -------------------------------------------------
# Q4 — PRODUCT SUMMARY DASHBOARD
# -------------------------------------------------

@app.get("/products/summary")
def product_summary():

    total_products = len(products)

    in_stock = len([p for p in products if p["in_stock"]])
    out_of_stock = len([p for p in products if not p["in_stock"]])

    most_expensive = max(products, key=lambda x: x["price"])
    cheapest = min(products, key=lambda x: x["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock,
        "out_of_stock_count": out_of_stock,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }


# -------------------------------------------------
# Q5 — BULK ORDER (PYDANTIC + BUSINESS LOGIC)
# -------------------------------------------------

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)
    items: List[OrderItem]


@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    success = []
    failed = []
    total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
            continue

        if not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": "Out of stock"})
            continue

        cost = product["price"] * item.quantity
        total += cost

        success.append({
            "product": product["name"],
            "quantity": item.quantity,
            "cost": cost
        })

    return {
        "company": order.company_name,
        "confirmed": success,
        "failed": failed,
        "grand_total": total
    }
    
# ----------------------------------------
# BONUS — ORDER STATUS TRACKER
# ----------------------------------------

orders_db = []

class Order(BaseModel):
    customer_name: str
    product: str
    quantity: int


# POST /orders
# Create new order with status "pending"
@app.post("/orders")
def create_order(order: Order):

    order_id = len(orders_db) + 1

    new_order = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "product": order.product,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders_db.append(new_order)

    return new_order


# GET /orders/{order_id}
# Get order details
@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders_db:
        if order["order_id"] == order_id:
            return order

    return {"error": "Order not found"}


# PATCH /orders/{order_id}/confirm
# Change status from pending → confirmed
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders_db:

        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return {"message": "Order confirmed", "order": order}

    return {"error": "Order not found"}

