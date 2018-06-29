from . import main
from app import db
from app.models import Team, Group, Duel, TeamPinYin
from flask import render_template


@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@main.route("/32/<int:page>/")
def power_32(page):
    if page is None:
        page = 1

    teams = Team.query.order_by(Team.integral.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).paginate(
        page=page, per_page=8)

    return render_template("32.html", teams=teams)


@main.route("/most_gd/")
def most_gd():
    group_a = Group.query.filter_by(name="A组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_b = Group.query.filter_by(name="B组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_c = Group.query.filter_by(name="C组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_d = Group.query.filter_by(name="D组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_e = Group.query.filter_by(name="E组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_f = Group.query.filter_by(name="F组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_g = Group.query.filter_by(name="G组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    group_h = Group.query.filter_by(name="H组").first().teams.order_by(Team.gd.desc()).join(TeamPinYin).order_by(
        TeamPinYin.name.asc()).limit(2)
    return render_template("most_gd.html", group_a=group_a, group_b=group_b, group_c=group_c, group_d=group_d,
                           group_e=group_e, group_f=group_f, group_g=group_g, group_h=group_h)


@main.route("/most-gap-3/")
def most_gap():
    duels = Duel.query.order_by((Duel.t1_score - Duel.t2_score).desc()).order_by(Duel.datetime.desc()).limit(3)
    return render_template("most_gap.html", duels=duels)


@main.route("/promotion/")
def promotion():
    group_a = Group.query.filter_by(name="A组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_b = Group.query.filter_by(name="B组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_c = Group.query.filter_by(name="C组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_d = Group.query.filter_by(name="D组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_e = Group.query.filter_by(name="E组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_f = Group.query.filter_by(name="F组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_g = Group.query.filter_by(name="G组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    group_h = Group.query.filter_by(name="H组").first().teams.order_by(Team.integral.desc()).order_by(
        Team.gd.desc()).join(TeamPinYin).order_by(TeamPinYin.name.asc()).limit(2)
    return render_template("promotion.html", group_a=group_a, group_b=group_b, group_c=group_c, group_d=group_d,
                           group_e=group_e, group_f=group_f, group_g=group_g, group_h=group_h)
