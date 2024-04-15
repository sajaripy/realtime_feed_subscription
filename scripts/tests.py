import requests
import json

URL = "http://127.0.0.1:8000/"

def postLogin(username, password):
    myobj = {"username": username,
          "password": password}
    queryURL = URL + "login/"
    response = requests.post(queryURL, json = myobj)
    result = json.loads(response.text)
    return result

def postRegister(username, password, password2, role):
    myobj = {"username": username,
             "password": password,
             "password2": password2,
             "role": role}
    queryURL = URL + "register/"
    response = requests.post(queryURL, json = myobj)
    result = json.loads(response.text)
    return result

def postSubscribe(username, password, gc_name):
    myobj = {"username": username,
             "password": password,
             "gc_name": gc_name}
    queryURL = URL + "subscribe/"
    response = requests.post(queryURL, json = myobj)
    result = json.loads(response.text)
    return result

# def Socket(token):
#     myobj = {"authorization": "Bearer "+token}
#     queryURL = "ws://127.0.0.1:8000/ws/binance/"
#     response = requests.post(queryURL, json = myobj)
#     result = json.loads(response.text)
#     return result

if __name__ == '__main__':
    method = int(input("Please enter if you want to register(1), login(2) or subscibe(3) in int:"))
    if method == 1:
        username = input("Enter username:")
        password = input("Enter password:")
        password2 = input("Enter password again to confirm:")
        role = int(input("Enter role: 1 for normal user\n2 for microservices user:\n"))
        print(postRegister(username, password, password2, role))
    elif method == 2:
        username = input("Enter username:")
        password = input("Enter password:")
        print(postLogin(username, password))
    elif method == 3:
        username = input("Enter username:")
        password = input("Enter password:")
        gc_name = input("Enter gc name:")
        print(postSubscribe(username, password, gc_name))
    # elif method == 4:
    #     token = input("Enter token:")
    #     print(Socket(token))
    else:
        print("wrong input")
    