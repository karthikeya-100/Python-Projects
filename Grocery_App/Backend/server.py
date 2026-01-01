from fastapi import FastAPI
from pydantic import BaseModel

import db_helper

app = FastAPI()

class GroceryItem(BaseModel):
    grocery_item: str
    quantity_value :float
    quantity_unit : str
    place_bought : str

@app.get("/groceries/{month}/{year}")
def return_groceries(month,year):
    groceries = db_helper.fetch_groceries(month,year)
    return groceries

@app.post("/groceries/{month}/{year}")
def insert_groceries(month:int,year:int,grocery:GroceryItem):
    print(type(month))
    print(type(year))
    grocery_id = db_helper.insert_grocery(month,year,grocery.grocery_item,grocery.quantity_value,grocery.quantity_unit,
                             grocery.place_bought)
    return {"grocery_id": grocery_id}

@app.delete("/groceries/{grocery_id}")
def delete_grocery(grocery_id:int):
    db_helper.delete_grocery(grocery_id)
    return "Grocery delete successfully"

@app.patch("/groceries/{bought_value}/{grocery_id}")
def update_is_bought(bought_value,grocery_id):
    db_helper.handle_is_bought(bought_value,grocery_id)
    return "Bought value updated successfully"

@app.patch("/groceries/{grocery_id}/{month}/{year}")
def update_grocery(grocery_id:int,grocery:GroceryItem):
    db_helper.update_grocery(grocery_id,grocery.grocery_item,grocery.quantity_value,grocery.quantity_unit
                             ,grocery.place_bought)
    return "Grocery update successfully"