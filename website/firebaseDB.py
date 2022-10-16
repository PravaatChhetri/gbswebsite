import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyBG2PYPubUrbWpIXU0wggIGw55aplGap8Y",
  'authDomain': "ground-booking-system-f797d.firebaseapp.com",
  'projectId': "ground-booking-system-f797d",
  'storageBucket': "ground-booking-system-f797d.appspot.com",
  'messagingSenderId': "320915277594",
  'appId': "1:320915277594:web:396a7464ccf7a08d398ea3"
}

firebase = pyrebase.initialize_app(firebaseConfig)