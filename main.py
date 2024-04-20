from flask_login import current_user
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
user = current_user
