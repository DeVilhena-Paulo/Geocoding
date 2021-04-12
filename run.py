from api.app import get_app
from api.port import PORT

app = get_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
