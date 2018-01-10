from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import models
import forms_renter
import forms_host
import numpy as np
import requests

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
DATE_DEFAULT = 'Day,Month,Year'
CHECK_DEFAULT = 'None'
VALUE_DEFAULT = '0'
SELECT_DEFAULT = 'No preference' 
ADDRESS_DEFAULT = {'renter': 'Toronto', 'host':['Street', 'District', 'Zip Code']}
CITY = ', Toronto'
INITIAL_RESULT_NUM = {'renter': 100, 'host': 300}
SHOP_REST_RATE = 0.8
LONG_RANGE= 0.01
LAT_RANGE =  0.01


# Helper function
def GetLatLng(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address}
    r = requests.get(url, params=params)
    results = r.json()['results']
    if len(results) == 0:
    	return None
    location = results[0]['geometry']['location']
    return (location['lat'],location['lng'])

def to_sql(text):
    return("_".join(text.lower().split()))

# Web Pages 
@app.route('/')
def home():
    return render_template('home.html', check_default = CHECK_DEFAULT, value_default = VALUE_DEFAULT, date_default = DATE_DEFAULT, 
    									select_default = SELECT_DEFAULT, address_default = ADDRESS_DEFAULT)

@app.route('/renter/<checked_amens>/<checked_rules>/<address>/<min_price>/<max_price>/<check_in>/<check_out>/\
	<inst_bookable>/<selected_room_type>/<selected_bed_num>/<selected_guest_num>/<lowest_crime_rate>/<close_shop>/<close_rest>', methods=['GET', 'POST'])
