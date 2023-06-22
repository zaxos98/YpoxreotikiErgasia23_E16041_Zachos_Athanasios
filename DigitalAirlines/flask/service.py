from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os 

app = Flask(__name__)

mongodb_hostname = os.environ.get("MONGO_HOSTNAME","mongodb2")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

db = client['DigitalAirlines']
users_collection = db['users']
flights_collection = db['flights']
reservations_collection = db['reservations']



#Log In
@app.route('/log-in', methods=['POST'])
def log_in():
    # Get user credentials
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find the user with the given email and password
    user = users_collection.find_one({'email': email, 'password': password})

    if user:
        users_collection.update_one(
            {'_id': user['_id']},
            {'$set': {'is_logged': True}}
        )
        if user['is_admin'] == True:
            return jsonify(message='Loged In As Administrator'), 200
        else:
            return jsonify(message='Login successful'), 200
        
    else:
        return jsonify(message='Invalid credentials. Please try again.'), 401



#Log Out
@app.route('/log-out',methods=['POST'])
def log_out():
    #Get user email
    data = request.get_json()
    email = data.get('email')
    
    user = users_collection.find_one({'email': email})

    #Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404

    if user:
        users_collection.update_one(
            {'_id': user['_id']},
            {'$set': {'is_logged': False}}
        )
        return jsonify(message='Log Out Successful.'), 200
    else:
        return jsonify(message='User Not Found'), 404



#Search_Flight
@app.route('/search-flight', methods=['POST'])
def search_flight():
    # Get search criteria from the request
    data = request.get_json()
    email = data.get('email')
    destination = data.get('Destination_Airport')
    origin = data.get('Airport_Of_Origin')
    date = data.get('Date_Of_Flight')

    #Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.')
    else:
        return jsonify(message='User not found.')

    # Construct the search query based on the provided criteria
    search_query = {}
    if destination:
        search_query['Destination_Airport'] = destination
    if origin:
        search_query['Airport_Of_Origin'] = origin
    if date:
        search_query['Date_Of_Flight'] = date

    # Perform the search based on the constructed query
    flights = flights_collection.find(search_query, {'_id': 1, 'Date_Of_Flight': 1, 'Destination_Airport': 1, 'Airport_Of_Origin': 1})

    # Create a list to store the flight results
    flight_results = []
    for flight in flights:
        flight_info = {
            '_id': str(flight['_id']),
            'Date_Of_Flight': flight['Date_Of_Flight'],
            'Destination_Airport': flight['Destination_Airport'],
            'Airport_Of_Origin': flight['Airport_Of_Origin']
        }
        flight_results.append(flight_info)

    return jsonify(flight_results), 200



#Delete User
@app.route('/delete-user',methods=['DELETE'])
def delete_user():
    data = request.get_json()
    email = data.get('email')

    user = users_collection.find_one({'email': email})

    #Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404

    if user:
        users_collection.delete_one({'_id': user['_id']})
        return jsonify(message='User Deleted Successfully'), 200
    else:
        return jsonify(message='User Not Found.'), 404



# Sing Up New User
@app.route('/sign-up', methods=['POST'])
def sign_up():
    # Get user data 
    data = request.get_json()
    username = data.get('username')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    birthday = data.get('birthday')
    region = data.get('region')
    passport_num = data.get('passport_num')

    # Check if the user already exists by email or username
    existing_user = users_collection.find_one(
        {
            '$or': [
                {'email': email},
                {'username': username}
            ]
        }
    )
    if existing_user:
        return jsonify(message='User with the same email or username already exists'), 409

    # Create a new user document
    user = {
        'username': username,
        'last_name': last_name,
        'email': email,
        'password': password,
        'birthday': birthday,
        'region': region,
        'passport_num': passport_num,
        'is_admin': False,
        'is_logged': False
    }

    # Insert the new user into the users collection
    users_collection.insert_one(user)

    return jsonify(message='User registered successfully'), 200



