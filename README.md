# Django Ajax recording

This is the follow-up repository for the [live recording tutorial](https://dev.to/sirneij/django-and-ajax-building-a-recording-application-4j0a) on dev.to

## Run locally

To run locally

- Clone this repo:
  ```
   git clone https://github.com/Sirneij/django-ajax-record.git
  ```
- Change directory into the folder:
  ```
   cd django-ajax-record
  ```
- Create a virtual environment:
  ```
   virtualenv -p python3.8 env
  ```
  You might opt for other dependencies management tools such as `pipenv` or `venv`. It's up to you.
- Activate the environment:
  - For Linux and Mac machines
    ```
    source env/bin/activate
    ```
  - For Windows machine:
    ```
    .\env\Scripts\activate
    ```
- Install the dependencies:
  ```
  pip install -r requirements.txt
  ```
- Modify `core/models.py` if you are not using Cloudinary as your storage service.
  - From
  ```
    voice_record = models.FileField(upload_to="records", storage=RawMediaCloudinaryStorage())
  ```
  - To
  ```
    voice_record = models.FileField(upload_to="records")
  ```
- Make migrations and migrate the database:
  ```
   python manage.py makemigrations
   python manage.py migrate
  ```
- Finally, run the application:
  ```
   python manage.py runserver
  ```
  Visit http://localhost:8000 in your browser

# Live version

This application is currentlly live [here](https://django-record.herokuapp.com/)
