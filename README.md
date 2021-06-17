# Amazon Clone Backend

## Project basic setup
- Create a folder name `amazon-clone`
- Navigate to the above folder using `terminal/CMD`
- Clone the project
- Go inside the folder using `cd amazon-clone-backend`
- run following command to set up run the backend server
    1) Install all requirements `pip install -r requirement.txt`
    2) Install virtual environment `pip install virtualenv`
    3) Create virtual environment `virtualenv env`
    4) Start virtual environment
        1) Windows: `env\Scripts\activate`
        2) mac / linux: `source env/bin/activate`
    5) Create database `python manage.py migrate`
    6) Finally, runserver the server on `5000 PORT` use the command `python manage.py runserver 5000`
    
- Now your server is up and running on `http://localhost:5000/`
- Now setup `frontend` so that you can see `amazon-clone` `UI`
Use this link to follow the `readme file` `https://github.com/KaranRohra/amazon-clone-frontend/issues`
  
- At the end your project should look like:
    - amazon-clone
        - amazon-clone-backend
            - other files
        - amazon-clone-frontend
            - other files
    
- Note: Make sure you have python>=3.8
- Remember: Always `run backend server` before `frontend` otherwise `frontend` not work