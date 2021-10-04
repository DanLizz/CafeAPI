# CafeAPI
API of Cafes in London where we can work

# Search Cafes By Location
Example Request
http://127.0.0.1:5000/search?location=Peckham

PARAMS: 
location - eg:Peckham

# Get Random Cafe
Example Request
http://127.0.0.1:5000/random

# Get All Cafes
Example Request
http://127.0.0.1:5000/all

# Add New Cafe
Example Request
http://127.0.0.1:5000/add

'name=TY Seven Dials' \
'map_url=https://www.google.com/maps/place/TY+Seven+Dials/@51.5128761,-0.1295574,17z/data=!3m1!4b1!4m5!3m4!1s0x487604cd0ed11587:0x3feff9f93e76a986!8m2!3d51.5128986!4d-0.1273307' \
'img_url=https://lh3.googleusercontent.com/proxy/T-qwQSPyOINfr7Uo2oMWf7QG0ULxHUvEaNxwIipRGwWhFvcuvbBFR6DhaEbAZlqSwBXXwHl9MbPCPAsIBOWyKQ58gN9QgUd4-YiU4BlKoEBcqvD5DVMHFrmIAqdaXEt9t7PnBRXFSku0SX6gDp2LvMAHZ4fHljNr' \
'location=London' \
'seats=20-30' \
'has_toilet=1' \
'has_wifi=1' \
'has_sockets=1' \
'can_take_calls=0'


# Update Price For A Cafe by ID
Example Request
http://localhost:5000/update-price/22?new_price=£3.50

PARAMS: 
new_price - £3.50


# Delete A Cafe By ID
Example Request
http://127.0.0.1:5000/report_closed/22?api_key=MyToPsECRETapiKeyisThis

PARAMS: 
api_key - MyToPsECRETapiKeyisThis
