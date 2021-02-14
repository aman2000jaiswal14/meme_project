##  Data Base Table

'''
create table memetable(
    memeid INT NOT NULL AUTO_INCREMENT,
       name VARCHAR(30) NOT NULL,
        caption VARCHAR(100) NOT NULL,
        url VARCHAR(40) NOT NULL,
        PRIMARY KEY ( memeid )
    );

'''

from flask import Flask,render_template,request
import mysql.connector

app = Flask(__name__)



class MemeDatabase:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # WRITE PASSWORD
            database=""  # DATABASE NAME
        )
    def read_db(self,id=None):

        mycursor = self.mydb.cursor()
        if(id==None):
            mycursor.execute("SELECT * FROM memetable")
        else:
            mycursor.execute("SELECT * FROM memetable where memeid={}".format(id))
        meme_table = mycursor.fetchall()
        memes = []
        for meme in meme_table[::-1]:
            memes.append({
                "memeid":meme[0],
                "name": meme[1],
                "caption":meme[2],
                "url":meme[3]
            }
            )
        return memes

    def write_db(self,name,caption,url):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO memetable (name, caption, url) VALUES (%s, %s, %s)"
        val = (name,caption,url)
        mycursor.execute(sql, val)

        self.mydb.commit()
    def __del__(self):
        self.mydb.close()
@app.route('/',methods=["POST","GET"])
def index():
    return render_template('index.html')

@app.route('/postmeme',methods=["GET","POST"])
def postmeme():
    try:
        if request.method=="POST":
            name = request.form["name"]
            caption = request.form["caption"]
            url = request.form["url"]
            db = MemeDatabase()
            db.write_db(name,caption,url)

            return render_template('postmeme.html')
    except Exception as e:
        print(e)

        pass
@app.route('/memes',defaults={'id': None},methods=["GET","POST"])
@app.route('/memes/<id>',methods=["GET"])
def memes(id=None):
    try:
        db = MemeDatabase()
        if(id!=None):
            memes = db.read_db(id)
        else:
            memes = db.read_db()
        return render_template('memes.html',memes=memes)
    except Exception as e:
        print(e)

if __name__=="__main__":
    app.run()