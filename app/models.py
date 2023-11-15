from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='Admin',
                 username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

        c1 = Category(name='Mobile')
        c2 = Category(name='Tablet')

        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        p1 = Product(name='iPad Pro 2022', price=24000000, category_id=2,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p2 = Product(name='iPhone 13', price=21000000, category_id=1,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p3 = Product(name='Galaxy S23', price=24000000, category_id=1,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p4 = Product(name='Note 22', price=22000000, category_id=1,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p5 = Product(name='Galaxy Tab S9', price=24000000, category_id=2,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p6 = Product(name='iPad Pro 2023', price=24000000, category_id=2,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p7 = Product(name='iPhone 15 Pro', price=21000000, category_id=1,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p8 = Product(name='Galaxy S24', price=24000000, category_id=1,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p9 = Product(name='Note 23 Pro', price=22000000, category_id=1,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")
        p10 = Product(name='Galaxy Tab S9 Ultra', price=24000000, category_id=2,
                     image="https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg")

        db.session.add_all([p1, p2, p3, p4, p5])
        db.session.add_all([p6, p7, p8, p9, p10])
        db.session.commit()