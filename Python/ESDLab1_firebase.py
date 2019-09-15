'''
<script>
  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyDlc1yS_SNO1cbMwYgaYHvimweNvMv6g-g",
    authDomain: "esdlab1.firebaseapp.com",
    databaseURL: "https://esdlab1.firebaseio.com",
    projectId: "esdlab1",
    storageBucket: "",
    messagingSenderId: "164859917448",
    appId: "1:164859917448:web:508f432bf1923e84891b3d"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
</script>
'''
<<<<<<< HEAD
import pyrebase
=======

import pyrebase

>>>>>>> c3f212e69b9f7f1435bf26fd428e10f8b2e8543d
config = {
	"apiKey": "AIzaSyDlc1yS_SNO1cbMwYgaYHvimweNvMv6g-g",
    "authDomain": "esdlab1.firebaseapp.com",
    "databaseURL": "https://esdlab1.firebaseio.com",
    "projectId": "esdlab1",
    "storageBucket": "",
    "messagingSenderId": "164859917448",
    "appId": "1:164859917448:web:508f432bf1923e84891b3d"
}
<<<<<<< HEAD
firebase = pyrebase.initialize_app(config)
#Get a reference to the auth service
auth = firebase.auth()
#Log the user in (For secure Database)
#user = auth.sign_in_with_email_and_password(email, password)
#Get a reference to the database service
db = firebase.database()
entries = []
print(entries)
curr_temp = 26
curr_light = 5
curr_time = 0
entries.append({
	'temp' : curr_temp,
	'light' : curr_light,
	'timestamp' : curr_time 
	})
print(entries)
db.child("log").set(entries)

=======

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in (For secure Database)
#user = auth.sign_in_with_email_and_password(email, password)

# Get a reference to the database service
db = firebase.database()

entries = []
print(entries)

curr_temp = 295
curr_light = 10
curr_time = "0"

entries.append({
	'temp' : curr_temp,
	'light' : curr_light,
	'timeStamp' : curr_time 
	})

temp = { 'temp' : curr_temp,
  'light' : curr_light,
  'timeStamp' : curr_time 
  }

print(entries)

#Push to database
db.child("log").push(temp)

#Read from database
state = bool(db.child("state").get().val())
print(state);
>>>>>>> c3f212e69b9f7f1435bf26fd428e10f8b2e8543d
