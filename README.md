# Readit_FastAPI
FastAPI readit
# READIT website uchun API
Bugungi darsda biz ReadIT sayti uchun fastapi va sqlalchemy yordamida API chiqaramiz. Bunda bizga 'database.py', 'models.py', 'schemas.py' va 'main.py' fayllarimiz kerak bo'ladi

1. database.py: Asinxron SQLAlchemy sozlamalari
Bu fayl ma'lumotlar bazasi bilan bog'lanishni va SQLAlchemy asosidagi asinxron sessiyani sozlash uchun kerak.
```python
# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```
2. models.py: Blog uchun model sozlamalari
Bu yerda Django'dagi models.py faylidagi barcha modellarni FastAPI uchun SQLAlchemy yordamida qayta yozamiz.

```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Many-to-Many relationship uchun yordamchi jadval
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), unique=True, index=True)

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), unique=True, index=True)

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), unique=True, index=True)
    image = Column(String, nullable=True)
    profession = Column(String(212), nullable=True)
    description = Column(Text, nullable=True)

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(212), index=True)
    image = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    author_id = Column(Integer, ForeignKey("authors.id"))
    
    category = relationship("Category", backref="posts")
    author = relationship("Author", backref="posts")
    tags = relationship("Tag", secondary=post_tags, backref="posts")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    name = Column(String(212))
    email = Column(String(212))
    website = Column(String(212), nullable=True)
    message = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    
    post = relationship("Post", backref="comments")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String(212), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ContactInfo(Base):
    __tablename__ = "contact_info"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(212), nullable=False)
    phone = Column(String(212), nullable=False)
    email = Column(String, nullable=False)
    website = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

```
### Izohlar:
* Many-to-Many Relationship: post_tags jadvali Post va Tag o'rtasida ko'pdan-ko'p munosabatni yaratish uchun yordamchi jadval sifatida ishlatilmoqda.
* Relationship: relationship funksiyasi orqali modellar o'rtasidagi bog'lanishlar aniqlangan. Masalan, Post modeli Category, Author, va Tag bilan bog'langan.
* DateTime: created_at va updated_at ustunlari Contact va ContactInfo modellariga qo'shilgan bo'lib, ularga avtomatik sanani kiritish va yangilanish vaqtini belgilash uchun func.now() ishlatilgan.


3. schemas.py: Pydantic asosidagi modellar (serializatorlar)
Bu yerda ma'lumotlarni seriyalashtirish va deserializatsiya qilish uchun kerakli Pydantic modellarini yaratamiz.
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Category schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Tag schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

# Author schemas
class AuthorBase(BaseModel):
    name: str
    image: Optional[str] = None
    profession: Optional[str] = None
    description: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

# Comment schemas
class CommentBase(BaseModel):
    name: str
    email: str
    website: Optional[str] = None
    message: str
    image: Optional[str] = None

class CommentCreate(CommentBase):
    post_id: int

class Comment(CommentBase):
    id: int
    post_id: int

    class Config:
        orm_mode = True

# Post schemas
class PostBase(BaseModel):
    title: str
    image: Optional[str] = None
    body: Optional[str] = None

class PostCreate(PostBase):
    category_id: int
    author_id: int
    tag_ids: List[int]

class Post(PostBase):
    id: int
    category: Category
    author: Author
    tags: List[Tag] = []
    comments: List[Comment] = []

    class Config:
        orm_mode = True

# Contact schemas
class ContactBase(BaseModel):
    name: str
    email: str
    phone: str
    message: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ContactInfo schemas
class ContactInfoBase(BaseModel):
    address: str
    phone: str
    email: str
    website: str

class ContactInfoCreate(ContactInfoBase):
    pass

class ContactInfo(ContactInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

```

### Izohlar:
* BaseModel va orm_mode: Pydantic modellaridan meros olingan va orm_mode = True orqali SQLAlchemy ORM obyektlarini Pydantic modeliga oson konvertatsiya qilish mumkin.

* Optional turlari: Kiritilishi shart bo'lmagan maydonlar Optional bilan belgilangan, masalan, image, profession, va website.

* datetime: Contact va ContactInfo modellarida vaqt maydonlari (created_at va updated_at) uchun datetime moduli ishlatilgan.

* List[int]: PostCreate modelida tag_ids uchun List[int] ishlatilgan, bu ko'pdan-ko'p bog'lanishlar (many-to-many relationships) uchun tag idlarini olishni ta'minlaydi.

4. main.py: FastAPI ilovasi
Bu yerda FastAPI ilovasini yaratamiz va kerakli endpointlar orqali CRUD operatsiyalarini amalga oshiramiz.
```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
import schemas

# Ma'lumotlar bazasini yaratish
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Category CRUD
@app.get("/categories/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Tag CRUD
@app.get("/tags/", response_model=List[schemas.Tag])
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    return tags

@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# Author CRUD
@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(
        name=author.name,
        image=author.image,
        profession=author.profession,
        description=author.description,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

# Post CRUD
@app.get("/posts/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(
        title=post.title,
        image=post.image,
        body=post.body,
        category_id=post.category_id,
        author_id=post.author_id,
    )
    db_post.tags = db.query(models.Tag).filter(models.Tag.id.in_(post.tag_ids)).all()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Comment CRUD
@app.get("/comments/", response_model=List[schemas.Comment])
def get_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    return comments

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = models.Comment(
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
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(
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
@app.get("/contact_info/", response_model=List[schemas.ContactInfo])
def get_contact_info(db: Session = Depends(get_db)):
    contact_info = db.query(models.ContactInfo).order_by(models.ContactInfo.id.desc()).limit(1).all()
    return contact_info

```

### Izohlar:
* Ma'lumotlar Bazasini Yarating: models.Base.metadata.create_all(bind=engine) buyrug'i ma'lumotlar bazasini yaratuvchi bo'lib, har safar ilova ishga tushganda kerakli jadvallar mavjudligini tekshiradi.

* Dependency: get_db() funktsiyasi SessionLocal() dan foydalangan holda yangi sessiyalarni yaratadi va ular tugagach yopadi. Bu funksiyani Depends() yordamida har bir CRUD funksiyasiga sessiyani ta'minlash uchun foydalaniladi.

* CRUD Operatsiyalar: Har bir model uchun GET va POST yo'llari yaratilgan. Bu yo'llar orqali ma'lumotlarni olish va qo'shish mumkin.

* Relationship: Post modeli yaratishda tags many-to-many munosabatlariga tegishli bo'lgani uchun, ular tanlab olinadi va keyinroq db_post.tags ga qo'shiladi.


