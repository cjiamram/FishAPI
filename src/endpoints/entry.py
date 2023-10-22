from fastapi import APIRouter
from fastapi import Query
from src.models.entry import  EntryBase,EntryController,EntryReport
from src.models.Item import ItemController as Item

router = APIRouter(
    prefix="/entry",
    tags=["entry"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root():
    return [{"id": 1}]


@router.post("/receive_item_trans/")
async def receive_item_trans(entry:EntryBase):
    db_control=EntryController()
    result=db_control.receive_item_trans(entry.dict())
    item=Item()
    is_change= item.update_item_cost(entry.item_code)
    result["is_change"]=is_change
    return result

@router.get("/cancel_item_trans/{id}")
async def cancel_item_trans(id):
    db_control=EntryController()
    result=db_control.cancel_item_trans(id)
    return result


@router.get("/search_entry/{keyword}")
async def search_entry(keyword):
    db_control=EntryController()
    result=db_control.search_data(keyword)
    return result

@router.get("/get_report_entry_by_duration/{item_code}")
async def get_report_entry_by_duration(item_code):
    db_control=EntryReport()
    start_length=90
    segment=10
    results=db_control.get_report_entry_by_duration(item_code,start_length,segment)
    return results
