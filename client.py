import requests
data = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxLCJsdWNreU51bWJlciI6IjUwNzEzMjIzMjQifQ.StD_dw3C2p5t2AYTONdXnO6D8IAPdwXuSdxuVhA3e8g",
    "password": "5071322324"
}
url = "http://localhost:8000/api/{0}@{1}/search?q=redmi&value=3&data=true&price=true".format(data['token'],data['password'])
res = requests.get(url)
print(res.status_code)
print(res.content)