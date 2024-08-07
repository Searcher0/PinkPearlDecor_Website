# PinkPearlDecor_Website

python app.py
to run

{
"username": "adminuser",
"password": "adminpassword",
"role": "admin",
"name": "Admin Name",
"permissions": "all"
}

{
"username": "adminuser",
"password": "adminpassword"
}

Method: POST
URL: http://127.0.0.1:5000/clients/1/add_note
Headers:
Key: Authorization
Value: Bearer <JWT_ACCESS_TOKEN> copy paste the result from last command
