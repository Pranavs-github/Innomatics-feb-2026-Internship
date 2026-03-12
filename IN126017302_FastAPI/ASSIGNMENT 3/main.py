from fastapi import FastAPI, HTTPException

app = FastAPI()

# initial product list
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 199, "category": "Stationery", "in_stock": True},
]


# -------------------------
# GET ALL PRODUCTS
# -------------------------
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


# -------------------------
# POST PRODUCT
# -------------------------
@app.post("/products")
def add_product(product: dict):

    for p in products:
        if p["name"].lower() == product["name"].lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_id = max(p["id"] for p in products) + 1
    product["id"] = new_id

    products.append(product)

    return {"message": "Product added", "product": product}


# -------------------------
# Q5 INVENTORY AUDIT
# -------------------------
@app.get("/products/audit")
def inventory_audit():

    total_products = len(products)

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p["name"] for p in products if not p["in_stock"]]

    total_value = sum(p["price"] * 10 for p in in_stock)

    expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock),
        "out_of_stock_names": out_stock,
        "total_stock_value": total_value,
        "most_expensive": expensive
    }



# -------------------------
# BONUS DISCOUNT
# -------------------------
@app.put("/products/discount")
def discount(category: str, discount_percent: int):

    updated = []

    for p in products:
        if p["category"].lower() == category.lower():

            new_price = int(p["price"] * (1 - discount_percent / 100))
            p["price"] = new_price
            updated.append(p)

    if not updated:
        return {"message": "No products found in that category"}

    return {"updated_products": updated}


# -------------------------
# GET PRODUCT BY ID
# -------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")


# -------------------------
# PUT UPDATE PRODUCT
# -------------------------
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    for p in products:

        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return {"message": "Product updated", "product": p}

    raise HTTPException(status_code=404, detail="Product not found")


# -------------------------
# DELETE PRODUCT
# -------------------------
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return {"message": f"Product '{p['name']}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")