def renter(checked_amens, checked_rules, 
			 address, min_price, max_price,
			 check_in, check_out, 
			 inst_bookable,
			 selected_room_type, selected_bed_num, selected_guest_num,
			 lowest_crime_rate, close_shop, close_rest):
	amenities = ["Heating", "Kitchen","TV","Wireless Internet"]
	house_rules = ["Pet Allowed", "Event Allowed","Smoking Allowed"]
	preferences = ["Lowest Crime Rate", "Distance to Shopping Centers", "Disatnce to Restaurants"]
	room_type_options = ['No preference','Private room', 'Entire home or apartment', 'Shared room']
	bed_num_options = ['No preference'] + [str(num) + ' or more' for num in range(1,6)]
	guest_num_options = ['No preference'] + [str(num) + ' or more' for num in range(1,6)]

	filter_group = []
	longitude = []
	latitude = []
	houseprice = []
	# Given information is not fully completed 
	if checked_amens != CHECK_DEFAULT or max_price > min_price or address != ADDRESS_DEFAULT['renter']: 
		yes_no = [int(i in checked_amens) for i in amenities]
		for attr in house_rules + amenities:
			if attr in checked_rules:
				filter_group.append(getattr(models.House, to_sql(attr)) == 1)
		# price filter 
		filter_group.append(getattr(models.House, "price") < int(max_price))
		filter_group.append(getattr(models.House, "price") > int(min_price))
		# instant bookable filter 
		if inst_bookable == '1':
			filter_group.append(getattr(models.House, "instant_bookable") == 't')
		# room type filter 
		if selected_room_type != SELECT_DEFAULT:
			if selected_room_type == room_type_options[2]:
				filter_group.append(getattr(models.House, "room_type") == 'Entire home/apt')
			else:
				filter_group.append(getattr(models.House, "room_type") == selected_room_type)
		# bed number filter 
		if selected_bed_num != SELECT_DEFAULT:
			filter_group.append(getattr(models.House, "beds") >= int(selected_bed_num[0]))
		# guest number filter 
		if selected_guest_num != SELECT_DEFAULT:
			filter_group.append(getattr(models.House, "guest_num") >= int(selected_guest_num[0]))

		# address filter 
		lat_long = GetLatLng(address + CITY)
		if lat_long is not None and address != ADDRESS_DEFAULT: 
			filter_group.append(getattr(models.House, "latitude") >= lat_long[0] - LAT_RANGE)
			filter_group.append(getattr(models.House, "latitude") <= lat_long[0] + LAT_RANGE)
			filter_group.append(getattr(models.House, "longitude") >= lat_long[1] - LONG_RANGE)
			filter_group.append(getattr(models.House, "longitude") <= lat_long[1] + LONG_RANGE)
		# lowest crime rate
		filter_group_temp = list(filter_group) 
		houses_temp = db.session.query(models.House).filter(and_(*filter_group_temp)).all()
		if len(houses_temp) != 0: 
			if lowest_crime_rate == "1":
				filter_group.append(getattr(models.House, "crime_count") <= int(np.min([h.crime_count for h in houses_temp])))
			# closest to shopping centers
			if close_shop == "1":
				filter_group.append(getattr(models.House, "shop_count") >= int(np.max([h.shop_count for h in houses_temp])*SHOP_REST_RATE))
			# closest to restaurants
			if close_rest == "1":
				filter_group.append(getattr(models.House, "rest_count") >= int(np.max([h.rest_count for h in houses_temp])*SHOP_REST_RATE))

		filter_group = list(filter_group) 
		houses = db.session.query(models.House).filter(and_(*filter_group)).all()
		# Get the long and lat for map marking 
	else:
		houses = db.session.query(models.House).all()
		np.random.shuffle(houses)
		houses = houses[:INITIAL_RESULT_NUM['renter']]

	urls = [h.listing_url for h in houses]
	houseprice.extend(float(h.price) for h in houses)
	longitude.extend([float(h.longitude) for h in houses])
	latitude.extend([float(h.latitude) for h in houses])

	form = forms_renter.selecthouse.form(amenities, checked_amens,
										 house_rules, checked_rules, 
										 address, min_price, max_price,
										 check_in, check_out, 
										 inst_bookable,
										 room_type_options,bed_num_options,guest_num_options,
										 selected_room_type, selected_bed_num, selected_guest_num,
										 lowest_crime_rate, close_shop, close_rest)

	if form.validate_on_submit():
		try:
			checked_amens = [i for i in form.get_amen_checked()]
			checked_rules = [i for i in form.get_rule_checked()]
			return redirect(url_for('renter', checked_amens = checked_amens,
												  checked_rules = checked_rules,
												  address = form.address.data,
												  min_price = form.min_price.data, max_price = form.max_price.data,
												  check_in = form.check_in.data, check_out = form.check_out.data, 
												  inst_bookable = 1 if form.inst_bookable.data else 0,
												  selected_room_type = form.selected_room_type.data,
												  selected_bed_num = form.selected_bed_num.data,
												  selected_guest_num = form.selected_guest_num.data,
												  lowest_crime_rate = 1 if form.lowest_crime_rate.data else 0,
												  close_shop = 1 if form.close_shop.data else 0,
												  close_rest = 1 if form.close_rest.data else 0))
		except BaseException as e:
			form.errors['database'] = str(e)
			return render_template('renter.html', houses = houses, form=form,
												  new_checked_amens = checked_amens,
												  new_checked_rules = checked_rules, 
												  new_address = address,
												  new_min_price = min_price, new_max_price = max_price,
												  new_check_in = check_in, new_check_out = check_out,
												  new_inst_bookable = inst_bookable,
												  new_selected_room_type = selected_room_type,
												  new_selected_bed_num = selected_bed_num,
												  new_selected_guest_num = selected_guest_num,
												  longitude = longitude, latitude = latitude,
												  new_lowest_crime_rate = lowest_crime_rate,
												  new_close_shop = close_shop,
												  new_close_rest = close_rest,
												  urls = urls,price = houseprice)
	else:
		return render_template('renter.html', houses = houses, form=form,
											  new_checked_amens = checked_amens,
											  new_checked_rules = checked_rules, 
											  new_address = address,
											  new_min_price = min_price, new_max_price = max_price,
											  new_check_in = check_in, new_check_out = check_out,
											  new_inst_bookable = inst_bookable,
											  new_selected_room_type = selected_room_type,
											  new_selected_bed_num = selected_bed_num,
											  new_selected_guest_num = selected_guest_num,
											  longitude = longitude, latitude = latitude,
											  new_lowest_crime_rate = lowest_crime_rate,
											  new_close_shop = close_shop,
											  new_close_rest = close_rest,
											  urls = urls,price = houseprice)


@app.route('/host/<checked_amens>/<checked_rules>/<selected_room_type>/\
	<selected_room_num>/<selected_bed_num>/<selected_guest_num>/<inst_bookable>/<super_host>/\
	<street>/<district>/<zip_code>', methods=['GET', 'POST'])
