import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


def negatif_place(competition, placesRequired):
    if int(competition["numberOfPlaces"]) < placesRequired:
        raise ValueError("More place request than place of competition")


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
point_memory = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try: 
        club = [club for club in clubs if club['email'] == request.form['email']][0]


        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        flash("Invalid email provided")
        return render_template("index.html"), 500


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    print(foundCompetition)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)




@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    """if point_memory == []:
        a = 0
        for competition in competitions:
            point_memory.append(competition)
            point_memory[a]['taken']=0
            a += 1"""

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    """for point in point_memory:
        if (competition['name']) == point['name']:
            point['taken'] = point['taken'] + placesRequired
            if point['taken'] > 12:
                placesRequired = placesRequired + (12 - point['taken'])
                point['taken'] = 12"""
            
    try:
        negatif_place(competition, placesRequired)
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        flash('Great-booking complete!')
        status_code = 200
    except ValueError as error:
        flash(error)
        status_code = 500

    
    
    
    
    return render_template('welcome.html', club=club, competitions=competitions), status_code


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
