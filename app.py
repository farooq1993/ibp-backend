from flask import Flask, jsonify
from utils.db_setup import init_db
from routes.create_user import createuser
from routes.login import userlogin
from routes.add_project import addproject
from routes.createmyc import myc

app = Flask(__name__)

init_db(app)


@app.route('/healthcheck', methods=['GET'])
def health_check():
    try:
        return jsonify({'msg':'Health api is working'})
    except:
        return jsonify({'error':'Health api is not working'})
    
# Register Blueprints
app.register_blueprint(createuser)
app.register_blueprint(userlogin)
app.register_blueprint(addproject)
app.register_blueprint(myc)




# main driver function
if __name__ == '__main__':
    app.run(debug=True)