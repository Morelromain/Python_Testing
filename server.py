import json
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


app = Flask(__name__)
app.secret_key = 'something_special'


def loadClubs():
    """ load clubs.json """

    with open('clubs.json') as c:
        return json.load(c)['clubs']


def loadCompetitions():
    """ load competitions.json """

    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


def old_or_new(competitions):
    """ sorting past or upcoming competitions """

    old_c = [c for c in competitions if datetime.datetime.strptime(
        c['date'], "%Y-%m-%d %H:%M:%S"
        ) < datetime.datetime.now()]
    new_c = [c for c in competitions if datetime.datetime.strptime(
            c['date'], "%Y-%m-%d %H:%M:%S"
            ) >= datetime.datetime.now()]
    return old_c, new_c


competitions = loadCompetitions()
clubs = loadClubs()
point_memory = []


# /
@app.route('/')
def index():
    """ display index.html for login """

    return render_template('index.html', clubs=clubs)


# /showSummary
@app.route('/showSummary', methods=['POST'])
def showSummary():
    """ display welcome.html if email matches """

    try:
        club = [
            club for club in clubs if club['email'] == request.form['email']
            ][0]
        old_c, new_c = old_or_new(competitions)
        return render_template(
            'welcome.html', club=club,
            competitions=new_c, old_c=old_c, clubs=clubs)

    except IndexError:
        flash("Invalid email provided")
        return render_template("index.html", clubs=clubs), 403


# /book
def create_point_memory(competitions):
    """ create point_memory if it does not exist """

    if point_memory == []:
        for a, competition in enumerate(competitions):
            point_memory.append(competition)
            point_memory[a]['taken'] = 0


def create_point_add(competition):
    """ create point_add from point_memory of the competition """

    for point in point_memory:
        if (competition['name']) == point['name']:
            point_add = int(point['taken'])
    return point_add


def not_old_check(foundCompetition):
    """ check if competition in progress """

    if datetime.datetime.strptime(
        foundCompetition['date'], "%Y-%m-%d %H:%M:%S"
            ) < datetime.datetime.now():
        raise ValueError("the competition is closed")


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """ display booking.html if competition matches """

    create_point_memory(competitions)
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    point_add = create_point_add(foundCompetition)
    try:
        not_old_check(foundCompetition)
    except ValueError as error:
        flash(error)
        status_code = 403
        old_c, new_c = old_or_new(competitions)
        return render_template(
            'welcome.html', club=club,
            competitions=new_c, old_c=old_c, clubs=clubs
            ), status_code
    limit = (
        int(foundClub["points"]) // 3,
        int(foundCompetition['numberOfPlaces']),
        12-point_add
        )
    return render_template(
        'booking.html', club=foundClub,
        competition=foundCompetition, limit=min(limit)
        )


# /purchasePlaces
def add_point_memory(competition, placesRequired):
    """ add required place to point_memory, check if less than 13 """

    if placesRequired > 12:
        raise ValueError("More place than 12 take per clubs")
    for point in point_memory:
        if (competition['name']) == point['name']:
            point['taken'] = point['taken'] + placesRequired
        if point['taken'] > 12:
            raise ValueError("More place than 12 take per clubs")


def place_substraction(competition, placesRequired):
    """ subtract required place to competition, check if it's possible """

    if int(competition["numberOfPlaces"]) < placesRequired:
        raise ValueError("More place request than place of competition")
    competition['numberOfPlaces'] = (
        int(competition['numberOfPlaces']) - placesRequired
        )


def club_point_substraction(club, placesRequired):
    """ subtract required place to the club, check if it's possible """

    if int(club["points"]) - (placesRequired * 3) < 0:
        raise ValueError("More place request than club point")
    club["points"] = int(club["points"]) - (placesRequired*3)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """ display welcome.html, check and update the reservation """

    competition = [
        c for c in competitions if c['name'] == request.form['competition']
        ][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    try:
        place_substraction(competition, placesRequired)
        add_point_memory(competition, placesRequired)
        club_point_substraction(club, placesRequired)
        flash('Great-booking complete!')
        status_code = 200
    except ValueError as error:
        flash(error)
        status_code = 403
    old_c, new_c = old_or_new(competitions)
    return render_template(
        'welcome.html', club=club,
        competitions=new_c, old_c=old_c, clubs=clubs
        ), status_code


# /logout
@app.route('/logout')
def logout():
    """ logout and display index.html """

    return redirect(url_for('index'))
