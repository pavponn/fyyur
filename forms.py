from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import InputRequired, AnyOf, URL, ValidationError
import re


def facebook_validate(form, field):
    matches = re.findall(r'www.facebook.com/.+$', field.data)
    if not matches:
        raise ValidationError('Not a valid Facebook link')

def phone_validate(form, field):
    matches = re.findall(r'^\d{3}-\d{3}-\d{4}$', field.data)
    if not matches:
        raise ValidationError('Not a valid phone number')

genres_choices = [
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
        
states_choices = [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
    ]

class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[InputRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[InputRequired()],
    )
    start_time = DateTimeField(
        'start_time',
        validators=[InputRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[InputRequired("Name can't be empty")]
    )
    city = StringField(
        'city', validators=[InputRequired("City can't be empty")]
    )
    state = SelectField(
        'state', validators=[InputRequired("State can't be empty")],
        choices=states_choices
    )
    address = StringField(
        'address', validators=[InputRequired("Address can't be empty")]
    )
    phone = StringField(
        'phone', validators=[InputRequired("Phone can't be empty"), phone_validate]
    )
    image_link = StringField(
        'image_link', validators=[InputRequired("Image link should be provided"), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[InputRequired("Genres can't be empty")],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), facebook_validate]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = StringField(
        'seeking_description'
    )

    

class ArtistForm(Form):
    name = StringField(
        'name', validators=[InputRequired("Name can't be empty")]
    )
    city = StringField(
        'city', validators=[InputRequired("City can't be empty")]
    )
    state = SelectField(
        'state', validators=[InputRequired("State can't be empty")],
        choices=states_choices
    )
    phone = StringField(
        'phone', validators=[InputRequired("Phone can't be empty"), phone_validate]
    )
    image_link = StringField(
        'image_link', validators=[InputRequired("Image link should be provided"), URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[InputRequired("Genres can't be empty")],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), facebook_validate]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description'
    )
