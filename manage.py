from app import app
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
from config import Development
from app import db


app.config.from_object(Development)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
