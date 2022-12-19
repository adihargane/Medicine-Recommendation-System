from os import name
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import pickle
from flask_mail import Mail, Message

application= Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

test=pd.read_csv("test_data.csv",error_bad_lines=False)
x_test=test.drop('prognosis',axis=1)

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = '@Xspax_@1'
application.config['MYSQL_DB'] = 'medicine'

 
mysql = MySQL(application)


mail = Mail(application) # instantiate the mail class

# configuration of mail
application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'medicination1@gmail.com'
application.config['MAIL_PASSWORD'] = 'Medicine@1234'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)


@application.route('/')
def Landing_page():
    return render_template('index.html')

  
@application.route('/check')
def check_page():
    return render_template('letscheck.html')

@application.route('/about')
def about_page():
    return render_template('about.html')
  
@application.route('/team')
def team_page():
    return render_template('team.html')
  
@application.route('/contact')
def contact_page():
    return render_template('contact.html')

@application.route('/send', methods =['GET','POST' ]  )
def send( ):
    
   
    if request.method=='POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']  
        message = request.form['message']
        cur=mysql.connection.cursor()
        cur.execute(" INSERT INTO contacts(name, address, email, phone, message)  VALUES( %s, %s, %s, %s, %s )", (name, address, email, phone, message) )
        mysql.connection.commit()
        cur.close()
        msg = Message(
                'Medicine ',
                sender ='medicination1@gmail.com',
                recipients = [email]
               )
        
        msg.html = render_template('mail.html')
        mail.send(msg)
        
        return render_template('ThankYou.html')
    
           
        
    return render_template('contact.html')



@application.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        col=x_test.columns
        inputt = [str(x) for x in request.form.values()]
 
        b=[0]*132
        for x in range(0,132):
            for y in inputt:
                if(col[x]==y):
                    b[x]=1
        b=np.array(b)
        b=b.reshape(1,132)
        prediction = model.predict(b)
        prediction=prediction[0]
        print(prediction)
    return render_template('letscheck.html', pred="The probable diagnosis says it could be {}".format(prediction))


if __name__=="__main__":
    application.run(debug=True,port=8001)