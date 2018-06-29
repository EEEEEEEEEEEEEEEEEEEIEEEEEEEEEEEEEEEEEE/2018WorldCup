from app import db


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), unique=True)
    teams = db.relationship("Team", backref="group", lazy="dynamic")


class Duel(db.Model):
    __tablename__ = 'duel'
    id = db.Column(db.Integer, primary_key=True)
    t1_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    t2_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    t1_score = db.Column(db.Integer)
    t2_score = db.Column(db.Integer)
    group_cls = db.Column(db.String(3), unique=True)
    datetime = db.Column(db.DateTime)
    area = db.Column(db.String(100))


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    session = db.Column(db.Integer)
    victory = db.Column(db.Integer)
    flat = db.Column(db.Integer)
    lost = db.Column(db.Integer)
    goal = db.Column(db.Integer)
    fumble = db.Column(db.Integer)
    gd = db.Column(db.Integer, index=True)  # goal difference
    integral = db.Column(db.Integer, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    duel_ed = db.relationship("Duel", foreign_keys=[Duel.t2_id], backref=db.backref("team_ed", lazy="joined"),
                              lazy="dynamic",
                              cascade="all,delete-orphan")
    duel_er = db.relationship("Duel", foreign_keys=[Duel.t1_id], backref=db.backref("team_er", lazy="joined"),
                              lazy="dynamic",
                              cascade="all,delete-orphan")

    team_pinyin = db.relationship("TeamPinYin", backref=db.backref("team", lazy="joined"),
                                  cascade="all,delete-orphan")


class TeamPinYin(db.Model):
    __tablename__ = 'teampinyin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))


if __name__ == '__main__':
    db.create_all()
