from db import db
from sqlalchemy.orm import load_only

class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    company = db.Column(db.String(50))
    balance = db.Column(db.Integer)
    order = db.Column(db.String)
    embedding = db.Column(db.String)


    def __init__(self, id, name, email, company, balance, order, embedding):
        self.id = id
        self.name = name
        self.email = email
        self.company = company
        self.balance = balance
        self.order = order
        self.embedding = embedding

    def json(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'company': self.company, 'balance': self.balance, 'order': self.order, 'embedding': self.embedding}

    def findAll():
        return UserModel.query.all()

    def findById(id):
        return UserModel.query.get(id)

    def findByEmail(userEmail):
        s = db.session.query(UserModel).filter(UserModel.email == userEmail)
        for row in db.session.execute(s):
            return dict(row)

    def findAllEmbedding():
        s = db.session.query(UserModel).options(load_only("embedding"))
        embeddings = []
        for row in db.session.execute(s):
            obj = dict(row)
            embeddings.append(obj)
        return embeddings


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, id):
        user = UserModel.query.get(id)
        user.name = self.name
        user.email = self.email
        user.company = self.company
        user.balance = self.balance
        user.order = self.order
        user.embedding = self.embedding
        db.session.commit()
        return user

    def transfer(creditor, debtor):
        if creditor.balance == 0:
            return None
        debtor.balance += creditor.balance
        creditor.balance = 0

        db.session.commit()
        return {"users": [creditor.json(), debtor.json()]}
