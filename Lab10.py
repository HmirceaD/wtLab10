import os
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
import werkzeug

UPLOAD_FOLDER = "E:\Programare\School\Web-Technologies\Lab10\\uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

upload_path = "E:\Programare\School\Web-Technologies\Lab10\\uploads"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uploader", methods=['POST',])
def uploader():
    if request.method == 'POST':

        f = request.files['file[]']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        return redirect('/')

@app.route('/download/<file>')
def download(file):

    for (dirpath, dirnames, filenames) in os.walk(upload_path):

        for f in filenames:
            if f == file:
                return send_from_directory(directory=dirpath, filename=f)

    return redirect("/")
@app.route("/remove/<file>")
def remove_route(file):

    for (dirpath, dirnames, filenames) in os.walk(upload_path):

        for f in filenames:

            if f == file:
                os.remove(dirpath + "\\" + f)

    return redirect('/')

@app.route('/<dir>')
def dir_routes(dir):

    html = ""
    print(dir)
    for file in os.listdir(upload_path + '\\' + dir):

        html += "<br>{}".format(file)

    return html

@app.route('/', methods = ['GET', 'POST'])
def index_route():

    if request.method == "GET":

        html = ""

        for (dirpath, dirnames, filenames) in os.walk(upload_path):

            dir_name = dirpath.replace(upload_path, "")
            html += '<br><a href = "{}">'.format(dir_name) + dir_name + "</a>"

            for file in filenames:

                html += "<br>{}".format(file)
            html += "<hr>"
        return html

@app.route('/upload')
def upload_route():
    return render_template("upload.html")


if __name__ == '__main__':
    app.run()
