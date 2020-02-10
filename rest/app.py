"""Module with flask app behaviour implementation"""
import connexion

app = connexion.App(__name__, specification_dir='../documentation')
app.add_api('swagger.yml')
app.run(host='127.0.0.1', port=5000, debug=True)