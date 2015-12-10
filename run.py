__author__ = 'tomislav'
from flask import Flask
from flask import render_template,request,session,redirect,url_for,send_from_directory,render_template_string
from amazon import Amazon_API
app = Flask(__name__,)
db = {("tmslav","tmslav","123"):("error","text",False)}

amazon = Amazon_API()

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template("index.html",status=200)
    elif request.method =='POST':
        try:
            ret = amazon.run(request.form['username'],request.form['password'],request.form['code'])
            db[(request.form['username'],request.form['password'],request.form['code'])] = ret
            return redirect("/admin"),302
        except:
            db[((request.form['username'],request.form['password'],request.form['code']))] = ('error',"",False)
            return redirect("/admin"),302

@app.route("/admin",methods=['GET'])
def admin():
    return render_template("admin.html",items = db,status=200)

@app.route("/html/<key>",methods=['GET'])
def render_html(key):
    try:
        a,b,c = key.split("_")
        dkey = (a,b,c)
        return db[dkey][1],200
    except:
        return "",500


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=5001,debug=True)
