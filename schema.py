from pydantic import BaseModel
from typing import List, Optional


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True