# Print Flight Info
@app.route('/flight-info', methods=['POST'])
def flight_info():
    data = request.get_json()
    email = data.get('email')
    flight_id = data.get('flight_id')
    flight_id = ObjectId(flight_id)

    # Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404

    # Find the flight with the given _id
    flight = flights_collection.find_one({'_id': flight_id})

    if flight:
        flight_info = {
            'Airport_Of_Origin': flight['Airport_Of_Origin'],
            'Destination_Airport': flight['Destination_Airport'],
            'Date_Of_Flight': flight['Date_Of_Flight'],
            'Available_Tickets_Eco': flight['Available_Tickets_Eco'],
            'Price_Eco': flight['Price_Eco'],
            'Available_Tickets_Bus': flight['Available_Tickets_Bus'],
            'Price_Bus': flight['Price_Bus'],
            '_id': str(flight['_id'])
        }

        # If the user is an admin, include reservations for the flight
        if logged['is_admin']:
            flight_id = str(flight_id)
            reservations = reservations_collection.find({'flight_id': flight_id})
            reservation_list = []
            for reservation in reservations:
                reservation_info = {
                    'username': reservation['username'],
                    'last_name': reservation['last_name'],
                    'ticket_type': reservation['ticket_type']
                }
                reservation_list.append(reservation_info)
            flight_info['reservations'] = reservation_list

        return jsonify(flight_info), 200
    else:
        return jsonify(message='Flight not found'), 404



# Make Reservation
@app.route('/make-reservation', methods=['POST'])
def make_reservation():
    # Get reservation data from the request
    data = request.get_json()
    flight_id = data.get('flight_id')
    username = data.get('username')
    last_name = data.get('last_name')
    passport_num = data.get('passport_num')
    birthday = data.get('birthday')
    email = data.get('email')
    ticket_type = data.get('ticket_type')  # 'eco' or 'business'

    #Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404
    

    # Check if the flight exists
    flight = flights_collection.find_one({'_id': ObjectId(flight_id)})
    if not flight:
        return jsonify(message='Flight not found'), 404

    # Create a new reservation document
    reservation = {
        'flight_id': flight_id,
        'username': username,
        'last_name': last_name,
        'passport_num': passport_num,
        'birthday': birthday,
        'email': email,
        'ticket_type': ticket_type
    }

    # Insert the reservation into the reservations collection
    reservations_collection.insert_one(reservation)

    return jsonify(message='Reservation created successfully'), 200



#Print Reservations
@app.route('/print-reservations', methods=['POST'])
def print_reservations():

    # Get the user email from the request
    data = request.get_json()
    email = data.get('email')

    #Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404

    # Retrieve the reservations for the user
    reservations = reservations_collection.find({'email': email})

    # Create a list to store the reservation information
    reservation_list = []
    for reservation in reservations:
        reservation_info = {
            'flight_id': str(reservation['flight_id']),
            'username': reservation['username'],
            'last_name': reservation['last_name'],
            'ticket_type': reservation['ticket_type']
        }
        reservation_list.append(reservation_info)

    return jsonify(reservation_list), 200



#Reservation Info
@app.route('/reservation-info', methods=['POST'])
def reservation_info():
    # Get the user email and reservation ID from the request
    data = request.get_json()
    email = data.get('email')
    reservation_id = data.get('reservation_id')

    #Check if logged in
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404

    # Retrieve the reservation for the user and reservation ID
    reservation = reservations_collection.find_one({'_id': ObjectId(reservation_id), 'email': email})
    if not reservation:
        return jsonify(message='Reservation not found'), 404
    flight = flights_collection.find_one({'_id': ObjectId(reservation['flight_id'])})

    # Extract the reservation information
    reservation_info = {
        'flight_id': str(reservation['flight_id']),
        'Airport_of_Origin': flight['Airport_Of_Origin'],
        'Destination_Airport': flight['Destination_Airport'],
        'Date_Of_Flight': flight['Date_Of_Flight'],
        'username': reservation['username'],
        'last_name': reservation['last_name'],
        'pasport_num': reservation['passport_num'],
        'birthday': reservation['birthday'],
        'ticket_type': reservation['ticket_type']
    }

    return jsonify(reservation_info), 200



