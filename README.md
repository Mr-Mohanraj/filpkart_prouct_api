# Flipkart Product List API (not official)

Flipkart product list API (Not officially):

* API had a flipkart.com scrape data and set it to users based on their needs.

* Download [python](https://www.python.org/downloads/)
    *check python installation correctly go to the terminal or command prompt

* *python -V*  your current python  version will be printed out like this: "*Python 3.9.9*"

* **pip install -r requirements.txt**

* python (for Windows) or python3 (not for Windows): manage.py runserver

* Check the API using the blow end point

* First user, the `user/*` Endpoint to create the user.

* Second, use the `developer/*` endpoint to create an API access token.

* third, use the api/`Your API token@api token password`/search?q=`your search query here`
    `Like this: http://localhost:8000/api/token@password/search?q=iphone&all=true here true is a case sensitive`

## Endpoints and HTTP Methods

| Endpoints                      | HTTP Methods |
| -------------                  |:-------------:|
|user/register/                  | post         |
|user/login/                     | post     |
|user/user/                      | get     |
|user/refresh/                   | post             |
|user/reset/                     | post          |
|user/forgot/                    | post          |
|developer/<str:username>/create/| get        |
|developer/<str:username>/refresh| get             |
|developer/<str:username>/view/ | get      |
|developer/<str:username>/delete/| get      |
|api/<str:token>@<str:password>/| post    |
|api/<str:token>@<str:password>/search/|get   |

### query variable and their default values on **api/<str:token>@<str:password>/search/** endpoint

{

* "q": "redmi", Return name of the product.
* "product_length": 10, Return the first number of product.
* "data": False, If true, Return all only name of the q variable value.
* "based_price": True, Return only price for first product_length value.
* "all": False, Return all product form database.

}

## Inside Apps

* authenticationApi
* productApi
  
### Third Party library

* [drf_spectacular](https://www.bing.com/ck/a?!&&p=a60dcbdabe1258aaJmltdHM9MTY3OTE4NDAwMCZpZ3VpZD0xMmM2MGIyOC0yMmNkLTY4ZWEtMTgwOC0xOWZiMjM3ZjY5NTcmaW5zaWQ9NTE5Mg&ptn=3&hsh=3&fclid=12c60b28-22cd-68ea-1808-19fb237f6957&psq=drf+spectacular&u=a1aHR0cHM6Ly9kcmYtc3BlY3RhY3VsYXIucmVhZHRoZWRvY3MuaW8vZW4vbGF0ZXN0L3JlYWRtZS5odG1s&ntb=1)
  For API auto document and swagger(open API). This feature is not available(In processing).
