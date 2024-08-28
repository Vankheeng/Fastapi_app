# from sqlalchemy.orm import Session
# from fastapi import Depends
# from database import get_db
# import models


# def get_admin(group_id:int, db: Session = Depends(get_db)):
#     admins = db.query(models.Member).filter(
#         models.Member.group_id == group_id 
#         and models.Member.role == "Admin"
#         ).all()
#     return admins

# def get_member(group_id:int, db: Session = Depends(get_db)):
#     members = db.query(models.Member).filter(
#         models.Member.group_id == group_id 
#         ).all()
#     return members
    