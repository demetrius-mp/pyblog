# pyblog

## Installation and execution
1. Clone the repository using the following command:
```
git clone git@github.com:demetrius-mp/pyblog.git
```

2. Change to the repository directory:
```
cd pyblog
```

3. Create a virtual environment and install the requirements:

- Using conda
```
conda create -n pyblog python=3.9
conda activate pyblog
pip install -r requirements.txt
```
- Using python venv
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create your .secrets.toml using the provided template
- [Defining a database connection string.](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)
- Creating your secret key:
```
openssl rand -base64 32
```

5. Run database migration:
```
flask db init
flask db migrate
flask db upgrade
```

6. Run the server:
```
flask run
```

- To run in development mode:
```
export FLASK_ENV=development
flask run
```
