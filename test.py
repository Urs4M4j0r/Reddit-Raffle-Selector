from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)
   else:
        return 'ERROR'

if __name__ == '__main__':
   app.run(host="127.0.0.1", port=8080, debug=True)
