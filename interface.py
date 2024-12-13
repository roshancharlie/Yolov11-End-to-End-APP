import requests
from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Define the external detect API URL
detect_api_url = "http://0.0.0.0:8080/detect?user_id={}"
index_page = "index.html"
result_page = "result.html"
ui_app = FastAPI()

# Mount static files (CSS, JS)
ui_app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@ui_app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(index_page, {"request": request})


@ui_app.post("/process")
async def process_form(
        request: Request,
        user_name: str = Form(...),
        file: UploadFile = File(...)
):
    try:
        # Validate file type
        if file.content_type not in ["image/jpeg", "image/png"]:
            return templates.TemplateResponse(
                result_page,
                {
                    "request": request,
                    "error": "Unsupported file type. Please upload a JPEG or PNG image.",
                    "message": None,
                    "data": [],
                },
            )

        files = {"image": (file.filename, await file.read(), file.content_type)}

        response = requests.post(detect_api_url.format(user_name), files=files)
        response.raise_for_status()

        # Parse the API response
        response_data = response.json()
        message = response_data.get("message", "No message in response")
        data = response_data.get("data", [])

        return templates.TemplateResponse(
            result_page,
            {"request": request, "message": message, "data": data, "error": None},
        )
    except requests.RequestException as e:
        return templates.TemplateResponse(
            result_page,
            {
                "request": request,
                "error": f"Error contacting detect API: {str(e)}",
                "message": None,
                "data": [],
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "error": f"Unexpected error: {str(e)}",
                "message": None,
                "data": [],
            },
        )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(ui_app, host="0.0.0.0", port=8081)