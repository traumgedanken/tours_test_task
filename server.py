"""If you want to run API server"""
from rest import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
