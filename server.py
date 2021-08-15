from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    print(request.data)
    return {'success': True}

if __name__ == '__main__':
    try:
        app.run(debug=False, host="0.0.0.0", port="5000")
    except KeyboardInterrupt:
        pass
    finally:
        print('Exited')
