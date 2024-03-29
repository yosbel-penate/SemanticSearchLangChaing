import os
from flask import Blueprint
from flask import flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from src.logic.process_query_LLM import *
from src.model.JsonTools import write_json, read_json

#Global variables
UPLOAD_FOLDER = 'store'
ALLOWED_EXTENSIONS = {'pdf'}
TAGS_PROMPS_DB = 'promps.json'
query_answer_tuple_list = []
db=None

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            joinPath = build_file_path(filename)
            create_directory_if_it_doesnot_exist(joinPath)
            file.save(joinPath)
            return redirect(url_for('main.dir_listing'))
    return render_template('load_form_super.html')

@main_bp.route('/about')
def about_page():
    return render_template('about.html')


#File

@main_bp.route('/files', methods=['GET'])
def dir_listing():
    abs_path = os.path.join(UPLOAD_FOLDER, '')
    extension_file = ".pdf"
    pdf_files = get_files_in_subdir(abs_path, extension_file)
    return render_template('files.html', files = pdf_files)

@main_bp.route('/files/<string:name>')
def download_file(name):
    joinPath = build_file_path(name)
    path = os.path.join( '../', os.path.dirname(joinPath))
    return send_from_directory(path, name)

@main_bp.route('/process/<string:name>', methods=['GET', 'POST'])
def process_file(name):
    joinPath = build_file_path(name)
    process_query_LLM(joinPath)
    return redirect(url_for('main.upload_file'))

@main_bp.route('/consult/<string:name>', methods=['GET', 'POST'])
def consult_file(name):
    global db, query_answer_tuple_list
    db = build_the_database(name)
    query_answer_tuple_list = []
    return redirect(url_for('main.make_query_form'))

def build_the_database(name):
    joinPath = build_file_path(name)
    return consult_query_LLM(joinPath)

@main_bp.route('/delete/<string:name>', methods=['GET', 'POST'])
def delete_file(name):
    joinPath = build_file_path(name)
    remove_file_path(joinPath)
    return redirect(url_for('main.dir_listing'))

#Query process

@main_bp.route('/query_form')
def make_query_form():
    global db
    if not db:
        return
    return render_template('query.html')

@main_bp.route('/query/', methods=['GET', 'POST'])
def query():
    global db
    if not db:
        return
    if request.method == 'POST':
        query = request.form['query']
        answer = send_query_to_OpenAI(db, query)
    else:
        answer = 'no answer!!!'
    return process_answer(query, answer)

@main_bp.route("/redirect", methods=["POST"])
def redirect_to_new_page():
    return redirect(url_for("main.make_query_form"))

@main_bp.route("/multiple-docs-query", methods=['POST'])
def handle_data():
    global db
    my_json = request.get_json()
    files = my_json['files']
    # do something with the data...
    for file in files:
        temp_db = build_the_database(file)
        if not db:
            db =  temp_db
        else:
            db.merge_from(temp_db)
    return "Done!"

#Promps process
@main_bp.route('/newpromps/<string:promps>', methods=['POST'])
def new_promps_form(promps):
    return render_template('new_promps.html', promps = promps)

@main_bp.route('/save-promps', methods=['GET', 'POST'])
def save_promps():
    if request.method == 'POST':
        tags = request.form['tags']
        promps = request.form['promps']
        save_tags_and_promps_in_json(tags, promps)
    global query_answer_tuple_list
    return render_template('answer.html', query_answer_tuple_list = query_answer_tuple_list)


#Promps list page

@main_bp.route('/promps')
def promps_list():
    tags_promps_db = os.path.join(UPLOAD_FOLDER, TAGS_PROMPS_DB)
    data_list = read_json(tags_promps_db)
    tuple_list = [(d['tags'], d['promps']) for d in data_list]
    return render_template('promps_list.html', promps = tuple_list)

@main_bp.route('/promps/<string:query>', methods=['GET', 'POST'])
def promps_query(query):
    global db
    if not db:
        return
    answer = send_query_to_OpenAI(db, query)
    return process_answer(query, answer)

#Commond

def process_answer(query, answer):
    global query_answer_tuple_list
    query_answer_tuple_list.append((query, answer))
    return render_template('answer.html', query_answer_tuple_list = query_answer_tuple_list)

#Tools
def build_file_path(filename):
    return os.path.join(UPLOAD_FOLDER, cleanFilename(filename), filename)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Controlers

import shutil
def remove_file_path(path_file_name):
    if os.path.exists(path_file_name):
        shutil.rmtree(os.path.dirname(path_file_name))

def save_tags_and_promps_in_json(tags, promps):
    tags_promps_db = os.path.join(UPLOAD_FOLDER, TAGS_PROMPS_DB)
    data = read_json(tags_promps_db)
    new_item = {"tags": tags, "promps": promps}
    data.append(new_item)
    write_json(tags_promps_db, data)