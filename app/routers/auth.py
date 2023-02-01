from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from app import database, models, utils
from app.schemas import UserLogin

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: UserLogin, db:Session = Depends(database.get_db())):
    user = db.query(models.User).filter_by(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentrials")

    return {"access token":"access token"}
