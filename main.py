from enum import Enum
from fastapi import FastAPI, Query, Path, Body, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List, Optional

from helpers.helper import append_to_item
from models.item import Image, Item, Offer
from models.user import UserIn, UserOut, fake_save_user


class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "resnet"
  lenet = "lenet"


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
  content = """
  <body>
  <form action="/files/" enctype="multipart/form-data" method="post">
  <input name="files" type="file" multiple>
  <input type="submit">
  </form>
  <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
  <input name="files" type="file" multiple>
  <input type="submit">
  </form>
  </body>
      """
  return HTMLResponse(content=content)


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
  return {"username": username}


@app.post("/file/")
async def create_file(file: bytes = File(...)):
  return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
  return {"filename": file.filename}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
  return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
  return {"filenames": [file.filename for file in files]}


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
  results = {"item_id": item_id}
  if q:
    results.update({"q": q})
  return results


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#   return fake_items_db[skip: skip + limit]

@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery")):
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
    results.update({"q": q})
  return results


@app.post("/items/")
async def create_item(item: Item):
  item_dict = item.dict()
  if item.tax:
    price_with_tax = item.price + item.tax
    item_dict.update({"price_with_tax": price_with_tax})
  return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
  results = {"item_id": item_id, "item": item}
  return results


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
  user_saved = fake_save_user(user)
  return user_saved


@app.get("/users/me")
async def read_user_me():
  return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
  return {"user_id": user_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
  item = {"item_id": item_id, "owner_id": user_id}
  return append_to_item(q, short, item)


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
  if model_name == ModelName.alexnet:
    return {"model_name": model_name, "message": "Deep Learning FTW!"}

  if model_name.value == "lenet":
    return {"model_name": model_name, "message": "LeCNN all the images"}

  return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
  return {"file_path": file_path}


@app.post("/offers/")
async def create_offer(offer: Offer):
  return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
  return images
