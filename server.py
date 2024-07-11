from flask import Flask, render_template, request, jsonify
import json
import chatgpt
app = Flask(__name__)

# the home route
@app.route('/')
def welcome():
    return render_template('index.html')


x = ''


async def text(txt):
    global x
    x = txt
    return x


async def anr():
    global x
    return chatgpt.answer(str(x))


# THE ROUTE FOR THE GET REQUEST
@app.route('/answer', methods=['GET'])
async def answer():
    if request.method == 'GET':
        ex = {
            'data': await anr()
        }
        jsonStr = json.dumps(ex)
        return jsonify(Response=jsonStr)




# The route for post request
@app.route("/reciver", methods=['POST'])
async def reciver():
    data = request.json
    txt = data['data']
    print(await text(txt))
    return ""


if __name__ == '__main__':
    app.run()
