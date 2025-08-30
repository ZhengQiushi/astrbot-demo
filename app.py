from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import logging

# Configure logging (optional but highly recommended)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/process_request")
async def process_request(request: Request):
    """
    转发处理 get_req 请求，接收 event 和 user_info，并返回结果。
    """
    try:
        message_str = "test"  # Static value, consider retrieving from request body if needed
        user_name = "test"  # Static value, consider retrieving from request body if needed

        body = await request.json()
        user_info = body.get("user_info")

        if not user_info:
            raise HTTPException(status_code=400, detail="Missing user_info in request body")

        try:
            # Crucially, `user_info` is ALREADY JSON if it comes from request.json()!
            # Remove the redundant json.loads() call.  Attempting to decode a string
            # that's ALREADY a Python dictionary will lead to a TypeError.
            # user_info_dict = json.loads(user_info)  # Incorrect.  Remove this.

            user_info_dict = user_info # Directly use the dictionary

            logger.info(f"Message: {message_str}, User Info: {user_info_dict}")
            result_message = f"Hello, {user_name}, 参数 {user_info_dict}!"

            return JSONResponse({"result": result_message})  # 返回处理后的结果

        except TypeError as e:
            logger.exception(f"Error processing JSON: {user_info}")
            result_message = f"Hello, {user_name}, 处理 JSON 参数时出错: {e}!"
            return JSONResponse({"result": result_message})
        except Exception as e:  # General exception handling *inside* user_info processing
            logger.exception(f"Error processing user_info: {user_info}")
            result_message = f"Hello, {user_name}, 处理 user_info 时出错: {e}!"
            return JSONResponse({"result": result_message})

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        logger.exception("Error processing request")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Example of how to run the server (if you're running this directly)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)