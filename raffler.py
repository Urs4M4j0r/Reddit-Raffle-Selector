from flask import Flask, request, render_template
import praw
from praw.models import MoreComments
from random import randint
from flask_mail import Mail, Message



app = Flask(__name__, static_url_path="/static")
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'XXXXXXXXXXXXXXX'
app.config['MAIL_PASSWORD'] = 'XXXXXXXXXXXXX'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/raffler')
def raffler():
    print('raffler')
    return render_template('raffler.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        url = request.form['url']
        result = getNames(url)
        return render_template('rafflerout.html',result = result)

def getNames(url):
    names = []
    
    reddit = praw.Reddit(client_id='XXXXXXX', client_secret='XXXXXXXXXXX', user_agent='Comment Raffle')
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None, threshold=0)
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        elif not top_level_comment.author:
            continue
        names.append(str(top_level_comment.author))
    res = []
    for i in names:
        if i not in res:
            res.append(i)
    randomUser = res[randint(0, len(res)-1)]
    print(randomUser)
    return randomUser

@app.route('/contact')
def contact():
    return render_template('contact.html') 


@app.route('/send', methods=['POST'])
def sendMail():
    if request.method == 'POST':
        name = str(request.form['name'])
        email = str(request.form['email'])
        message = str(request.form['message'])
        category = str(request.form['category'])
    message2 = name + ' has sent you an email of type ' + category + '. The message reads:   ' + message + '.    If you wish to reply, use: ' + email
    sendEmail(email,message2)
    return render_template('feedbacksuccess.html')

@app.route("/")
def sendEmail(email, message):
   msg = Message(
                'Hello',
                sender ='XXXXXXXXXXX',
                recipients = ['XXXXXXXXXXXX']
               )
   msg.body = message
   mail.send(msg)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    UPLOAD_FOLDER = '/files/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
