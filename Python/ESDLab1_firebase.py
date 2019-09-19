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
import pyrebase

global config
global auth
global db
config = {
	"apiKey": "AIzaSyDlc1yS_SNO1cbMwYgaYHvimweNvMv6g-g",
    "authDomain": "esdlab1.firebaseapp.com",
    "databaseURL": "https://esdlab1.firebaseio.com",
    "projectId": "esdlab1",
    "storageBucket": "",
    "messagingSenderId": "164859917448",
    "appId": "1:164859917448:web:508f432bf1923e84891b3d"
}

firebase = pyrebase.initialize_app(config)
#Get a reference to the auth service
auth = firebase.auth()
#Log the user in (For secure Database)
#user = auth.sign_in_with_email_and_password(email, password)
#Get a reference to the database service
db = firebase.database()
#state = bool(db.child("state").get().val())

#INITIALIZE
def basic_initze_fb(config):
  global auth
  global db
  try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
    print('connected')
    tb = threading.Thread(target = poll_firebase())
    tb.daemon = True
    tb.start()
  except Exception as e:
    print(e)

def Push_data_firebase(temp_int,light_int,time_str,config):
  global auth
  global db
  firebase = pyrebase.initialize_app(config)
  auth = firebase.auth()
  db = firebase.database()
  curr_temp = temp_int
  curr_light = light_int
  curr_time = time_str
  temp = { 'temp' : curr_temp,'light' : curr_light,'timeStamp' : curr_time}
  db.child("log").push(temp)

#Read from database
def get_state_firebase(state):
  global config
  global auth
  global db
  firebase = pyrebase.initialize_app(config)
  auth = firebase.auth()
  db = firebase.database()
  state = bool(db.child("state").get().val())

  


if __name__=="__main__":
  entries = []

  curr_temp = 666
  curr_light = 1210
  curr_time = "2"

  entries.append({
    'temp' : curr_temp,
    'light' : curr_light,
    'timeStamp' : curr_time 
    })

  print(entries)

  #Push to database
  db.child("log").push(temp)
