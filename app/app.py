from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# This is a demo, so a hard coded username and password is okay.
# This isn't something to do in production.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://appuser:94nfsUl7@localhost/appdata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Greeting(db.Model):
    """ A simple class to represent a greeting """

    gid = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80), unique=True)

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return '<Greeting %r>' % self.message

    @classmethod
    def get_or_create(cls, message):
        """ Gets or creates a Greeting """
        record = cls.query.filter(cls.message == message).first()

        if record:
            return record

        record = cls(message=message)
        db.session.add(record)
        db.session.commit()

        return record

@app.route("/", methods=['GET', 'POST'])
def main():
    """ The index.html route """
    if request.method == 'POST':
        # Safely get form data
        greeting_msg = request.form.get('greeting')
        if greeting_msg:
            Greeting.get_or_create(greeting_msg)

    return render_template('index.html', greetings=Greeting.query.all())

with app.app_context():
    # Make sure the tables exist
    db.create_all()

    # Create some records.
    try:
        Greeting.get_or_create("Hello!")
        Greeting.get_or_create("Hola!")
        Greeting.get_or_create("Ciao!")
    except Exception as e:
        # Ignore errors if DB isn't ready or data exists
        print(f"Startup data skipped: {e}")

if __name__ == "__main__":
    app.run()