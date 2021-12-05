from fastapi import Request
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_
from starlette.background import BackgroundTasks
from starlette.responses import Response
from repository import Schemas
from security import faceid
from database import database, models


def verify(request: Request, username: str, image1, image2, image3):
    unique_id = request.headers['referer'].split("/")[-1]
    db = database.SessionLocal()
    user = db.query(models.PendingVerificationImage).filter(
                and_(models.PendingVerificationImage.user_username == username,
                     models.PendingVerificationImage.id == unique_id))
    db.close()
    face_status =  faceid.verification_image(username, image1, image2, image3)
    if face_status.status_code == 204:
        user.delete(synchronize_session=False)
        db.commit()
    return face_status


def alert_user(request: Schemas.PendingVerification, db: Session, bg_task: BackgroundTasks):
    import time
    print("COnnection oLay")
    time.sleep(3)
    print("connection okay")
    return Response(status_code=204)

def remove_pending(request: Schemas.PendingVerification, db: Session):
    pending_data = db.query(models.PendingVerificationImage).filter(models.PendingVerificationImage.id == request.username)
    username = pending_data.first().user_username
    if pending_data.first().hod_or_teacher == 'T':
        user = db.query(models.Teachers).filter(models.Teachers.username == username)
    else:
        user = db.query(models.Hod).filter(models.Hod.user_name == username)

    user.delete(synchronize_session=False)
    pending_data.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)