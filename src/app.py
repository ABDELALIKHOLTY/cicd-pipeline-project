
from flask import Flask
app=Flask(__name__)
import json

json.load

@app.route('/')
def home():
    return 'hello everyone on this project that is titled by Production-Grade CI/CD Pipeline'

@app.route('/health')
def health():
    return {'status':'OK'}

@app.route("/profil")
def profil():
    return{
        'nom':'kholty',
        'prenom':'ali'


    }



if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001)
