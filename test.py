from app import db, Todo, app 
import unittest
from os import environ
class TodoTests(unittest.TestCase):

    def setup(self):
        app.config["TESTING"] = True 
        app.config["WTF_CSRF_ENABLED"] = False 
        app.config["DEBUG"] = False 
        app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("TEST_DB_URL")
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.create_todo()
        self.assertEqual(app.debug, False)

    def create_todo(self):
        i1 = Todo(title="Complete CI/CD")
        i2 = Todo(title="Write a blog on this overkill expermient")

        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()

if __name__ == "__main__":
    unittest.main()
