
from flask import Flask, request
from flask_json import FlaskJSON,JsonError, json_response, as_json
import operationHandler as oph
from flask_cors import CORS, cross_origin

app = Flask(__name__)
json = FlaskJSON(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'


@app.route('/')
def index():
    return json_response(msg = "test correct form the new version")

@app.route('/save-file',methods = ['POST'])
def save_file():
    
    '''
    accepts form data
    path does not matter
    {
    root: test,
    path: '/',
    content: 'rohit is the hero',
    filename: 'text.txt'
    }
    '''
    root = request.form.get('root')
    path = request.form.get('path')
    content = request.form.get('content')
    filename = request.form.get('filename')
    # root, path,content,filename
    msg = oph.save_file(root=root, path=path,content=content,filename=filename)
    if msg == 0:
        return json_response(msg = "successful")
    else:
        return json_response(msg = "error")

@app.route('/save-commit',methods = ['POST'])
def save_commit():
    '''
    accepts json data
    {
        branch: branch_name,
        root: "root name",
        commit_msg: "first commit"
        files: [{
                    filename: "test.txt",
                    content:"test"
                },
                {
                    filename: "test.txt",
                    content:"test"
                }]
    }
    '''
    payload = request.json
    print(payload)

    msg,code = oph.save_commit(payload = payload)
    
    return json_response(msg = msg, error=code)


@app.route('/pull-server',methods = ['POST'])
def pull_server():
    '''
    accepts form data
    {
    root: test,
    project_name: test_project,
    branch: username
    }
    '''
    #root,project_name,branch
    root = request.form.get('root')
    project_name = request.form.get('project_name')
    branch = request.form.get('branch')
    print("app.py", root,branch,project_name)
    hiry = oph.pull_editor(root = root, project_name= project_name,branch=branch)
    return json_response(files = hiry)

@app.route('/get-file',methods = ['POST'])
def get_file():
    '''
    accepts form data
    {
    root: test,
    path: '/',
    filename: 'test.txt'
    }
    '''
    #root,path,filename
    root = request.form.get("root")
    path = request.form.get("path")
    filename = request.form.get("filename")
    content = oph.get_file(root=root, path=path, filename = filename)
    #print(content)
    return json_response(content = content)

@app.route('/hir',methods=['POST'])
def get_hir():
    '''
    accepts form data
    {
        root:test
    }
    '''
    root = request.form.get("root")
    resp = oph.get_hir(root)
    return json_response(hir=resp)

@app.route('/delete-dir',methods = ['POST'])
def del_dir():
    '''
    accepts form data
    path does not matter
    {
    root: test,
    path: '/',
    dirname: 'test1'
    }
    '''
    #root,path,new_dir
    root = request.form.get("root")
    path = request.form.get("path")
    dirname = request.form.get("dirname")
    hir,error = oph.delete_dir(root = root, path=path, dirname = dirname)
    return json_response(hir = hir,error=error)

@app.route('/delete-file',methods = ['POST'])
def del_file():
    '''
    accepts form data
    path does not matter
    {
    root: test,
    path: '/',
    filename: 'test1.php'
    }
    '''
    #root,path,new_dir
    root = request.form.get("root")
    path = request.form.get("path")
    filename = request.form.get("filename")
    hir,error = oph.delete_file(root = root, path=path, filename = filename)
    return json_response(hir = hir,error=error)


@app.route('/make-dir',methods = ['POST'])
def make_dir():
    '''
    accepts form data
    path does not matter
    {
    root: test,
    path: '/',
    dirname: 'test1'
    }
    '''
    #root,path,new_dir
    root = request.form.get("root")
    path = request.form.get("path")
    new_dir = request.form.get("dirname")
    hir,error = oph.make_dir(root = root, path=path, dir_name = new_dir)
    return json_response(hir= hir,error = error)


@app.route('/make-file',methods = ['POST'])
def make_file():
    '''
    accepts form data
    path matters
    {
    root: test,
    path: '/test1',
    filename: 'test1.txt'
    }
    '''
    #root,path,filename
    root = request.form.get("root")
    path = request.form.get("path")
    filename = request.form.get("filename")
    file_hir,error = oph.make_file(root = root, path=path, filename = filename)
    return json_response(hir = file_hir,error= error)

@app.route('/make-repo',methods = ['POST'])
def make_repo():
    '''
    accepts json data
    {
    projectname: 'test_project',
    users = ["b1","b2","b3"]
    }
    '''
    payload = request.json
    msg = oph.make_repo(payload = payload)
    return json_response(msg = msg)

@app.route('/push-repo',methods = ['POST'])
def push_repo():
    '''
    {
        root: test,
        branch: b1
    }
    '''
    root = request.form.get("root")
    branch = request.form.get("branch")
    msg , code = oph.push_code(branch=branch, root=root)
    return json_response(msg = msg, error= code)
@app.route('/add-users',methods = ['POST'])
def add_user():
    '''
    accepts json data
    {
        projectname : projectname,
        base_branch : base_branch,
        new_branchs : ['b1',b2,b3]
    }
    '''
    payload = request.json
    return oph.add_user(payload=payload)

@app.route('/delete-working-dir',methods=['POST'])
def deleteWorkingDir():
    root = request.form.get("root")
    return oph.delete_working_dir(root = root)


if __name__ =="__main__":
   app.run(host="0.0.0.0",port=8800)
