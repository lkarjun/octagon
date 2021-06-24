from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from typing import List
import Schemas, database, models
router = APIRouter()

get_db = database.get_db

@router.post('/create_hod', tags=['Admin'], status_code=status.HTTP_201_CREATED, response_model=Schemas.ShowHods)
async def create_hod(request: Schemas.CreateHod, db: Session = Depends(get_db)):
    new_hod = models.Hod(name = request.name, email = request.email, \
                        phone_num = request.phone_num, user_name = request.user_name, \
                        department = request.department)
    db.add(new_hod)
    db.commit()
    db.refresh(new_hod)
    return new_hod


@router.delete('/delete_hod/{name}/{department}', tags=['Admin'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(name:str, department: str, db: Session = Depends(get_db)):
    hod = db.query(models.Hod).filter(and_(models.Hod.name == name,
                                models.Hod.department == department))
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {name} and department: {department}") 

    hod.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)

@router.put('/edit_hod/{user_name}', tags=['Admin'], status_code=status.HTTP_202_ACCEPTED)
async def edit_hod(user_name: str, request: Schemas.CreateHod, db: Session = Depends(get_db)):
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name)
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with {user_name}") 
    hod.update(dict(request))
    db.commit()
    return "Done"

@router.get('/hods', tags=['Admin'], status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowHods])
async def hods_full_details(db: Session = Depends(get_db)):
    hods = db.query(models.Hod).all()
    if not hods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return hods

@router.get('/hods/{user_name}', tags = ['Admin'], status_code=status.HTTP_202_ACCEPTED, response_model=Schemas.ShowHods)
async def hod_detail(db: Session = Depends(get_db), user_name = None):
    if user_name is None: return 'Please pass hod name to get details'
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name).first()
    if not hod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = f'THERE IS NO HOD IN USER NAME: {user_name}')
    return hod