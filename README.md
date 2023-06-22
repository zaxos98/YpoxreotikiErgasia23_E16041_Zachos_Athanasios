# Digital Airlines 

<h2>How to set this rervice to your system.</h2>
Download the repository and open terminal on that location

<h3>Run the following commands</h3>
<pre>
  cd DigitalAirlines
  ls <br>  
    Directory: C:\Users\zaxos\Desktop\DigitalAirlines

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         22/6/2023   8:18 μμ                flask
-a----         21/6/2023  10:08 μμ            538 docker-compose.yml
<br><br>
docker compose up
</pre>

<pre>
  docker cp flask/data/users.json mongodb2:/users.json
  docker cp flask/data/reservations.json mongodb2:/reservations.json
  docker cp flask/data/flights.json mongodb2:/flights.json
  <br>
  docer exex -it mongodb2 mongoimport --db=DigitalAirlines --collection=users --file=users.json --jsonArray
  docer exex -it mongodb2 mongoimport --db=DigitalAirlines --collection=reservations --file=reservations.json --jsonArray
  docer exex -it mongodb2 mongoimport --db=DigitalAirlines --collection=flights --file=flights.json --jsonArray
</pre>

<hr>

<h3>Exaples.</h3>
<br>
On some endpoint there a field for email. This indicates to database if the user is log in or simple user/administrator.
<br>
<pre>
  #Sing Up#
  
  Type: POST
  Url: http://0.0.0.0:5000/sign-up
  body:
  {
    "username": "Christos",
    "last_name": "Chatzidamianos",
    "email" : "dami@mail.com",
    "password": "123456",
    "birthday": "25/12/1997",
    "region": "Greece",
    "passport_num": "B887246"
  }

  response:
  {
      "message": "User registered successfully"
  }

  If the email or username already exist in database then

  {
      "message": "User with the same email or username already exists"
  }
</pre>

<pre>
  #Log In#
  
  Type: POST
  Url: http://0.0.0.0:5000/log-in
  body:
  {
    "email": "zaxos2998@gmail.com",
    "password": "123456"
  }
  
  if user is simple user
  
  response:
  {
    "message": "Login successful"
  }

  if user is an administrator
  {
    "message": "Loged In As Administrator"
  }
</pre>

<pre>
  #Log Out#
  
  Type: POST
  Url: http://0.0.0.0:5000/log-out
  body:
  {
    "email": "zaxos2998@gmail.com"
  }  
  
  response:
  {
    "message": "Log Out Successful."
  }
</pre>

<pre>
  #Delete User#
  
  Type: DELETE  
  Url: http://0.0.0.0:5000/delete-user
  body:
  {
    "email": "dam1@mail.com"
  }
  
  response:
  {
     "message": "User Deleted Successfully"
  }

  If there is not this user:
  
  response:
  {
     "message": "User not found."
  }
</pre>

<pre>
  #Create Flight#
  
  Type: POST
  Url: http://0.0.0.0:5000/create-flight
  body:
  {
    "email": "zaxos2998@gmail.com",
    "Airport_Of_Origin": "Thessaloniki",
    "Destination_Airport": "Chania",
    "Date_Of_Flight":"07/12/2023",
    "Available_Tickets_Eco": "25",
    "Price_Eco": "208",
    "Available_Tickets_Business": "145",
    "Price_Business": "50"
  }

  response:
  {
    "message": "Flight Created Succefully"
  }
</pre>

<pre>
  #Delete Flight#
  
  Type: POST
  Url: http://0.0.0.0:5000/delete-flight
body:
  {
    "email": "zaxos2998@gmail.com",
    "flight_id": "646b85a0eb3fded11ef57540"
  }
  
response:
  {
    "message": "Cannot delete flight with existing reservations"
  }

body:
  {
    "email": "zaxos2998@gmail.com",
    "flight_id": "646b85a0eb3fded11ef57540"
  }

response:
  {
    "message": "Flight deleted successfully" 
  }
</pre>

<pre>
  #Search Flight#
  
  Type: POST
  Url: http://0.0.0.0:5000/search-flight
  body:
  {
    "email":"zaxos2998@gmail.com",
    "Airport_Of_Origin":"",
    "Destination_Airport":"",
    "Date_Of_Flight":""
  }

  # depending on which blanks are filled, it will give the corresponding results. In the exaple none of the blanks are filled and it return all of the flights.

  response:
  [
    {
        "Airport_Of_Origin": "Amsterdam",
        "Date_Of_Flight": "07/12/2023",
        "Destination_Airport": "New York",
        "_id": "646e1b65bd93b43c4a7b6b55"
    },
    {
        "Airport_Of_Origin": "Amsterdam",
        "Date_Of_Flight": "02/9/2023",
        "Destination_Airport": "New York",
        "_id": "646b85a0eb3fded11ef57540"
    },
    {
        "Airport_Of_Origin": "Chicago",
        "Date_Of_Flight": "02/9/2023",
        "Destination_Airport": "Tokio",
        "_id": "646cff94dc26363ef5b77e4c"
    },
    {
        "Airport_Of_Origin": "Thessaloniki",
        "Date_Of_Flight": "07/12/2023",
        "Destination_Airport": "Chania",
        "_id": "646e1bc7bd93b43c4a7b6b56"
    },
    {
        "Airport_Of_Origin": "Thessaloniki",
        "Date_Of_Flight": "07/12/2023",
        "Destination_Airport": "Chania",
        "_id": "649349752f8d6353630e6da0"
    },
    {
        "Airport_Of_Origin": "Thessaloniki",
        "Date_Of_Flight": "07/12/2023",
        "Destination_Airport": "Chania",
        "_id": "649349ad2f8d6353630e6da1"
    },
    {
        "Airport_Of_Origin": "Thessaloniki",
        "Date_Of_Flight": "07/12/2023",
        "Destination_Airport": "Chania",
        "_id": "64948cab03733dbd51a20c3b"
    }
]

