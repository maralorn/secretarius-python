from flask import Flask, render_template, g, flash, url_for, redirect, request, abort, jsonify, send_from_directory
import os
from werkzeug import secure_filename
from controller import Controller

app = Flask(__name__)

SECRET_KEY = "idoodewaiNgah4hi"
UPLOAD_FOLDER = os.path.expanduser('~/files/')
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif','wav'])

app.config.from_object(__name__)



@app.before_request
def before():
    g.con = Controller()
    g.con._open()
@app.teardown_request
def after(response):
    g.con._close()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/inbox/')
def inbox():
    return render_template("inbox.html")

@app.route('/later/')
def later():
    return render_template("later.html")

@app.route('/asap/<name>')
def asap(name):
    return render_template("asap.html", name=name)

@app.route('/projects/')
def projects():
    return render_template("projects.html")



@app.route('/file/<id>/')
def file(id):
    try:
        return redirect(url_for('filen', id=id, name=g.con.get_filename(id)))
    except ValueError:
        abort(404)

@app.route('/file/<id>/<name>')
def filen(id, name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], str(id))



@app.route('/appointment/create/', methods=['POST'])
def appointment_create():
    id = g.con.create_appointment(request.form['description'], request.form['date'][:10].replace(".","/"), request.form.get('time',None)[11:], request.form.get('length',None), request.form.get('referencing',None))
    return jsonify(success=True, id=id)

@app.route('/asap/create/', methods=['POST'])
def asap_create():
    id = g.con.create_asap(request.form['description'], request.form['list'], request.form.get('referencing',None), request.form.get('project',None))
    return jsonify(success=True, id=id)

@app.route('/asap/changelist/<id>', methods=['POST'])
def asap_changelist(id):
    id = g.con.change_asaplist(id, request.form['list'])
    return jsonify(success=True)

@app.route('/asap/set/project/<id>', methods=['POST'])
def asap_set_project(id):
    id = g.con.asap_set_project(id, request.form.get("project",None))
    return jsonify(success=True)

@app.route('/asaplist/create/<name>')
def asaplist_create(name):
    g.con.create_asaplist(name)
    return jsonify(success=True)

@app.route('/asaplist/rename/<name>', methods=['POST','GET'])
def asaplist_rename(name):
    g.con.rename_asaplist(name, request.form['new_name'])
    return jsonify(success=True)

@app.route('/asaplist/delete/<name>', methods=['POST','GET'])
def asaplist_delete(name):
    g.con.asaplist_delete(name)
    return jsonify(success=True)

@app.route('/asaplist/get/names')
def asaplist_get_names():
    result = g.con.asaplist_get_names()
    return jsonify(names=map(lambda x: x["name"], result))

@app.route('/asaplist/get/<name>')
def asaplist_get(name):
    result = g.con.asaplist_get(name)
    return jsonify(name=name, result=result)

@app.route('/inbox/get/first/')
def inbox_get_first():
    ret = g.con.first_in_inbox()
    if ret:
        return jsonify(ret)
    else:
        return jsonify(error="Inbox is empty!")

@app.route('/info/get/<id>')
def info_get(id):
    return jsonify(g.con.get_information(id))

@app.route('/inbox/count')
def inbox_count():
    return jsonify(urgent=g.con.count_urgent(), inbox=g.con.count_inbox())

@app.route('/info/remove/reference/<id>', methods=['POST','GET'])
def info_remove_reference(id):
    g.con.info_remove_reference(id, request.form["referenceid"])
    return jsonify(success=True)

@app.route('/info/delete/<id>')
def info_delete(id):
    g.con.delete_info(id)
    return jsonify(success=True)

@app.route('/info/maybe/<id>')
def info_maybe(id):
    g.con.maybe_info(id)
    return jsonify(success=True)

@app.route('/info/archive/<id>')
def info_archive(id):
    g.con.archive_info(id)
    return jsonify(success=True)

@app.route('/info/delay/<id>', methods=['POST','GET'])
def info_delay(id):
    g.con.delay_info(id,request.form['until'].replace(".","/"))
    return jsonify(success=True)

@app.route('/later/get/list')
def later_get_list():
    return jsonify(later=g.con.later_get_list())

@app.route('/note/create/', methods=['POST'])
def note_create():
    attachment = request.files.get("attachment")
    fileid = None
    if attachment:
        filename = secure_filename(attachment.filename)
        fileid = g.con.new_file(filename)
        attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], str(fileid)))
    id = g.con.new_note(request.form["content"], fileid)
    return redirect(url_for('index'))

@app.route('/note/delete/attachment/<id>')
def note_delete_attachment(id):
    g.con.note_delete_attachment(id)
    return jsonify(success=True)

@app.route('/note/change/<id>', methods=['POST'])
def note_change(id):
    g.con.change_note(id, request.form['content'])
    return jsonify(success=True)

@app.route('/project/create/', methods=['POST'])
def project_create():
    id = g.con.create_project(request.form.get('description',""), request.form.get('referencing', None), request.form.get('parent', None))
    return jsonify(success=True,id=id)

@app.route('/project/set/parent/<id>', methods=['POST'])
def project_set_parent(id):
    id = g.con.project_set_parent(id, request.form.get("parent",None))
    return jsonify(success=True)

@app.route('/project/get/tree/')
def project_get_tree():
    projects = g.con.project_get_all()
    projectdict = {}
    root = []
    for project in projects:
        projectdict[project['id']] = project
        project['children'] = []
    for project in projects:
        try:
            projectdict[project['parent']]['children'].append(project)
        except:
            root.append(project)
        del project['parent']
    for asap in g.con.asap_get_all():
        try:
            projectdict[asap['project']]['children'].append(asap)
        except:
            root.append(asap)
        del asap['project']
        del asap['projectdescription']
    return jsonify(root=root)

@app.route('/task/done/<id>')
def task_done(id):
    g.con.task_done(id)
    return jsonify(success=True)
