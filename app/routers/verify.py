from fastapi import APIRouter, status, Request, Form, File, UploadFile, BackgroundTasks
from templates import OthersTemplates
from repository import verify

router = APIRouter(tags = ['Registration Verification'], prefix='/verify')

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def verify_page(request: Request, id: str):
    return OthersTemplates.verify(request, id)


@router.post('/verification_image', status_code=status.HTTP_204_NO_CONTENT)
async def verification_image(request: Request,
                            bg_task: BackgroundTasks,
                            username: str = Form(...),
                            image1: UploadFile = File(...),
                            image2: UploadFile = File(...),
                            image3: UploadFile = File(...)):
    image1, image2, image3 = await image1.read(), await image2.read(),\
                                await image3.read()
    return verify.verify(request,bg_task, username, image1, image2, image3)