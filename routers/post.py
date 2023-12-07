import schemas
import models
import oauth2
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/getall", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    result = db.query(models.Post).all()
    return result


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published)VALUES(%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # newpost = cursor.fetchone()
    # conn.commit()
    newpost = models.Post(owner_id=current_user.id, **post.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # conv_id = str(id)
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (conv_id,))
    #
    # sppost = cursor.fetchone()
    # sppost = db.query(models.Post).filter(models.Post.id == id).first()
    sppost = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                        models.Vote.post_id == models.Post.id,
                                                                                        isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not sppost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with {id} Not Found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":"Not_Found"}
    return sppost


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # conv_id = str(id)
    # cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING*""", (conv_id,))
    # d_post = cursor.fetchone()
    # conn.commit()
    d_post = db.query(models.Post).filter(models.Post.id == id)
    if d_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the {id} is not found")

    if d_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to do this !")

    d_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # conv_id = str(id)
    # cursor.execute("""UPDATE posts SET title = %s,content = %s WHERE id = %s RETURNING*""",
    #                (post.title, post.content, conv_id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)

    if update_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id is not found")
    update_query.update(post.model_dump(), synchronize_session=False)
    if update_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to do this !")

    db.commit()
    return update_query.first()
