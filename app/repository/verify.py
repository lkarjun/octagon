from fastapi import Request, BackgroundTasks, Response
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_
from repository import Schemas
from security import faceid
from database import database, models
from octagonmail import octagonmail

def verify(request: Request, bg_task: BackgroundTasks, username: str, image1, image2, image3):
    unique_id = request.headers['referer'].split("/")[-1]
    db = database.SessionLocal()
    user = db.query(models.PendingVerificationImage).filter(
                and_(models.PendingVerificationImage.user_username == username,
                     models.PendingVerificationImage.id == unique_id))
    if user.first().hod_or_teacher == 'T':
        user_details = db.query(models.Teachers).filter(models.Teachers.username == username).first()
    else:
        user_details = db.query(models.Hod).filter(models.Hod.user_name == username).first()
    db.close()
    face_status =  faceid.verification_image(username, image1, image2, image3)
    if face_status.status_code == 204:
        user.delete(synchronize_session=False)
        db.commit()
        bg_task.add_task(octagonmail.greeting_mail, username, user_details.name, user_details.email)
    return face_status


def alert_user(request: Schemas.PendingVerification, db: Session, bg_task: BackgroundTasks):
    user = db.query(models.PendingVerificationImage).filter(models.PendingVerificationImage.id == request.username).first()
    bg_task.add_task(octagonmail.verification_mail, "User", user.user_email, request.username)
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