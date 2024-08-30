from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from database import Session_Local, engine
import madels
import schema

madels.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()


# Category CRUD
@app.get('/categories/', response_model=List[schema.Category])
def get_category(db: Session = Depends(get_db)):
    category = db.query(madels.Category).all()
    return category


@app.post('/categories/', response_model=schema.Category)
def create_category(category: schema.CategoryCreate, db: Session = Depends(get_db)):
    category_db = madels.Category(name=category.name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)

    return category_db


# Tag CRUD
@app.get('/tags/', response_model=List[schema.Tag])
def get_tag(db: Session = Depends(get_db)):
    tag = db.query(madels.Tag).all()
    return tag


@app.post('/tags/', response_model=schema.Tag)
def create_tag(tag: schema.TagCreate, db: Session = Depends(get_db)):
    tag_db = madels.Tag(name=tag.name)
    db.add(tag_db)
    db.commit()
    db.refresh(tag_db)

    return tag_db


# Author CRUD
@app.get('/authors/', response_model=List[schema.Author])
def get_author(db: Session = Depends(get_db)):
    author = db.query(madels.Author).all()
    return author


@app.post('/authors/', response_model=schema.Author)
def create_author(author: schema.AuthorCreate, db: Session = Depends(get_db)):
    author_db = madels.Author(
        name=author.name,
        image=author.image,
        profession=author.profession,
        description=author.description,
    )
    db.add(author_db)
    db.commit()
    db.refresh(author_db)

    return author_db


# Post CRUD
@app.get('/posts/', response_model=List[schema.Post])
def get_post(db: Session = Depends(get_db)):
    post = db.query(madels.Post).all()
    return post


@app.post("/posts/", response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    db_post = madels.Post(
        title=post.title,
        image=post.image,
        body=post.body,
        category_id=post.category_id,
        author_id=post.author_id,
    )
    db_post.tags = db.query(madels.Tag).filter(madels.Tag.id.in_(post.tag_ids)).all()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# Comment CRUD
@app.get('/comments/', response_model=List[schema.Comment])
def get_comment(db: Session = Depends(get_db)):
    comment = db.query(madels.Comment).all()
    return comment


@app.post("/comments/", response_model=schema.Comment)
def create_comment(comment: schema.CommentCreate, db: Session = Depends(get_db)):
    db_comment = madels.Comment(
        name=comment.name,
        email=comment.email,
        website=comment.website,
        message=comment.message,
        post_id=comment.post_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# Contact CRUD
@app.get('/contacts/', response_model=List[schema.Contact])
def get_contact(db: Session = Depends(get_db)):
    contact = db.query(madels.Contact).all()
    return contact


@app.post("/contacts/", response_model=schema.Contact)
def create_contact(contact: schema.ContactCreate, db: Session = Depends(get_db)):
    db_contact = madels.Contact(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        message=contact.message,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# ContactInfo CRUD
@app.get("/contact_info/", response_model=List[schema.ContactInfo])
def get_contact_info(db: Session = Depends(get_db)):
    contact_info = db.query(madels.ContactInfo).order_by(madels.ContactInfo.id.desc()).limit(1).all()
    return contact_info


@app.post("/contact-info/", response_model=schema.ContactInfo)
def create_contact_info(contact_info: schema.ContactInfoCreate, db: Session = Depends(get_db)):
    db_contact_info = madels.ContactInfo(
        address=contact_info.address,
        phone=contact_info.phone,
        email=contact_info.email,
        website=contact_info.website,
    )
    db.add(db_contact_info)
    db.commit()
    db.refresh(db_contact_info)
    return db_contact_info
