from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from analyser.schemas import JSONList,CleanedJSON
from fastapi.responses import JSONResponse
from analyser.services import llm_call,check_if_description_is_same
from analyser.cloudinary_db import upload_to_cloudinary
from analyser.motor_db import get_all_events,insert_in_collection
router = APIRouter(prefix="/analyse",tags=["analyse"])

@router.post("/jsons")
async def analyse_jsons(request: JSONList):
    request_json_list = request.json_list
    cleaned_json_list = []
    for request_json in request_json_list:
        post_date = request_json["Post Date"]
        cleaned_json = CleanedJSON(
            url=request_json["Post Image"],
            caption=request_json["Post Caption"]
        )
        llm_response = await llm_call(cleaned_json)
        llm_response_dict = llm_response.dict()

        if llm_response.isRelevant:
            event_list = await get_all_events()

            if not event_list:
                print("Event list is empty. Inserting the first event.")
                
                cloudinary_url = await upload_to_cloudinary(request_json["Post Image"])
                llm_response_dict["cloudinary_url"] = cloudinary_url
                insert_in_motor = await insert_in_collection(llm_response_dict)
                if not insert_in_motor["success"]:
                    raise HTTPException(status_code=400, detail="Motor issue")
                cleaned_json_list.append(llm_response_dict)
                continue  

            is_duplicate = False
            for event in event_list:
                if await check_if_description_is_same(event["description"], llm_response.description):
                    print("-----------------Duplicate Found----------------")
                    is_duplicate = True
                    break

            if not is_duplicate:
                llm_response_dict["post_date"] = post_date
                cloudinary_url = await upload_to_cloudinary(request_json["Post Image"])
                llm_response_dict["cloudinary_url"] = cloudinary_url
                insert_in_motor = await insert_in_collection(llm_response_dict)
                if not insert_in_motor["success"]:
                    raise HTTPException(status_code=400, detail="Motor issue")
                cleaned_json_list.append(llm_response_dict)
            else:
                print(f"Skipping duplicate event: {llm_response_dict['title']}")

        print(f"Extracted JSON: ", llm_response_dict)
    return JSONResponse(content=cleaned_json_list)