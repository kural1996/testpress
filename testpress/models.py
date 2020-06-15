from testpress import db

def get_question(question_id):
    return qanda.query.get(question_id)


class qanda(db.Model):


    __tablename__ = 'qanda'


    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String,nullable=False)
    answer = db.Column(db.String,nullable = True)


    def __init__(self,question,answer,id):
        self.question = question
        self.answer = answer
        self.id = id


    def __repr__(self):
        return self.question