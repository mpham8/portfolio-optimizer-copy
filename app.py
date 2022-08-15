from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os.path
import shutil


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable = False)
  completed = db.Column(db.Integer, default = 0)
  date_created = db.Column(db.DateTime, default = datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' %self.id

# @app.route("/post_field", methods=["GET", "POST"])
# def need_input():
#   for key, value in request.form.items():
#     print("key: {0}, value: {1}".format(key, value))

# @app.route("/form", methods=["GET"])
# def get_form():
#   return render_template('index.html')

# @app.route('/optimize', methods=["GET", "POST"])
# def optimize():
#   print(request.form)
#   return render_template('index.html')


app.config["UPLOAD_FOLDER"] = "uploads/"

@app.route('/upload', methods = ['GET', 'POST'])
def display_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()   
        
        shutil.copy(os.path.join("uploads/", "stocks.csv"), os.getcwd())

        
    return render_template('index.html', content=content) 

# app.config["UPLOAD_PATH"] = "uploads/"

# @app.route('/upload', methods=["GET", "POST"])
# def upload_file():
#   if request.method == 'POST':
#     f = request.files['file_name']
#     f.save(os.path.join(app.config["UPLOAD_PATH"],f.filename))

#     return render_template("index.html", message = "uploaded")



#   # if request.method == "POST":
#   #   print(request.form["objective_function"])
#   #   print(request.form["target_return"])
#   #   return
#   return render_template("index.html", "please upload file")


@app.route('/', methods=["GET", "POST"])
def index():
  return render_template("index.html")


@app.route('/download')
def download():
    path = 'results.csv'
    return send_file(path, as_attachment=True)

@app.route('/calculate', methods=["GET", "POST"])
def calc():
  if request.method == 'POST':
    
    simulation_month = request.form['simulation_month']
    years_data = int(request.form['years_data'])
    max_position_size = float(request.form['max_position_size'])
    pricing_model = request.form['pricing_model']
    risk_model = request.form['risk_model']
    objective_function = request.form['objective_function']
    target_return = int(request.form['target_return'])
    #file_name = request.form['file']


    print(type(simulation_month))
    print(type(years_data))
    print(type(max_position_size))
    print(type(pricing_model))
    print(type(risk_model))
    print(type(objective_function))
    print(type(target_return))
    #print(file_name)
    
    # render_template('loading.html')
    import optimizer as op
    op.main(simulation_month, years_data, max_position_size, pricing_model, objective_function, target_return, risk_model)
    return redirect('/download')



  return redirect('/')



# @app.route('/')
# def index():
#   print(request.args)
#   dict = request.args
#   print(dict['pricing_model'])
  

#   return render_template('index.html')

if __name__ == '__main__':
  app.run(host="localhost", port=8000, debug=True)