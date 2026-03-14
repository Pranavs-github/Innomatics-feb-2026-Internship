from fastapi import FastAPI, HTTPException

app = FastAPI()

# Products database
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "in_stock": True},
]

cart = []
orders = []


# -----------------------------------
# ADD TO CART
# -----------------------------------
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    existing = next((item for item in cart if item["product_id"] == product_id), None)

    if existing:
        existing["quantity"] += quantity
        existing["subtotal"] = existing["quantity"] * existing["unit_price"]
        return {"message": "Cart updated", "cart_item": existing}

    item = {
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": quantity * product["price"]
    }

    cart.append(item)

    return {"message": "Added to cart", "cart_item": item}


# -----------------------------------
# VIEW CART
# -----------------------------------
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": total
    }


# -----------------------------------
# REMOVE ITEM FROM CART
# -----------------------------------
@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed"}

    raise HTTPException(status_code=404, detail="Item not in cart")


# -----------------------------------
# CHECKOUT
# -----------------------------------
@app.post("/cart/checkout")
def checkout(customer_name: str, delivery_address: str):

    if not cart:
        raise HTTPException(status_code=400, detail="CART_EMPTY")

    total = sum(item["subtotal"] for item in cart)

    for item in cart:
        orders.append({
            "order_id": len(orders) + 1,
            "customer_name": customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        })

    cart.clear()

    return {"orders_placed": len(orders), "grand_total": total}


# -----------------------------------
# VIEW ORDERS
# -----------------------------------
@app.get("/orders")
def view_orders():

    return {"orders": orders, "total_orders": len(orders)}