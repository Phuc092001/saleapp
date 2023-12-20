from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
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
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://res.cloudinary.com/dp87nci6w/image/upload/v1698970995/tablet.jpg')
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime)
    active = Column(Boolean, default=True)


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


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

        p1 = Product(name='iPad Pro 2022', price=24000000, category_id=2)
        p2 = Product(name='iPhone 13', price=21000000, category_id=1)
        p3 = Product(name='Galaxy S23', price=24000000, category_id=1)
        p4 = Product(name='Note 22', price=22000000, category_id=1)
        p5 = Product(name='Galaxy Tab S9', price=24000000, category_id=2)
        p6 = Product(name='iPad Pro 2023', price=24000000, category_id=2)
        p7 = Product(name='iPhone 15 Pro', price=21000000, category_id=1)
        db.session.add_all([p1, p2, p3, p4, p5, p6, p7])
        db.session.commit()