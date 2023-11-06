# pip install fastapi framework , provides automatic documentation generation, request validation 
# pip install uvicorn for running app

import uvicorn
import firebase_admin
from firebase_admin import credentials,auth,firestore
from datetime import datetime
from fastapi import FastAPI,HTTPException
import pyrebase
from models import Register,Login
from fastapi.responses import JSONResponse

config = {
   "apiKey": "AIzaSyDoVkCWENvvT1PLiBjHWI4qNxHsTashp6o",
  "authDomain": "fir-workpy.firebaseapp.com",
  "databaseURL": "https://fir-workpy-default-rtdb.firebaseio.com",
  "projectId": "fir-workpy",
  "storageBucket": "fir-workpy.appspot.com",
  "messagingSenderId": "554028189654",
  "appId": "1:554028189654:web:affc3d8b15f0872d8c8677",
  "measurementId": "G-LDLEE0EPBR"
}
# Create a FastAPI app instance
app = FastAPI(
    description= "this is app for firebase auth with fastapi",
    title="firebase auth",
    docs_url="/"
)


if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

firebase = pyrebase.initialize_app(config)


@app.post("/register")
async def register(user_data: Register):
    try:
        # Create user in Firebase Authentication
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password,
       
        )

        # Store user information in Firestore (excluding the password)
        created_at = datetime.now()
        user_doc_ref = db.collection("users").document(user.uid)
        user_doc_ref.set({
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "created_at": created_at
        })

        return JSONResponse(content={"message":f"User account register succesfuly {user.uid}"},
                            status_code=201)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
async def create_access_token(user_data:Login):
 
    try:
        user = firebase.auth().sign_in_with_email_and_password(email=user_data.email, password=user_data.password)
        token = user['idToken']
        return JSONResponse(content={"token": token},status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/profile")
async def profile():
    pass

@app.post("/retrive")
async def retrive():
    pass

@app.post("/update")
async def update():
    pass


# Run the application with uvicorn
if __name__ == "__main__":
    uvicorn.run("firebase_work:app", host="0.0.0.0", port=8000, reload=True)

