#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from model import db,Venue,Artist,Show,seed_data
from sqlalchemy import func

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
# TODO: connect to a local postgresql database
# db = SQLAlchemy(app)
migrate = Migrate(app, db)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Query to get all venues with the number of upcoming shows
    upcoming_shows = Show.query.all()
    venues_data = db.session.query(Venue,func.count(Show.id))\
                  .outerjoin(Show, Show.venue_id == Venue.id)\
                  .filter(Show.date > datetime.now())\
                  .group_by(Venue.id)\
                  .all()

    data = []
    
    for venue in venues_data:
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": 0
        }]
      })
    
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')

    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

    response = {
        "count": len(venues),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": 0,
        } for venue in venues]
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if not venue:
        abort(404)

    past_show = db.session.query(Show,Artist)\
                .join(Artist, Show.artist_id == Artist.id)\
                  .filter(Show.venue_id == venue_id, Show.date >= datetime.now()).all()
                  
    upcoming_shows = db.session.query(Show, Artist)\
                     .join(Artist, Show.artist_id == Artist.id)\
                       .filter(Show.venue_id == venue_id, Show.date >= datetime.now()).all()
    data = {
        "id": venue.id,
        "name": venue.name,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "facebook_link": venue.facebook_link,
        "image_link": venue.image_link,
        "genres": [],
        "seeking_talent": False,
        "seeking_description": "",
        "past_shows": past_show,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
      form = VenueForm(request.form)
      if form.validate():
        try:
              venue_name = form.name.data
              new_venue = Venue(
                      name=venue_name,
                      city=form.city.data,
                      state=form.state.data,
                      address=form.address.data,
                      phone=form.phone.data,
                      facebook_link=form.facebook_link.data,
                      image_link = form.image_link.data,
                      genres = form.genres.data,
                      seeking_talent = form.seeking_talent.data,
                      seeking_description = form.seeking_description.data,
                      website_link = form.website_link.data
                  )
              db.session.add(new_venue)
              db.session.commit()
              flash(f'Venue {form.name.data} was successfully listed!')
        except :
              db.session.rollback()
              flash(f'An error occurred. Venue {form.name.data} could not be listed.')
        finally:
          db.session.close()
      else:
        flash('Form validation failed. Please check the inputs.')
      return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

    try:
        Venue.query.filter_by(venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for("index"))
    # return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # Query to get all venues with the number of upcoming shows
    art_data = Artist.query.all()

    data = []

    for d in art_data:
            data.append({
              "id": d.id,
              "name":d.name,

            })

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', '')

    art = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

    response = {
        "count": len(art),
        "data": [{
            "id": a.id,
            "name": a.name,
            "num_upcoming_shows": 0,
        } for a in art]
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.filter_by(id=artist_id).first()

    if artist is None:
        return abort(404)

    upcoming_shows = []
    past_shows = []
    for show in artist.shows:
      if show.date > datetime.now():
        upcoming_shows.append(show)
    else:
      past_shows.append(show)
      artist.upcoming_shows = upcoming_shows
      artist.past_shows = past_shows
    
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  art_found = Artist.query.get(artist_id)
  if art_found is None:
      abort(404)

  artist={
    "id": art_found.id,
    "name": art_found.name,
    "genres": art_found.genres,
    "city": art_found.city,
    "state": art_found.state,
    "phone": art_found.phone,
    "facebook_link": art_found.facebook_link,
    "seeking_venue": True,
    "image_link": art_found.image_link
  }
  form = ArtistForm(formdata=None, data=artist)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  art_found = Artist.query.get(artist_id)

  if art_found is None:
      abort(404)
  else:
      try:
        form = ArtistForm(request.form)
        art_found.name = form.name.data
        art_found.genres = form.genres.data
        art_found.city = form.city.data
        art_found.state = form.state.data
        art_found.phone = form.phone.data
        art_found.facebook_link = form.facebook_link.data
        art_found.seeking_venue = form.seeking_value.data
        art_found.image_link = form.image_link.data

        db.session.commit()
      except:
        db.session.rollback()
        print(sys.exc_info)
      finally:
        db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue_found = Venue.query.get(venue_id)

    if venue_found is None:
        abort(404)

    venue = {
        'id': venue_found.id,
        'name': venue_found.name,
        'address': venue_found.address,
        'city': venue_found.city,
        'phone': venue_found.phone,
        'facebook_link': venue_found.facebook_link,
        'image_link': venue_found.image_link
    }

    form = VenueForm(formdata=None, data=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue_found = Venue.query.get(venue_id)

  if venue_found is None:
      abort(404)
  else:
      try:
          form = VenueForm(request.form)
          venue_found.name = form.name.data
          venue_found.address = form.address.data
          venue_found.city = form.city.data
          venue_found.phone = form.phone.data
          venue_found.facebook_link = form.facebook_link.data
          venue_found.image_link = form.image_link.data

          db.session.commit()
      except:
          db.session.rollback()
          print(sys.exc_info)
      finally:
          db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  if form.validate():
    try:

        data = Artist(
            name = form.name.data,
            state = form.state.data,
            city = form.city.data,
            phone = form.phone.data,
            image_link = form.image_link.data,
            facebook_link = form.facebook_link.data,
            seeking_venue = form.seeking_venue.data,
            seeking_description = form.seeking_description.data,
            website_link = form.website_link.data,
            genres = form.genres.data
        )
        db.session.add(data)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        message = ('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
      message = ('An error occurred. Artist ' + form.name.data + ' could not be listed.')
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    return render_template('pages/home.html')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = db.session.query(Show, Venue, Artist) \
    .join(Venue, Show.venue_id == Venue.id) \
    .join(Artist, Show.artist_id == Artist.id) \
    .all()
  data = []
  
  for show, venue, artist in shows:
      data.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": show.artist_id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.date.strftime('%Y-%m-%d %H:%M:%S')
      })

  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  if form.validate():
    try:
        
        
        venue_found = Venue.query.get(form.venue_id.data)
        art_found = Artist.query.get(form.artist_id.data)
        if venue_found is not None and art_found is not None:
            data = Show(
                venue_id = form.venue_id.data,
                artist_id = form.artist_id.data,
                date = form.start_time.data
            )
            db.session.add(data)
            db.session.commit()
    except:
        db.session.rollback()
        sys.exc_info()
    finally:
        db.session.close()
  else:
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
