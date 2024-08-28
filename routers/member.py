# from fastapi import APIRouter, status, Depends
# import repository.group
# import repository.member
# from schemas import group
# from sqlalchemy.orm import Session
# from database import get_db
# import models, oauth2
# import schemas.group
# import schemas.member
# from schemas.user import TokenData
# from datetime import datetime
# import repository, schemas
# import schemas.user



# router = APIRouter(tags=['Members'], prefix="/members")

# @router.post('', status_code=200)
# def create_member_request(group_name: str, db : Session = Depends(get_db)):
#     new_request = models.Member(
        
#     )

# @router.get('', status_code=200)
# def get_admin(group_id:int, db: Session = Depends(get_db)):
#     return repository.member.get_admin(group_id, db)
    
    
    
# @router.get('', status_code=200)
# def get_member(group_id:int, db: Session = Depends(get_db)):
#     return repository.member.get_member(group_id, db)