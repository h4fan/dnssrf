from flask import Flask, redirect, render_template, request, jsonify, send_file
from dbop import log2db, getrecords
from config import API_TOKEN,REDIRECT_30x_Code,REDIRECT_30x_Value,REDIRECT_30x_Check

import random

app = Flask(__name__, static_url_path='')


def randomtemplate():
	return random.choice(["404.html","test.html","test1.html","test2.html","test3.html"])

def logrequest():
    fullrequest = request.url + "\r\n"
    fullrequest += "%s %s %s\r\n" % (request.method,request.full_path,request.environ.get('SERVER_PROTOCOL'))
    for key, value in request.headers.items():
        fullrequest += "%s:%s\r\n" % (key,value)
    if(request.content_length is not None):
        if(int(request.content_length) > 1000):
            fullrequest += "\r\n\r\ncontent too long"
        elif(int(request.content_length) < 1000 and int(request.content_length) > 0):
            fullrequest += "\r\n%s" %  request.get_data(as_text=True)
        else:
            pass
    if("X-Real-Ip" in request.headers.keys()):
        log2db(request.headers["X-Real-Ip"],"HTTP",request.host.split(":")[0],fullrequest)
    else:
        log2db(request.remote_addr,"HTTP",request.host.split(":")[0],fullrequest)


app.before_request(logrequest)


@app.route("/", methods=['GET', 'POST'])
def list2():
    return render_template(randomtemplate())



@app.route("/hydra", methods=['GET', 'POST'])
def hydra():
    if("X-Hydra" in request.headers.keys() and request.headers["X-Hydra"] == API_TOKEN):
        return jsonify(getrecords())
    return render_template(randomtemplate())

@app.route("/ok", methods=['GET', 'POST'])
def lok():
    return render_template("404.html")

@app.route("/30", methods=['GET', 'POST'])
def red30():
    return redirect(REDIRECT_30x_Check, code=REDIRECT_30x_Code)


@app.route("/r/<name>", methods=['GET', 'POST'])
def red30_random(name):
    return redirect(REDIRECT_30x_Value, code=REDIRECT_30x_Code)


@app.route("/shell.php", methods=['GET', 'POST'])
def zipbomb():
    return send_file('static/zbsm.zip', mimetype='application/zip', as_attachment=True, attachment_filename='archive.zip')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template(randomtemplate()), 200

@app.errorhandler(405)
def page_not_found(e):
    # note that we set the 404 status explicitly
    #logrequest()
    return render_template(randomtemplate()), 200


#app.register_error_handler(404, page_not_found)

if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0",port="8000")
