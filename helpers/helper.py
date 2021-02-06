from typing import Optional


def append_to_item(q: Optional[str], short: bool, item):
    if q:
      item.update({"q": q})
    if not short:
      item.update(
        {"description": "This is an amazing item that has a long description"}
    )
    return item