from io import BytesIO
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse

from model import detect

app = FastAPI()


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post("/detect")
async def upload_image(user_id, image: UploadFile = File(...)):
    try:
        if image.content_type not in ["image/jpeg", "image/png"]:
            return {"message": "Unsupported file type. Use JPEG or PNG.", "data": []}

        image_data = Image.open(BytesIO(await image.read()))
        response = detect(image_data, user_id)

        return {"message": "Success", "data": response}
    except Exception as error_message:
        return {"message": error_message, "data": []}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
