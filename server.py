from flask import Flask,render_template,request,jsonify
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def welcome():
          
        # print(data['body']) 
        return render_template('index.html')

@app.route("/reciver",methods = ['GET','POST'])
def reciver():
        txt ='o'
        if request.method == 'POST':
          data = request.json
          txt= data['data']
          print(txt)
        
        elif request.method == 'GET':
                     ex = {
                          'data': "hello world"
                     }
                     jsonStr = json.dumps(ex)
                     return jsonify(Response=jsonStr)
        #  print(request.json)

        return txt
                 
        


if __name__ == '__main__':
    app.run()