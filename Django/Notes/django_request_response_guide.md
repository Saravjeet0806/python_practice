# How Python Django Request and Response Work

This guide explains what happens when a browser or frontend sends a
request to a Django application and how Django returns a response.

## 1. The big picture

A **request** is a message sent by a client (browser, mobile app, or
React frontend) to the server.

A **response** is the message the server sends back.

Typical flow:

``` text
Browser / React frontend
        |
        |  HTTP request
        v
Web server / WSGI or ASGI
        |
        v
Django middleware (request phase)
        |
        v
URL dispatcher (urls.py)
        |
        v
View function or class (views.py)
        |
        +----> Model / Database (if needed)
        |
        v
Django middleware (response phase)
        |
        v
HTTP response
        |
        v
Browser / React frontend
```

## 2. What is an HTTP request?

An HTTP request contains information that tells the server what the
client wants.

For example:

``` http
GET /api/products/ HTTP/1.1
Host: example.com
Accept: application/json
Authorization: Bearer <token>
```

The important parts are:

  -----------------------------------------------------------------------
  Part                                Meaning
  ----------------------------------- -----------------------------------
  Method                              The action, such as `GET`, `POST`,
                                      `PUT`, `PATCH`, or `DELETE`

  Path                                The endpoint being requested, such
                                      as `/api/products/`

  Headers                             Extra information, such as content
                                      type or authorization

  Query parameters                    Optional values in the URL, such as
                                      `?page=2`

  Body                                Data sent with requests such as
                                      `POST`, `PUT`, or `PATCH`
  -----------------------------------------------------------------------

### Common HTTP methods

  Method     Typical purpose
  ---------- -------------------------------------
  `GET`      Read or retrieve data
  `POST`     Create data or trigger an operation
  `PUT`      Replace a resource
  `PATCH`    Partially update a resource
  `DELETE`   Delete a resource

A method does not automatically perform the action. Your Django view
defines what happens.

## 3. How Django receives a request

Suppose the frontend sends:

``` http
GET /api/hello/?name=Sam
```

Django receives the HTTP request through its WSGI or ASGI application.
The server interface depends on how the Django project is deployed.

Django then creates an `HttpRequest` object. The view receives this
object as its first argument, conventionally named `request`.

The request object provides information such as:

-   `request.method` --- HTTP method.
-   `request.path` --- requested path.
-   `request.GET` --- query-string parameters.
-   `request.POST` --- form data from POST requests.
-   `request.body` --- raw request body bytes.
-   `request.headers` --- request headers.
-   `request.user` --- authenticated user, when authentication
    middleware is configured.
-   `request.COOKIES` --- cookies sent by the client.

For JSON APIs, you commonly read and parse `request.body` rather than
using `request.POST`.

## 4. URL routing: `urls.py`

Django checks the URL patterns in your project's URL configuration and
selects the matching view.

**project/urls.py**

``` python
from django.urls import path
from myapp import views

urlpatterns = [
    path("api/hello/", views.hello),
]
```

This tells Django:

-   If the requested path is `/api/hello/`,
-   call the `hello` view.

URL routing chooses the view; it does not itself generate the response.

## 5. The view: `views.py`

A view contains the application logic. It receives the request and must
return a response.

**myapp/views.py**

``` python
from django.http import JsonResponse

def hello(request):
    name = request.GET.get("name", "Guest")

    return JsonResponse({
        "message": f"Hello, {name}!"
    })
```

If the client requests:

``` text
GET /api/hello/?name=Sam
```

Django reads `name` from `request.GET` and returns JSON:

``` json
{
  "message": "Hello, Sam!"
}
```

`JsonResponse` serializes a Python dictionary into JSON and sets an
appropriate JSON content type.

## 6. Reading data from different places

### Query parameters

URL:

``` text
/api/products/?category=books&page=2
```

View:

``` python
def products(request):
    category = request.GET.get("category")
    page = request.GET.get("page", "1")
```

Use `request.GET` for values in the URL after `?`.

### JSON request body

A React frontend might send:

``` javascript
fetch("/api/users/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "name": "Sam",
        "email": "sam@example.com"
    })
});
```

A basic Django view can parse the JSON body:

``` python
import json
from django.http import JsonResponse

def create_user(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    name = data.get("name")

    if not name:
        return JsonResponse(
            {"error": "Name is required"},
            status=400
        )

    return JsonResponse(
        {"message": "User data received", "name": name},
        status=201
    )
```

In a production API, validate all input and use Django forms, model
forms, or a serializer layer such as Django REST Framework serializers.
Also handle authentication, permissions, and database errors
appropriately.

**Important:** `request.POST` is primarily for form-encoded and
multipart form submissions. It does not automatically parse a JSON
request body.

## 7. How Django creates a response

A view returns an HTTP response object. Common choices include:

### `HttpResponse`

Useful for plain text or HTML:

``` python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Django!")
```

### `JsonResponse`

Useful for JSON APIs:

``` python
from django.http import JsonResponse

def status(request):
    return JsonResponse({
        "status": "success"
    })
```

