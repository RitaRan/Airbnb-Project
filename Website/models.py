from sqlalchemy import sql, orm
from app import db

class Crime(db.Model):
	__tablename__ = 'crime'
	index = db. Column('index', db.BigInteger, primary_key = True)
	mci = db.Column('mci', db.String(20), primary_key = True)
	longitude = db.Column('longitude', db.Float)
	latitude = db.Column('latitude', db.Float)

class House(db.Model):
	__tablename__ = 'house'
	id = db.Column('id', db.Integer, primary_key = True)
	listing_url = db.Column('listing_url', db.String(64))
	longitude = db.Column('longitude', db.Float)
	latitude = db.Column('latitude', db.Float)
	guest_num = db.Column('guest_num', db.Integer)
	room_type = db.Column('room_type', db.String(32))
	price = db.Column('price', db.Float)
	instant_bookable = db.Column('instant_bookable', db.String(1))
	bedrooms = db.Column('bedrooms', db.Integer)
	beds = db.Column('beds', db.Integer)
	bathrooms = db.Column('bathrooms', db.Float)
	superhost = db.Column('superhost', db.String(1))
	pet_allowed = db.Column('pet_allowed', db.Integer)
	event_allowed = db.Column('event_allowed', db.Integer)
	smoking_allowed = db.Column('smoking_allowed', db.Integer)
	free_parking = db.Column('free_parking', db.Integer)
	family_kid_friendly = db.Column('family_kid_friendly', db.Integer)
	washer = db.Column('washer', db.Integer)
	hangers = db.Column('hangers', db.Integer)
	lock_on_bedroom_door = db.Column('lock_on_bedroom_door', db.Integer)
	wireless_internet = db.Column('wireless_internet', db.Integer)
	laptop_friendly_workspace = db.Column('laptop_friendly_workspace', db.Integer) 
	tv = db.Column('tv', db.Integer) 
	self_check_in = db.Column('self_check_in', db.Integer)
	heating = db.Column('heating', db.Integer)
	hair_dryer = db.Column('hair_dryer', db.Integer)
	indoor_fireplace = db.Column('indoor_fireplace', db.Integer)
	dryer = db.Column('dryer', db.Integer)
	iron = db.Column('iron', db.Integer)
	breakfast = db.Column('breakfast', db.Integer)
	doorman = db.Column('doorman', db.Integer)
	buzzer_wireless_intercom = db.Column('buzzer_wireless_intercom', db.Integer)
	air_conditioning = db.Column('air_conditioning', db.Integer)
	pool = db.Column('pool', db.Integer)
	kitchen = db.Column('kitchen', db.Integer)
	crime_count = db.Column('crime_count', db.Integer)
	shop_count = db.Column('shop_count', db.Integer)
	rest_count = db.Column('rest_count', db.Integer)

class Availability(db.Model):
	__tablename__ = 'availability'
	postid = db.Column('postid', db.Integer, db.ForeignKey('house.id'),primary_key = True)
	start_date = db.Column('start_date', db.DateTime)
	end_date = db.Column('end_date', db.DateTime)
	
class Business(db.Model):
	__tablename__ = 'business'
	id = db.Column('id', db.String(22), primary_key = True)
	name = db.Column('name', db.String(255))
	address = db.Column('address', db.String(255))
	city = db.Column('city', db.String(255))
	state = db.Column('state', db.String(255))
	postal_code = db.Column('postal_code', db.String(255))
	latitude = db.Column('latitude', db.Float)
	longitude = db.Column('longitude', db.Float)
	stars = db.Column('stars', db.Float)
	review_count = db.Column('review_count', db.BigInteger)
	is_shop = db.Column('is_shop', db.Integer)
	is_rest = db.Column('is_rest', db.Integer)


class Category(db.Model):
	__tablename__ = 'category'
	business_id = db.Column('business_id', db.String(22),db.ForeignKey('business.id'), primary_key = True)
	category = db.Column('category', db.String(255))

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column('id', db.String(22), db.ForeignKey('business.id'), primary_key=True)	
    stars = db.Column('stars', db.BigInteger)
    date = db.Column('date', db.DateTime)
    text = db.Column('text', db.Text)
    business_id = db.Column('business_id', db.String(22))







		




