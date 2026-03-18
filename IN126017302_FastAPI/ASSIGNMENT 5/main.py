from fastapi import FastAPI, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = [
    {"order_id": 1, "customer_name": "Rahul Sharma"},
    {"order_id": 2, "customer_name": "Amit Kumar"},
    {"order_id": 3, "customer_name": "Rahul Verma"},
]

# ---------------------------
# Q1 SEARCH PRODUCTS
# ---------------------------
@app.get("/products/search")
def search_products(keyword: str):

    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {"total_found": len(result), "products": result}


# ---------------------------
# Q2 SORT PRODUCTS
# ---------------------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {"sort_by": sort_by, "order": order, "products": sorted_products}


# ---------------------------
# Q3 PAGINATION
# ---------------------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    paginated = products[start:end]

    total_pages = (len(products) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": paginated
    }


# ---------------------------
# Q4 SEARCH ORDERS
# ---------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):

    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not result:
        return {"message": "No orders found"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# ---------------------------
# Q5 SORT BY CATEGORY + PRICE
# ---------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(products, key=lambda x: (x["category"], x["price"]))

    return {"products": sorted_products}


# ---------------------------
# Q6 COMBINED API
# ---------------------------
@app.get("/products/browse")
def browse_products(
        keyword: str = None,
        sort_by: str = "price",
        order: str = "asc",
        page: int = 1,
        limit: int = 4):

    result = products

    # SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # SORT
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # PAGINATION
    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    total_pages = (len(result) + limit - 1) // limit

    return {
        "total_found": len(result),
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": paginated
    }


# ---------------------------
# BONUS PAGINATE ORDERS
# ---------------------------
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    start = (page - 1) * limit
    end = start + limit

    paginated = orders[start:end]

    total_pages = (len(orders) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "orders": paginated
    }