body:
  {
    "email":"zaxos2998@gmail.com",
    "Airport_Of_Origin":"Amsterdam",
    "Destination_Airport":"",
    "Date_Of_Flight":""
  }

response:
  [
    {
        "Airport_Of_Origin": "Amsterdam",
        "Date_Of_Flight": "07/12/2023",
        "Destination_Airport": "New York",
        "_id": "646e1b65bd93b43c4a7b6b55"
    },
    {
        "Airport_Of_Origin": "Amsterdam",
        "Date_Of_Flight": "02/9/2023",
        "Destination_Airport": "New York",
        "_id": "646b85a0eb3fded11ef57540"
    }
]
</pre>

<pre>
  #Flight Information#
  
  Type: POST
  Url: http://0.0.0.0:5000/flight-info
body:
  {
    "email": "zaxos2998@gmail.com",
    "flight_id": "646b85a0eb3fded11ef57540"
  }
  
response:
 {
    "Airport_Of_Origin": "Amsterdam",
    "Available_Tickets_Bus": 45,
    "Available_Tickets_Eco": 153,
    "Date_Of_Flight": "02/9/2023",
    "Destination_Airport": "New York",
    "Price_Bus": 824456,
    "Price_Eco": 23910,
    "_id": "646b85a0eb3fded11ef57540",
    "reservations": [
        {
            "last_name": "Zaxos",
            "ticket_type": "eco",
            "username": "Thanasis4"
        }
    ]
  }
  
  # If this flight does not exist.
  
  body:
  {
    "email": "zaxos2998@gmail.com",
    "flight_id": "6469068b1e68da30ac6a1784"
  }

  response:
  {
    "message": "Flight not found"
  }
</pre>


<pre>
  #Update Prices#
  
  Type: POST
  Url: http://0.0.0.0:5000/update-prices
body:
  {
    "email": "zaxos2998@gmail.com",
    "flight_id": "646b85a0eb3fded11ef57540",
    "new_price_eco": "300",
    "new_price_bus": ""
  }

  
response:
  {
    "message": "Prices updated successfully"
  }
</pre>

<pre>
  #Make Reservation#
  
  Type: POST
  Url: http://0.0.0.0:5000/make-reservation
body:
  {
    "flight_id": "646b85a0eb3fded11ef57540",
    "username": "Thanasis4",
    "last_name": "Zaxos",
    "passport_num": "B187",
    "birthday": "29/04/1998",
    "email": "zaxos2998@gmail.com",
    "ticket_type": "eco"
  }

  
response:
  {
    "message": "Reservation created successfully"
  }
</pre>

<pre>
  #Print Reservations#
  
  Type: POST
  Url: http://0.0.0.0:5000/print-reservations
body:
  {
    "email": "zaxos2998@gmail.com"
  }

  
response:
  [
    {
        "flight_id": "6469aa91c46bbb6eeb53d4aa",
        "last_name": "Zaxos",
        "ticket_type": "eco",
        "username": "Thanasis1"
    },
    {
        "flight_id": "6469aa91c46bbb6eeb53d4aa",
        "last_name": "Zaxos",
        "ticket_type": "eco",
        "username": "Thanasis2"
    },
  ]
</pre>

<pre>
  #Reservation Info#
  
  Type: POST
  Url: http://0.0.0.0:5000/reservation-info
body:
  {
    "email":"zaxos2998@gmail.com",
    "reservation_id": "646dd65ac9c481fb867285c8"
  }
  
response:
  [
    {
        "flight_id": "6469aa91c46bbb6eeb53d4aa",
        "last_name": "Zaxos",
        "ticket_type": "eco",
        "username": "Thanasis1"
    },
    {
        "flight_id": "6469aa91c46bbb6eeb53d4aa",
        "last_name": "Zaxos",
        "ticket_type": "eco",
        "username": "Thanasis2"
    },
  ]
</pre>

<pre>
  #Cancel Reservation#
  
  Type: POST
  Url: http://0.0.0.0:5000/cancel-reservation
body:
 {
    "email": "zaxos2998@gmail.com",
    "reservation_id": "646de476760e6874a79c8091"
}
  
response:
  {
    "message": "Reservation canceled successfully"
  }
</pre>
