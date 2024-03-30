import kvant_py
import requests

# Create user
kvant_py.create_user("", "", "", "", "", "")

print(requests.get("http://127.0.0.1:8000/check_login_credentials?login=admin&password=1234").text)