#Cancel Reservation
@app.route('/cancel-reservation', methods=['POST'])
def cancel_reservation():
    # Get the reservation ID from the request
    data = request.get_json()
    email = data.get('email')
    reservation_id = data.get('reservation_id')

    #Check if logged in 
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
    else:
        return jsonify(message='User not found.'), 404

    # Check if the reservation exists
    reservation = reservations_collection.find_one({'_id': ObjectId(reservation_id)})
    if not reservation:
        return jsonify(message='Reservation not found'), 404

    # Delete the reservation
    reservations_collection.delete_one({'_id': ObjectId(reservation_id)})

    return jsonify(message='Reservation canceled successfully'), 200


#Create Flight
@app.route('/create-flight', methods=['POST'])
def create_flight():
    data = request.get_json()
    email = data.get('email')
    origin = data.get('Airport_Of_Origin')
    destination = data.get('Destination_Airport')
    date = data.get('Date_Of_Flight')
    available_eco = data.get('Available_Tickets_Eco')
    price_eco = data.get('Price_Eco')
    available_bus = data.get('Available_Tickets_Business')
    price_bus = data.get('Price_Business')

    #Check if logged in and admin
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
        if not logged['is_admin']:
            return jsonify(message='You are not an Administrator.'), 403
    else:
        return jsonify(message='User not found.'), 404

    flight = {
        'Airport_Of_Origin': origin,
        'Destination_Airport': destination,
        'Date_Of_Flight': date,
        'Available_Tickets_Eco': int(available_eco),
        'Price_Eco': int(price_eco),
        'Available_Tickets_Bus': int(available_bus),
        'Price_Bus': int(price_bus)
    }

    flights_collection.insert_one(flight)

    return jsonify(message='Flight Created Succefully'), 200       



#Update Prices
@app.route('/update-prices', methods=['POST'])
def update_prices():
    # Get the flight ID and new prices from the request data
    data = request.get_json()
    email = data.get('email')
    flight_id = data.get('flight_id')
    new_price_eco = data.get('new_price_eco')
    new_price_bus = data.get('new_price_bus')
    
    #Check if logged in or admin
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
        if not logged['is_admin']:
            return jsonify(message='You are not an Administrator.'), 403
    else:
        return jsonify(message='User not found.'), 404

    flight_id = ObjectId(flight_id)

    # Find the flight with the given _id
    flight = flights_collection.find_one({'_id': flight_id})

    if flight:
        if new_price_eco and new_price_bus:
            # Save the updated flight document
            flights_collection.update_one({'_id': flight_id},
                                       {'$set':{'Price_Eco':int(new_price_eco)}})
            flights_collection.update_one({'_id': flight_id},
                                       {'$set':{'Price_Bus':int(new_price_bus)}})
            return jsonify(message='Prices updated successfully'), 200
        elif not new_price_bus:
            flights_collection.update_one({'_id': flight_id},
                                       {'$set':{'Price_Eco':int(new_price_eco)}})
            return jsonify(message='Prices updated successfully'), 200
        elif not new_price_eco:
            flights_collection.update_one({'_id': flight_id},
                                       {'$set':{'Price_Bus':int(new_price_bus)}})
            return jsonify(message='Prices updated successfully'), 200
    else:
        return jsonify(message='Flight not found'), 404



#Delete Flight
@app.route('/delete-flight', methods=['POST'])
def delete_flight():
    data = request.get_json()
    email = data.get('email')
    flight_id = data.get('flight_id')

    #Check if logged in or admin
    logged = users_collection.find_one({'email': email})

    if logged:
        if not logged['is_logged']:
            return jsonify(message='Log In first.'), 403
        if not logged['is_admin']:
            return jsonify(message='You are not an Administrator.'), 403
    else:
        return jsonify(message='User not found.'), 404


    # Check if the flight exists
    flight = flights_collection.find_one({'_id': ObjectId(flight_id)})
    if not flight:
        return jsonify(message='Flight not found'), 404

    # Check if there are reservations for the flight
    reservation = reservations_collection.find_one({'flight_id': flight_id})
    if reservation:
        return jsonify(message='Cannot delete flight with existing reservations'), 400


    # Delete the flight
    flights_collection.delete_one({'_id': ObjectId(flight_id)})

    return jsonify(message='Flight deleted successfully'), 200




if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)