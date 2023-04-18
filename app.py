import os
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from src.logic.process_query_LLM import *

UPLOAD_FOLDER = 'store'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            joinPath = build_file_path(filename)
            create_directory_if_it_doesnot_exist(joinPath)
            file.save(joinPath)
            return redirect(url_for('download_file', name = filename))
    return render_template('load_form.html')

@app.route('/files')
def dir_listing():
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], '')
    extension_file = ".pdf"
    pdf_files = get_files_in_subdir(abs_path, extension_file)
    return render_template('files.html', files = pdf_files)

@app.route('/files/<string:name>')
def download_file(name):
    joinPath = build_file_path(name)
    return send_from_directory(os.path.dirname(joinPath), name)

def build_file_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], cleanFilename(filename), filename)

@app.route('/process/<string:name>', methods=['GET', 'POST'])
def process_file(name):
    joinPath = build_file_path(name)
    process_query_LLM(joinPath)
    return redirect(url_for('upload_file'))

db=None
@app.route('/consult/<string:name>', methods=['GET', 'POST'])
def consult_file(name):
    global db
    if not db:
        joinPath = build_file_path(name)
        db = consult_query_LLM(joinPath)
    return redirect(url_for('make_query_form'))

@app.route('/query/', methods=['GET', 'POST'])
def query():
    global db
    if not db:
        return
    if request.method == 'POST':
        query = request.form['query']
        docs = db.similarity_search(query)
        answer = docs[0].page_content
    else:
        answer = 'no answer!!!'
    return render_template('answer.html', answer = answer, query = query)

@app.route('/query_form')
def make_query_form():
    global db
    if not db:
        return
    return render_template('query.html')