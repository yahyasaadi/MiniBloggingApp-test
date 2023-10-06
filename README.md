# MINI BLOGGING APP

## Prerequisites
Before you begin make sure you the following installed: 
* Python 3.11
* Django 
* Django REST framework
* Docker (for containerization)

## Installation
To install and run the application follow these steps:
* first go to your terminal
* then, navigate to the folder the you would like to host the app
* then copy the project using: 
```
git clone https://github.com/yahyasaadi/MiniBloggingApp-test.git
```
* Create a Python virtual environment (optional but recommended)
```
python -m venv yourvenv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install project dependencies:
```
pip install -r requirements.txt
```

### Run database migrations:
```
python manage.py migrate
```

### Start the Django development server
```
python manage.py runserver
```



### Access the application at `http://localhost:8000` in your web browser.

## Running with Docker
You can also run the application using Docker:
1. Bulid the Docker image
```
docker build -t blog-docker:0.0.1 .
```
2. Start the Docker container:
```
docker run -d -p 8000:8000 blog-docker:0.0.1
```
3. Access the application at `http://localhost:8000` in your web browser.

## Usage
* Use Postman to consume the API endpoints.
* Use the swagger API documentation at `http://127.0.0.1:8000/swagger/` to see all the endpoints.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.

## Support and contact details
You can reach me on:
* Gmail: yahyasnoor@gmail.com
* [twitter](https://twitter.com/yahyasnoor)

## License
The MIT Open source [License](https://opensource.org/licenses/MIT)

### List of contributors
* Yahya Saadi
