from fastapi.routing import APIRouter
from fastapi.requests import Request
from analyser.schemas import JSONList,CleanedJSON
from fastapi.responses import JSONResponse
from analyser.services import llm_call
router = APIRouter(prefix="/analyse",tags=["analyse"])

@router.post("/jsons")
async def analyse_jsons(request:JSONList):
    request_json_list = request.json_list
    cleaned_json_list = []
    for request_json in request_json_list:
        cleaned_json = {
            "Post Caption":request_json["Post Caption"],
            "Post Image":request_json["Post Image"]
        }
        cleaned_json = CleanedJSON(
            url=request_json["Post Image"],
            caption=request_json["Post Caption"]
        )
        llm_response = await llm_call(cleaned_json)
        cleaned_json_list.append(llm_response.dict())
    
    return JSONResponse(content=cleaned_json_list)

    