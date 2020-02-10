"""Module with flask app behaviour implementation"""
import connexion

from service import Database

app = connexion.App(__name__, specification_dir='../documentation')
app.add_api('swagger.yml')
app.app.config['DATABASE'] = Database()

# app.run(host='127.0.0.1', port=5000)
