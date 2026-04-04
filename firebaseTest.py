from firebase import firebase
def readFirebase():
    firebase1 = firebase.FirebaseApplication('https://augmentedreality-af310-default-rtdb.firebaseio.com/', None)
    temp = firebase1.get('/AE443/temp', None)
    humidity = firebase1.get('/AE443/humidity', None)
    moisture = firebase1.get('/AE443/moisture', None)
    return(temp,humidity,moisture)

#readFirebase()

# def writeFirebase(pump):
#     firebase1 = firebase.FirebaseApplication('https://augmentedreality-af310-default-rtdb.firebaseio.com/', None)
#     result = firebase1.put('AE353','pumpControl',pump)
#     print(result)


#writeFirebase('4',900,500,6,7000)
#print(writeFirebase('Black Rot'))
#print(readFirebase())