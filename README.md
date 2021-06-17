# Amazon Clone Backend

## Project basic setup
- Create a folder name `amazon-clone`
- Navigate to the above folder using `terminal/CMD`
- Clone the project
- Go inside the folder using `cd amazon-clone-backend`
- Run following command to set up the backend server
    1) Install virtual environment `pip install virtualenv`
    2) Create virtual environment `virtualenv env`
    3) Start virtual environment
        1) Windows: `env\Scripts\activate`
        2) mac / linux: `source env/bin/activate`
    4) Install all requirements `pip install -r requirements.txt`
    5) Create database `python manage.py migrate`
    6) Finally, runserver the server on `5000 PORT` using the command `python manage.py runserver 5000`
    7) From next time repeat steps from `5` if you have pull the code or else always run from step `6`
    
- Now your server is up and running on http://localhost:5000/
- Now setup [frontend](https://github.com/KaranRohra/amazon-clone-frontend/)
  
- At the end, your project structure should look like:
    - amazon-clone
        - amazon-clone-backend
          - other files
          - env
            - other files
        - amazon-clone-frontend
            - other files
    
- Note: Make sure you have python >= 3.8
- Remember: Always `run backend server` before `frontend` otherwise `frontend` not work