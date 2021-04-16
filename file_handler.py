import os
import shutil
import subprocess
import pprint

class FHandler():
    base = "/home/rohit/nfsfiles/php"
    folder_path = ""
    root=""
    hierarchy = {}
    dir_name = ""
    
    hir_ar = []
    def __init__(self,dir_name,make_dir=False):
        self.folder_path = "/home/ubuntu/nfsfiles/php"
        self.hierarchy = {"files":[]}
        self.hir_ar=[]
        # print(self.hierarchy)
        self.root=dir_name
        self.dir_name = dir_name  
        if make_dir:
            a =  self.make_dir(dirname = dir_name,create_file=False)

        for d in dir_name.split("/"):
            self.folder_path = os.path.join(self.base,d)

    def set_default_path(self):
        '''
        This function is to set the dir to default
        '''
        os.chdir(self.folder_path)

    def change_dir(self,dir_name):
        '''
        This function is to change directory
        '''
        p = self.folder_path
        for d in dir_name.split("/"):
            p = os.path.join(p,d)
        os.chdir(p)

    def current_dir(self):
        '''
        This will retun the current directory
        '''
        return self.folder_path

    def make_dir(self,dirname,path="/",create_file=True):
        '''
        This function will create directory
        '''
        
        file_path = self.folder_path
        for p in path.split("/"):
            file_path = os.path.join(file_path,p)
        try:
            file_path = os.path.join(file_path,dirname)
            os.mkdir(file_path)
            if(create_file):
                file_path = os.path.join(file_path,"readme.txt")
                with open(file_path,"w") as f1:
                    f1.write("\n")
            return 1
        except:
            return 0
        


    def make_file(self,fname,path="/"):
        '''
        This will create files
        '''
        file_path = self.folder_path
        for p in path.split("/"):
            file_path =os.path.join(file_path,p)
        file_path =os.path.join(file_path,fname)
        print(file_path)
        #if os.path
        try:
            f = open(file_path,"x")
            f.close()
            with open(file_path,"w") as f1:
                f1.write("#write your code here")
            return 1
        except FileExistsError:
            return 0
    def delete_dir(self,dirname):
        p = self.folder_path
        print(dirname)
        for i in dirname.split("/"):
            p = os.path.join(p,i)
        
        shutil.rmtree(p)
    def delete_file(self,filename):
        p = self.folder_path
        for i in filename.split("/"):
            p = os.path.join(p,i)
        os.remove(p)
    def delete_folder_final(self):
        '''
        This will be used to delete the file
        '''
        shutil.rmtree(self.folder_path)

    def save_file(self,content,file_name,path='/'):
        '''
        This will be used to save the file to the current directory
        '''
        p=self.folder_path
        for i in path.split("/") :
            p = os.path.join(p,i)
        print(p)
        p = os.path.join(p, file_name)
        print(p)
        try: 
            if not os.path.isfile(p):
                return 1
            with open(p,"wb") as f:
                f.write(content)
            return 0
        except:
            print("Something went wrong")
            return 1
    def recursive_copy(self,src,path='/'):
        for item in os.listdir(src):
            if item[0] ==".":
                continue
            file_path = os.path.join(src, item)
            if os.path.isfile(file_path):
                file = { "path": path,	"filename": item }
                self.hir_ar.append(file)
            elif os.path.isdir(file_path):
                item+="/"
                self.recursive_copy(file_path,path+item)

    def helper(self,hr,fol):
        if fol[0] in hr:
            if len(fol) == 0:
                return hr
            else:
                self.helper(hr[fol[0]],fol[1:])
        else:
            hr[fol[0]] = {"files":[]}
            if len(fol)-1 == 0:
                return hr
            else:
                self.helper(hr[fol[0]],fol[1:])

    def sorter_hir(self,lis):
        hr = {"files":[]}
        se = set()
        for i in lis:
            a = i['path']
            se.add(a)
        
        folders = sorted(se)
        r = []
        for j in folders:
            a = j.split("/")
            while "" in a:
                a.remove("")
            if len(a) == 0:
                continue
            self.helper(hr,a)
        pp = pprint.PrettyPrinter(indent=2)
        #print(hr)
        #pp.pprint(hr)
        #print(lis)
        for i in lis:
            a = i['path'].split("/")
            while "" in a:
                a.remove("")
            if len(a) == 0:
                hr["files"].append(i["filename"])
            else:
                temp = hr

                for fol in a:
                    temp = temp[fol]
                temp["files"].append(i["filename"])
        #pp.pprint(hr)

        return hr

    def get_hierarchy(self):
        
        path = self.folder_path
        self.recursive_copy(path)
        return self.sorter_hir(lis = self.hir_ar)


    def get_file_content(self,filename,path="/"):
        
        p = self.folder_path
        for d in path.split("/"):
            p = os.path.join(p,d)
        content = ""
        final_p=os.path.join(p,filename)
        try:
            with open(final_p) as f:
                content = f.read()
        except FileExistsError:
            print("File does not exist")
        return content

    def setup_default_hierarchy(self):
        content = """
        <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Hello World</title>
            </head>
            <body>
                    Happy Coding
            </body>
        </html>
        """
        p = self.folder_path
        try:
            self.make_dir(dirname = "css",create_file=True)
            self.make_dir(dirname = "js",create_file=True)
            self.make_file(fname="index.php")
            self.save_file(content = bytes(content,'utf-8'),file_name="index.php")
        except:
            return 0
        return 1


if __name__ == "__main__":
    fh = FHandler(dir_name="test")
    print(fh.get_file_content(filename = "test1/testapi1/readme.txt"))