def host(checked_amens, checked_rules, selected_room_type, selected_room_num, 
		 selected_bed_num, selected_guest_num,
		 inst_bookable, super_host,
		 street, district, zip_code):
    
    amenities = ["Heating", "Kitchen","TV","Wireless Internet"]
    house_rules = ["Pet Allowed", "Event Allowed","Smoking Allowed"]
    room_type_options = ['No preference','Private room', 'Entire home or apartment', 'Shared room']

    room_num_options = ['No preference'] + [str(num) + ' or more' for num in range(1,6)]
    bed_num_options = ['No preference'] + [str(num) + ' or more' for num in range(1,6)]
    guest_num_options = ['No preference'] + [str(num) + ' or more' for num in range(1,6)]

    filter_group = []
    longitude = []
    latitude = []
    prices = []
    for attr in amenities+house_rules:
    	if attr in checked_amens or attr in checked_rules:
    		filter_group.append(getattr(models.House, to_sql(attr)) == 1)
    # instant bookable filter
    if inst_bookable == '1':
    	filter_group.append(getattr(models.House, "instant_bookable") == 't')
    # super host filter
    if super_host == '1':
    	filter_group.append(getattr(models.House, "superhost") == 't')
    # room type filter
    if selected_room_type != SELECT_DEFAULT:
    	# Special Case "/" in url 
    	if selected_room_type == room_type_options[2]:
    		filter_group.append(getattr(models.House, "room_type") == 'Entire home/apt')
    	else:
    		filter_group.append(getattr(models.House, "room_type") == selected_room_type)
    # room number filter 
    if selected_room_num != SELECT_DEFAULT:
    	filter_group.append(getattr(models.House, "bedrooms") >= int(selected_room_num[0]))
    # bed number filter
    if selected_bed_num != SELECT_DEFAULT:
    	filter_group.append(getattr(models.House, "beds") >= int(selected_bed_num[0]))
    # guest number filter
    if selected_guest_num != SELECT_DEFAULT:
    	filter_group.append(getattr(models.House, "guest_num") >= int(selected_guest_num[0]))
    filter_group = list(filter_group)

    lat_long = GetLatLng(street + ', ' + district + ', ' + zip_code + CITY) 
    # if no specific a random sub sampled house information will be given 
    if lat_long is None or street == ADDRESS_DEFAULT['host'][0]:
    	houses = db.session.query(models.House).filter(and_(*filter_group)).all()
    	np.random.shuffle(houses)
    	houses = houses[:INITIAL_RESULT_NUM['host']]
    else:	
    	filter_group.append(getattr(models.House, "latitude") >= lat_long[0] - LAT_RANGE)
    	filter_group.append(getattr(models.House, "latitude") <= lat_long[0] + LAT_RANGE)
    	filter_group.append(getattr(models.House, "longitude") >= lat_long[1] - LONG_RANGE)
    	filter_group.append(getattr(models.House, "longitude") <= lat_long[1] + LONG_RANGE)
    	houses = db.session.query(models.House).filter(and_(*filter_group)).all()

    prices.extend([float(h.price) for h in houses])
    urls = [h.listing_url for h in houses]
    longitude.extend([float(h.longitude) for h in houses])
    latitude.extend([float(h.latitude) for h in houses])
    mean_price = 'N/A' if len(prices) == 0 else int(np.mean(prices))

    form = forms_host.selecthouse.form(amenities, house_rules, 
    	checked_amens, checked_rules,
    	street, district, zip_code,
    	inst_bookable, super_host,
    	room_type_options, room_num_options, bed_num_options, guest_num_options,
    	selected_room_type, selected_room_num, selected_bed_num, selected_guest_num)


    if form.validate_on_submit():
    	try:
    		form.errors.pop('database', None) 
    		checked_amens = [i for i in form.get_amen_checked()]
    		checked_rules = [i for i in form.get_rule_checked()]
    		return redirect(url_for('host', checked_amens = checked_amens, 
            								checked_rules = checked_rules,
            								selected_room_type = form.selected_room_type.data,
            								selected_room_num = form.selected_room_num.data,
            								selected_bed_num = form.selected_bed_num.data,
            								selected_guest_num = form.selected_guest_num.data,
            								inst_bookable = 1 if form.inst_bookable.data else 0,
            								super_host = 1 if form.super_host.data else 0,
            								street = form.street.data,
    										district = form.district.data,
    										zip_code = form.zip_code.data))

    	except BaseException as e:
    		form.errors['database'] = str(e)
    		return render_template('host.html', houses = houses, form=form, 
    											new_checked_amens = checked_amens, 
    											new_checked_rules = checked_rules,
    											new_selected_room_type = selected_room_type,
    											new_selected_room_num = selected_room_num,
    											new_selected_bed_num = selected_bed_num,
    											new_selected_guest_num = selected_guest_num,
    											new_inst_bookable = inst_bookable,
    											new_superhost = super_host,
    											longitude = longitude, latitude = latitude,
    											prices = prices, mean_price = mean_price, urls = urls,
    											new_street = street,
    											new_district = district,
    											new_zip_code = zip_code)
    else:
    	return render_template('host.html', houses = houses, form=form, 
    											new_checked_amens = checked_amens, 
    											new_checked_rules = checked_rules,
    											new_selected_room_type = selected_room_type,
    											new_selected_room_num = selected_room_num,
    											new_selected_bed_num = selected_bed_num,
    											new_selected_guest_num = selected_guest_num,
    											new_inst_bookable = inst_bookable,
    											new_superhost = super_host,
    											longitude = longitude, latitude = latitude,
    											prices = prices, mean_price = mean_price, urls = urls,
    											new_street = street,
    											new_district = district,
    											new_zip_code = zip_code)

if __name__=="__main__":
	app.run(host='0.0.0.0', port=5010)