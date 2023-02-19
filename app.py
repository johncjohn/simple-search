from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Define the database connection string
db_conn_str = "postgresql://dbuser:dbpass@database/mydb"

# Create the database engine
engine = create_engine(db_conn_str)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a declarative base
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

# Create the database schema
Base.metadata.create_all(engine)

# Define a route that uses the database
@app.route('/')
def index():
    # Create a session
    session = Session()

    # Query the database
    users = session.query(User).all()

    # Close the session
    session.close()

    # Render the results
    return 'Users: {}'.format(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
