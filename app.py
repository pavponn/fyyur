#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import Artist, Venue, Show
from appconfig import db, app
from datetime import datetime as dt
import sys


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    form = None
    return render_template('pages/home.html', form=form)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    map = {}
    result_data = []
    for venue in venues:
        # TODO num of upcoming shows
        shows_avail = Show.query.filter_by(venue_id=venue.id)
        num_upcoming_shows = shows_avail.filter(Show.start_time > dt.now()).count()
        venue_object = {"id": venue.id, "name": venue.name, "num_upcoming_shows": num_upcoming_shows}
        key = venue.city + "|" + venue.state
        if key not in map:
            map[key] = [venue_object]
        else:
            map[key].append(venue_object)
    for key, value in map.items():
        splitted_key = key.split("|")
        city = splitted_key[0]
        state = splitted_key[1]
        result_object = {"city": city, "state": state, "venues": value}
        result_data.append(result_object)
    
    return render_template('pages/venues.html', areas=result_data, form=VenueForm())

@app.route('/venues/search', methods=['POST'])
def search_venues():
    substr_to_search_for = request.form.get('search_term', '')
    matched_venues = Venue.query.filter(func.lower(Venue.name).contains(substr_to_search_for.lower())).all()
    response = {
        "count" : len(matched_venues),
        "data" : []
    }
    for venue in matched_venues:
        shows_avail = Show.query.filter_by(venue_id=venue.id)
        num_upcoming_shows = shows_avail.filter(Show.start_time > dt.now()).count()
        result_obj = {"id" : venue.id, "name" : venue.name, "num_upcoming_shows" : num_upcoming_shows}
        response['data'].append(result_obj)
    return render_template('pages/search_venues.html', results=response, search_term=substr_to_search_for, form=VenueForm())

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO shows
    venue = Venue.query.filter_by(id=venue_id).one_or_none()
    shows = Show.query.filter_by(venue_id=venue.id).all()
    past_shows = []
    upcoming_shows = []
    for show in shows:
        show_data = {
        'artist_id': show.artist_id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': str(show.start_time)
        }
        if show.start_time <= dt.now():
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)
    venue_data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=venue_data, form=VenueForm())


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = None
    form = VenueForm(request.form)
    print('------ {0}'.format(request.form))
    if not form.validate():
        flash('Invalid input data')
        return render_template('forms/new_venue.html', form=form)
    try: 
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        image_link = request.form['image_link']
        website = request.form['website']
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website=website)
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + name + ' could not be listed.')
        return render_template('forms/new_venue.html', form=form)
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html', form=VenueForm())

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all(), form=ArtistForm())

@app.route('/artists/search', methods=['POST'])
def search_artists():
    substr_to_search_for = request.form.get('search_term', '')
    matched_artists = Artist.query.filter(func.lower(Artist.name).contains(substr_to_search_for.lower())).all()
    response = {
        "count" : len(matched_artists),
        "data" : []
    }
    for artist in matched_artists:
        result_obj = {"id" : artist.id, "name" : artist.name, "num_upcoming_shows" : 0}
        response['data'].append(result_obj)
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''), form=ArtistForm())

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artists page with the given artist_id
    artist = Artist.query.filter_by(id=artist_id).one_or_none()
    shows = Show.query.filter_by(artist_id=artist.id).all()
    past_shows = []
    upcoming_shows = []
    for show in shows:
        show_data = {
        'venue_id': show.venue_id,
        'venue_name': show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time': str(show.start_time)
        }
        if show.start_time <= dt.now():
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)
    artist_data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=artist_data, form=ArtistForm())

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).one_or_none()
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.website.data = artist.website
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link

    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = None
    form = ArtistForm(request.form)
    if not form.validate():
        flash('Invalid input')
        return redirect(url_for('edit_artist', artist_id=artist_id))
    try:
        selectedArtist = Artist.query.get(artist_id)
        selectedArtist.name = request.form['name']
        selectedArtist.city = request.form['city']
        selectedArtist.state = request.form['state']
        selectedArtist.phone = request.form['phone']
        selectedArtist.genres = request.form.getlist('genres')
        selectedArtist.facebook_link = request.form['facebook_link']
        selectedArtist.image_link = request.form['image_link']
        selectedArtist.website = request.form['website']
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully edited!')
    else:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).one_or_none()
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.image_link.data = venue.image_link
    form.website.data = venue.website
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.address.data = venue.address

    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = None
    form = VenueForm(request.form)
    if not form.validate():
        flash('Invalid input')
        return redirect(url_for('edit_venue', venue_id=venue_id))
    try:
        selectedVenue = Venue.query.get(venue_id)
        selectedVenue.name = request.form['name']
        selectedVenue.city = request.form['city']
        selectedVenue.state = request.form['state']
        selectedVenue.phone = request.form['phone']
        selectedVenue.genres = request.form.getlist('genres')
        selectedVenue.facebook_link = request.form['facebook_link']
        selectedVenue.image_link = request.form['image_link']
        selectedVenue.website = request.form['website']
        selectedVenue.address = request.form['address']
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully edited!')
    else:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    return render_template('forms/new_artist.html', form=ArtistForm())

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = None
    form = ArtistForm(request.form)
    print('------ {0}'.format(request.form))
    if not form.validate():
        flash('Invalid input data')
        return render_template('forms/new_artist.html', form=form)
    try: 
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        image_link = request.form['image_link']
        website = request.form['website']
        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website=website)
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + name + ' could not be listed.')
        return render_template('forms/new_artist.html', form=form)
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html', form=ArtistForm())

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = Show.query.order_by(desc(Show.start_time)).all()
    data = []
    for show in shows:
        obj = {
        "venue_id" : show.venue_id,
        "venue_name" : show.venue.name,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time" : str(show.start_time)
        }
        data.append(obj)
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
     # called to create new shows in the db, upon submitting new show listing form
    error = None
    form = ShowForm(request.form)
    print('------ {0}'.format(request.form))
    if not form.validate():
        flash('Invalid input data')
        return render_template('forms/new_show.html', form=form)
    try: 
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
        return render_template('forms/new_show.html', form=form)
    else:
        flash('Show was successfully listed!')
        return render_template('pages/home.html', form=ShowForm())
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
