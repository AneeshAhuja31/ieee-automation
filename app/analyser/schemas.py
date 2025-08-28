from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class JSONList(BaseModel):
    json_list: List[Dict[str, Any]]

class CleanedJSON(BaseModel):
    url:str
    caption:str

class EventInfo(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    venue: Optional[str] = None
    registrationType: Optional[str] = None
    actionLinks: Optional[List[str]] = None
    prizes: Optional[List[str]] = None
    description: Optional[str] = None
    isRelevant: bool

class IsSame(BaseModel):
    isSame:bool