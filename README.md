# API Documentation

Here is a list of available endpoints for the API:

| Endpoint             | Description                     |
|----------------------|---------------------------------|
| `admin/`      | Admin panel         |
| `swagger/` | Swagger  Document API endpoints, including parameters, request bodies, and response schemas.|
| `redoc/`       | Redoc  Document API endpoints, including parameters, request bodies, and response schemas.          |
| `api/v1/product/`  | List all products  |
| `api/v1/product/create/`       | Create a new product            |
| `api/v1/product/update/<pk>/`  | Update an existing product (identified by its primary key)
| `api/v1/product/delete/<pk>/`       | Delete an existing product (identified by its primary key)          |
| `api/v1/establishment/`  | List all establishments  |
| `api/v1/establishment/create/`       | List and create songs           |
| `api/v1/establishment/update/<pk>/`  | Update an existing establishment (identified by its UUID) |
| `api/v1/establishment/delete/<pk>/`       | Delete an existing establishment (identified by its UUID)          |

<br>
<br>


For more detailed information, refer to the API documentation.

# Reviro

This project is a simple product inventory management system. It allows users to add, 
update, delete, and view information about establishments and products in the inventory.

## Getting Started

Follow these steps to get the project up and running:

1. ### Clone the repository:<br>
    ```git clone https://github.com/Kylych-dev/reviro_test.git``` <br>
    ```cd reviro_test```
2. ### Build and run containers using Docker Compose: <br>

    Start containers in the foreground and build images.<br>
    ```docker-compose up --build``` <br>

    Start containers in the background.<br>
    ``` docker-compose up -d``` <br>
    
    Create database migrations.<br>
    ``` docker exec -it my_container sh -c 'python3 manage.py makemigrations'``` <br>
    
    Apply migrations to create the database schema.<br>
    ``` docker exec -it my_container sh -c "python3 manage.py migrate"``` <br>
    
    Stop and remove containers, networks, and volumes.<br>
    ``` docker compose down ``` <br>


3. ### Access Swagger documentation:

    Open your browser and navigate to the following URL: <br>
    ```http://localhost:8000/swagger/``` <br>
    Here you will find documentation for all available API endpoints, including parameters, request bodies, and response schemas.<br>


4. ### Using the API

    You can use any HTTP client, such as curl or Postman, to send requests to the API. Below are examples of requests and expected responses: <br>
    Get a list of establishments (GET /establishments/): <br>

    ```curl -X GET http://localhost:8000/establishments/``` <br>
    
    #### Response:
    ```
    [
        {
            "name": "Example Establishment",
            "description": "Description of the establishment",
            "locations": "Location 1, Location 2",
            "opening_hours": "9:00 AM - 5:00 PM",
            "requirements": "Requirements for the establishment"
        },
        {
            "name": "Another Establishment",
            "description": "Another description",
            "locations": "Location 3, Location 4",
            "opening_hours": "8:00 AM - 6:00 PM",
            "requirements": "Other requirements"
        }
    ]
    ```

4. Add a new establishment (POST /establishments/): <br>
    ```curl -X POST -H "Content-Type: application/json" -d '{"name": "New Establishment", "description": "Description of the new establishment", "locations": "New Location", "opening_hours": "8:30 AM - 4:30 PM", "requirements": "New requirements"}' http://localhost:8000/establishments/```

    #### Response:
    ```
    {
        "name": "New Establishment",
        "description": "Description of the new establishment",
        "locations": "New Location",
        "opening_hours": "8:30 AM - 4:30 PM",
        "requirements": "New requirements"
    }
    ```


5. ### Stopping Containers: <br>
    ```docker-compose down```


## Contributing

`telegram: @mirbekov0909` <br>
<br>

`email: tteest624@gmail.com` <br>
<br>

`email: mirbekov1kylych@gmail.com`



