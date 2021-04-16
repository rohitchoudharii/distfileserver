import subprocess
from time import sleep

class GHandler():
    server = "/home/ubuntu/nfsfiles/git"
    cwd = ""
    def __init__(self,cwd):
        self.cwd = cwd
    def git_add(self,files = None):
        self.execute(command = "git add .",output = "")
    def git_commit(self,msg):
        return  self.execute(command = 'git commit -m "{ms}"'.format(ms=msg), output = "nothing to commit")
    def git_push(self,branch):
        return self.execute('git push origin {brch}'.format(brch=branch), output = "")
    def git_clone(self,server,project_name,branch):
        self.cmd.append('git clone -b {brch} {server}:{project}.git'.format(brch=branch,server=server,project=project_name))
    def git_init(self):
        return  self.execute(command = "git init",output = "Reinitialized")
    def git_remote_add(self,project_name):
        return self.execute("git remote add origin {server}/{project}.git".format(server=self.server, project=project_name) ,output = "")
        #return self.execute("git remote add origin {server}:{project}.git".format(server=self.server, project=project_name) ,output = "")
        
    def git_pull_server(self, branch):
        return self.execute(command = "git pull origin {branch}".format(branch=branch),output="")
    def git_add_user(self,branch):
        return self.execute(command = "git branch {branch}".format(branch=branch))

    def execute(self,command,output=None):
        #print(self.cwd)
        ps = subprocess.run(args = command, capture_output = True, text=True,shell = True,cwd=self.cwd)
        #print(ps.stdout)
        #print(ps.stderr)
        print(ps) 
        if output == None:
            return 
        if output in ps.stdout or ps.returncode != 0 :
            if ps.stderr == "":
                return (ps.stdout,True)
            else:
                return (ps.stderr,True)
        else:
            return (ps.stdout,False)
    # def execute2(self,command1,cwd,input1 = None,output=None):
    #     print(command1)
    #     ps = subprocess.run(args = ["start-ssh-agent.cmd",command1],text=True,shell = True,cwd=cwd)
    #     print("done ssh")
    #     #pp = ps.communicate(command1)
    #     print(ps.stdout)
    #     print(ps.stderr)
    #     print(ps)
    #     if output == None:
    #         return 
    #     if output in ps.stdout or ps.returncode != 0 :
    #         if ps.stderr == "":
    #             return ("somthing went wrong",True)
    #         else:
    #             return (ps.stdout,True)
    #     else:
    #         return (ps.stdout,False)
if __name__ =="__main__":
    gh = GHandler("/home/rohit/php/test4")
    gh.git_init()
    gh.git_remote_add("test2")
    gh.git_pull_server(branch="b1")
