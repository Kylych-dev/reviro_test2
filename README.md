# API Documentation

Here is a list of available endpoints for the API:

| Endpoint                                | Description                         |
|-----------------------------------------|-------------------------------------|
| `api/v1/register/partner/`              | Регистрация партнера                |
| `api/v1/register/admin/`                | Регистрация администратора          |
| `api/v1/register/user/`                 | Регистрация обычного пользователя   |
| `api/v1/login/`                         | Вход пользователя                   |
| `api/v1/logout/`                        | Выход пользователя                  |
| `api/v1/password-reset/`                | Запрос на сброс пароля              |
| `api/v1/users_update/<pk>/`             | Обновление данных пользователя      |
| `api/v1/partner_update/<pk>/`           | Обновление данных партнера          |
| `api/v1/chat-msg/`                      | Создание сообщения чата             |
| `api/v1/beverage/`                      | Получение списка всех напитков      |
| `api/v1/beverage/create/`               | Создание нового напитка            |
| `api/v1/beverage/update/<pk>/`          | Обновление информации о напитке    |
| `api/v1/beverage/delete/<pk>/`          | Удаление напитка                   |
| `api/v1/establishment/`                 | Получение списка всех заведений     |
| `api/v1/establishment/create/`          | Создание нового заведения          |
| `api/v1/establishment/update/<pk>/`     | Обновление информации о заведении  |
| `api/v1/establishment/delete/<pk>/`     | Удаление заведения                 |
| `api/v1/order/`                         | Получение списка всех заказов      |
| `api/v1/order/create/`                  | Создание нового заказа             |
| `api/v1/order/update/<pk>/`             | Обновление информации о заказе     |
| `api/v1/order/delete/<pk>/`             | Удаление заказа                    |
| `api/v1/qr_code/`                       | Получение списка всех QR-кодов     |
| `api/v1/qr_code/create/`                | Создание нового QR-кода            |
| `api/v1/qr_code/update/<pk>/`           | Обновление информации о QR-коде    |
| `api/v1/qr_code/delete/<pk>/`           | Удаление QR-кода                   |
|-----------------------------------------|-------------------------------------|


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



