"""Module with flask app behaviour implementation"""
import connexion

app = connexion.App(__name__, specification_dir='../documentation')
app.add_api('swagger.yml')
