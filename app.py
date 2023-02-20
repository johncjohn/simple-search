import os
import psycopg2
import openai
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")## Call the API key under your account (in a secure way) 
                                            ##and store it in .env file
#db_url = os.environ.get('DATABASE_URL')
#conn = psycopg2.connect(db_url)
#engine = create_engine(os.getenv('DATABASE_URL'))
engine = create_engine("postgresql://admin:LK1joKixSkHrItiDOyhAneLKIrWwmsv9@dpg-cfp0vk82i3mo4bvetdjg-a.oregon-postgres.render.com/institute")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# create a new user
user = User(name='John', email='john@example.com', password='secret')
session.add(user)
session.commit()

# retrieve all users
users = session.query(User).all()
print(users)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        intext = request.form["query"]
        response = GPT_Completion(intext)
        return render_template('creation.html', result=response)

    result = request.args.get("result")
    return render_template("index.html", result=result)


def GPT_Completion(intext):
  ## Call the API key under your account (in a secure way)
  #openai.api_key = ""
  response = openai.Completion.create(
      engine="text-davinci-002",
      prompt =  intext,#generate_prompt(intext),
      temperature = 0.6,
      top_p = 1,
      max_tokens = 64,
      frequency_penalty = 0,
      presence_penalty = 0
      )
  #return print(response.choices[0].text)
  return response.choices[0].text

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