### `render`

Useful when Django renders an HTML template:

``` python
from django.shortcuts import render

def home(request):
    return render(request, "home.html", {
        "username": "Sam"
    })
```

### Redirect response

Useful when the client should navigate to another URL:

``` python
from django.shortcuts import redirect

def go_home(request):
    return redirect("/")
```

## 8. HTTP status codes

The response includes a status code that describes the result.

  -----------------------------------------------------------------------
  Code                    Meaning                 Typical use
  ----------------------- ----------------------- -----------------------
  `200`                   OK                      Request succeeded

  `201`                   Created                 A resource was created

  `204`                   No Content              Succeeded, with no
                                                  response body

  `400`                   Bad Request             Invalid input

  `401`                   Unauthorized            Authentication is
                                                  required or invalid

  `403`                   Forbidden               User is not allowed to
                                                  perform the action

  `404`                   Not Found               Resource or route was
                                                  not found

  `405`                   Method Not Allowed      Endpoint does not
                                                  support that HTTP
                                                  method

  `500`                   Internal Server Error   Unexpected server-side
                                                  failure
  -----------------------------------------------------------------------

Example:

``` python
return JsonResponse(
    {"message": "Product created"},
    status=201
)
```

## 9. What is middleware?

Middleware is a layer that can process requests before they reach the
view and responses before they are sent to the client.

Examples of middleware responsibilities include:

-   Session handling.
-   Authentication.
-   Security-related processing.
-   CSRF protection.
-   Common request and response processing.

Simplified lifecycle:

``` text
Request
  |
  v
Middleware 1
  |
  v
Middleware 2
  |
  v
View
  |
  v
Middleware 2 (response processing)
  |
  v
Middleware 1 (response processing)
  |
  v
Response
```

The actual middleware behavior depends on the middleware classes and
their order in `MIDDLEWARE` in `settings.py`. Middleware can also return
a response early, without calling the view.

## 10. Complete request-response example

Imagine a React frontend needs a list of products.

### Step 1: React sends a request

``` javascript
fetch("http://localhost:8000/api/products/")
    .then(response => response.json())
    .then(data => console.log(data));
```

### Step 2: Django URL configuration

``` python
# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("api/products/", views.get_products),
]
```

### Step 3: Django view returns JSON

``` python
# views.py

from django.http import JsonResponse

def get_products(request):
    products = [
        {"id": 1, "name": "Laptop", "price": 50000},
        {"id": 2, "name": "Mouse", "price": 500}
    ]

    return JsonResponse({
        "success": True,
        "products": products
    })
```

### Step 4: Django sends the response

Example response body:

``` json
{
  "success": true,
  "products": [
    {
      "id": 1,
      "name": "Laptop",
      "price": 50000
    },
    {
      "id": 2,
      "name": "Mouse",
      "price": 500
    }
  ]
}
```

### Step 5: React reads the response

The frontend parses the JSON and can use `data.products` to display the
products.

Note: `fetch()` does not reject its promise just because the server
returns an HTTP error such as `404` or `500`. Check `response.ok` or
`response.status` before treating the result as successful.

``` javascript
fetch("http://localhost:8000/api/products/")
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data.products);
    })
    .catch(error => {
        console.error(error);
    });
```

## 11. What happens when an error occurs?

Django may return an error response when:

-   No URL pattern matches the requested path (`404`).
-   The view does not allow the requested HTTP method (`405`, if handled
    by the view).
-   Input validation fails (`400`, if your code returns it).
-   The user is not authenticated (`401`, depending on the
    authentication/API setup).
-   An unexpected exception occurs (`500`, unless handled).

For APIs, return clear and consistent error messages without exposing
secrets, stack traces, or internal implementation details to clients.

## 12. Important concepts to remember

1.  The **client** sends an HTTP request.
2.  Django receives it through its WSGI or ASGI application.
3.  Middleware can process the request.
4.  URL routing selects the matching view.
5.  The view runs application logic and may interact with models and the
    database.
6.  The view returns an HTTP response.
7.  Middleware can process the response.
8.  The client receives the response and handles its status, headers,
    and body.

### Request vs response

  -----------------------------------------------------------------------
  Request                             Response
  ----------------------------------- -----------------------------------
  Sent by the client                  Sent by the server

  Contains method, URL, headers, and  Contains status code, headers, and
  possibly a body                     possibly a body

  Available in Django as `request`    Returned by the view as an HTTP
                                      response object

  Example: `request.GET.get("id")`    Example: `JsonResponse({"id": 1})`
  -----------------------------------------------------------------------

## 13. A simple mental model

Think of Django like a restaurant:

-   **Client:** Customer placing an order.
-   **URL:** The counter or department that receives the order.
-   **Middleware:** Security and checks at the entrance and exit.
-   **View:** Staff member who handles the order.
-   **Model/database:** Store room where information is retrieved or
    saved.
-   **Response:** The completed order delivered to the customer.

The key idea is:

> A Django view takes a request, performs the required work, and returns
> a response.
