
from file_handler import FHandler
from git_handler import GHandler
#from paramiko import SSHClient
import subprocess
import time
import json
import os

def delete_working_dir(root):
    fh = FHandler(dir_name = root)
    fh.delete_folder_final()
    if os.path.isdir(fh.current_dir()):
        del fh
        return "error deleting"

    else:
        del fh
        return "folder deleted"


def push_code(root,branch):
    fh = FHandler(dir_name = root)
    gh = GHandler(fh.current_dir())
    msg,code = gh.git_push(branch=branch)
    if "fatal" in msg:
        return "Error saving your file to the server",1
    return "successfull saving all the files , now you can leave the editor",code


def commit(msg,branch,root):
    fh = FHandler(dir_name = root)
    #fh.set_default_path()
    gh = GHandler(cwd = fh.current_dir())
    gh.git_add()
    res , flag = gh.git_commit(msg)
    #gh.git_push(branch)
    if flag:
        if "nothing to commit" in res:
            return "nothing to commit"
        else:
            return "error"
    else:

        return "All good"

def pull_editor(root,project_name,branch):
    '''
    Pull the data to php folder
    send the directory structure to the user
    '''
    print(branch,project_name)
    #Set the path and make the directory
    fh = FHandler(root,make_dir=True)
    print(fh.current_dir())
    gh = GHandler(cwd = fh.current_dir())
    #perform gti fetch
    gh.git_init()
    gh.git_remote_add(project_name = project_name)
    #gh.add_ssh()
    print(fh.current_dir())
    gh.git_pull_server(branch = branch)
    #msg, flag = gh.execute()
    del gh
    del fh
    #Fetch the file structure
    fh  = FHandler(root)

    hierarchy = fh.get_hierarchy()
    return hierarchy

def save_commit(payload):
    '''
    {
        branch: branch_name,
        root: "root name",
        commit_msg: "first commit",
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
    #payload = json.loads(payload1)
    branch = payload["branch"]
    commit_msg = payload["commit_msg"]
    root = payload["root"]
    files = payload["files"]
    #Saving all the files
    for file in files:
        #path = file['path']
        path = "/"
        filename = file["filename"]
        content = file["content"]
        res = save_file(root=root,path = path,content = content, filename = filename)
        if res == 1:
            return "error saving"

    # commiting the code
    commit_res = commit(msg = commit_msg, branch = branch,root = root)
    if commit_res == "error":
        return "error commiting",1
    if commit_res == "nothing to commit":
        return "nothing to commit",1
    return "done",0


def save_file(root, path,content,filename):
    fh = FHandler(root)
    print(fh.current_dir())
    #fh.set_default_path()
    msg = fh.save_file(content = bytes(content,'utf-8'), file_name = filename,path = "/")
    return msg

def get_file(root,path,filename):
    fh = FHandler(root)
    print(fh.current_dir())
    # if path!="/":
    #     fh.change_dir(path)
    #     print(fh.current_dir())
    content = fh.get_file_content(filename=filename,path="/")
    return content

def make_dir(root,path,dir_name):
    fh = FHandler(root)
    # if path != '/':
    #     fh.change_dir(path)
    # print(fh.current_dir())
    if fh.make_dir(dir_name) == 1:
        return fh.get_hierarchy(),0
    else:
        return 0,1

def make_file(root,path,filename):
    fh = FHandler(root)
    if fh.make_file(fname = filename,path=path) == 1:
        return fh.get_hierarchy(),0
    else:
        return 0,1


def make_repo(payload):
    # send request to the git server using API
    projectname = payload["projectname"] #project name in string
    users = payload["users"]  #users in the form of array
    users.append("dev")
    if not os.path.isdir("/home/ubuntu/nfsfiles/git/"+projectname+".git"):
        ps = subprocess.run(args = "git init --bare {projectname}.git".format(projectname = projectname), capture_output=True,shell=True,text=True,cwd="/home/ubuntu/nfsfiles/git")
        print(ps)
        fh = FHandler("temp_"+projectname, make_dir=True)
        print("from the function: "+fh.current_dir())
        gh = GHandler(fh.current_dir())
        print(fh.setup_default_hierarchy())
        # exit()
        gh.git_init()
        gh.git_remote_add(project_name=projectname)
        gh.git_add()
        gh.git_commit(msg="Initial Build-up")
        for u in users:
            gh.git_add_user(branch = u)
        gh.git_push(branch = "master "+ " ".join(users))

        fh.delete_folder_final()
        return ("successfull", 0)
    else:
        return ("project already exist!",1)
    
    

def delete_dir(root,path,dirname):
    fh = FHandler(root)
    error = fh.delete_dir(dirname = dirname)
    return fh.get_hierarchy(),error


def delete_file(root,path,filename):
    fh = FHandler(root)
    error = fh.delete_file(filename = filename)
    return fh.get_hierarchy(),error

def get_hir(root):
    fh = FHandler(dir_name=root)
    return fh.get_hierarchy()
def add_user(payload):
    try:
        projectname = payload['projectname']
        b_branch = payload['base_branch']
        new_branches = ['new_branchs']
        fh = FHandler("branch_"+projectname, make_dir=True)
        gh = GHandler(fh.current_dir())
        gh.git_init()
        gh.git_remote_add(project_name=projectname)
        gh.git_pull_server(branch = b_branch)
        for n in new_branches:
            gh.git_add_user(n)
        gh.git_push(branch = " ".join(users))
        fh.delete_folder_final()
    except Exception as e:
        return str(e)
    return "Done"




def tester(root):
    t = time.time()
    payload = {
        "projectname":"first_test",
        "users":["b1","b2","b3","b4","b5"]
    }
    make_repo(payload=payload)
    print(time.time() - t)

if __name__ == "__main__":
    # hir = pull_editor(str(time.time()),"project","master")
    # for files in hir:
    #     print(files)
    #ommit(msg,branch,parent_path)
    #print(save_file(content = "Test file",root="dist", path='/',filename="test.txt"))
    print(tester(root="test1"))
