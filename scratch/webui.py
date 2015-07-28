from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
	return "hello world!"

run(app, host='localhost',port=8080)