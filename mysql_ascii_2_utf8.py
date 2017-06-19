#!/usr/bin/env python

import tempfile
import subprocess
import argparse
import sys

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True
        
def printNice(var=''):
    #print("print:")
    print(var)
    #print(":print")

#conversion class
class ascii2utf8():
    #initialisation object
    def __init__(self):
        self.tempDir = ""
        self.tempfile = ""
        self.parseFile1 = ""
        self.parseFile2 = ""
        self.rootReq = True
        #self.argParser = ""
        
        self.db_user_old = ""
        self.db_name_old = ""

        self.db_user_new = ""
        self.db_name_new = ""
        self.db_pw_new = ""
        
        self.args = ""
        self.file = False
        
        
        self.tempDir = tempfile.mkdtemp()
        self.tempfile = self.tempDir+'tmpfile'
        self.parseFile1 = self.tempDir+'parseFile1'
        self.parseFile2 = self.tempDir+'parseFile2'
        
        #Create / set Application parameters (arguments)
        self.argParser = argparse.ArgumentParser(description='Convert DB from ASCII to UTF8.')
        
        #create sub function (program <sub function> <arguments>
        subparsers = self.argParser.add_subparsers(help='HELP')
        
        #file sub function
        file_subparser = subparsers.add_parser('file', help='Convert/Parse File')
        file_subparser.add_argument('-inFile',required=True,help='In File')
        file_subparser.add_argument('-outFile',required=True,help='Out File')
        file_subparser.set_defaults(func=self.parseArgsFile)

        #sql Sub Function
        sql_subparser = subparsers.add_parser('mysql', help='Mysql:Dump/Parse/Create/Import')
        sql_subparser.set_defaults(func=self.parseArgsMysql)
        
        #sql Sub Function group for old db details
        old_group = sql_subparser.add_argument_group('Existing User','Existing MySQL User Details')
        old_group.add_argument('-old_db_user',required=True,help='The mysql User name of the existing user')
        old_group.add_argument('-old_db_name',help='The existing Mysql Database name',required=True)
        
        #sql Sub Function group for new db details
        new_group = sql_subparser.add_argument_group('New/Testing User','New MySQL User Details')
        new_group.add_argument('-new_db_user',help='The mysql User name of the "new/testing" user',required=True)
        new_group.add_argument('-new_db_pw',help='The "new/testing" user Password',required=True)
        new_group.add_argument('-new_db_name',help='The "new/testing" Mysql Database name',required=True)
        
        #sql Sub Function group for checking if 'old' user is able to create databases and users
        misc_group = sql_subparser.add_argument_group('Misc Options (Optional)')
        misc_group.add_argument('can_create',help='The existing Mysql user is able to create users/databases ')        
        
        
    #Destructor function
    def __del__(self):
        if self.isFile() == False:
            self.tempDir.cleanup()
        pass
    
    #dumps db to temp file
    def dumpDB(self):
        command = "mysqldump -u "+self.db_user_old+" -p --add-drop-table --skip-lock-tables --opt --quote-names --skip-set-charset --default-character-set=latin1 "+self.db_name_old+"  > "+self.tempfile
        subprocess.call(["mysql",command])
        pass
    
    #imports tmp file to new user/new database
    def importDB(self):
        command = "mysql -u "+self.db_user_new+" -p --default-character-set=utf8 "+self.db_name_new+" < "+self.parseFile1
        subprocess.call(["mysql",command])
        pass
    
    #creates a new db users and database
    def mkUser(self):
        command = "Create Database if not exists "+self.db_name_new+" ;GRANT ALL PRIVILEGES on "+self.db_name_new+".* to "+self.db_user_new+"@'localhost' identified by '"+self.db_pw_new+"';FLUSH PRIVILEGES"
        if self.rootReq:
            subprocess.call(["mysql -u root -p -e ",command ])
        else:
            subprocess.call(["mysql -u "+self.db_user_old+" -p -e ",command ])
        pass
    
    #converts the temp file from an ascii database to a utf8
    def parseDump(self):
        #parses one file and converts the following options and writes it to the other file.
        f1 = open(self.tempfile, 'r')
        f2 = open(self.parseFile1, 'w')
        for line in f1:
            f2.write(
                line.replace('MyISAM', 'InnoDB')
                .replace('varchar(8000)', 'varchar(4000)')
                .replace('latin1', 'utf8')
                     )
        f1.close()
        f2.close()
        
    #argument parser for Mysql arguments
    def parseArgsMysql(self,args):
        printNice("parseMysql")
        self.db_user_old = args.old_db_user
        self.db_name_old = args.old_db_name

        self.db_user_new = args.new_db_user
        self.db_name_new = args.new_db_name
        self.db_pw_new = args.new_db_pw
        
        if args.can_create:
            self.rootReq = False
            
    #argument parser for FILE arguments
    def parseArgsFile(self,args):
#        self.tempDir.cleanup()
        printNice("parseFile")
        self.file = True
        printNice(args.inFile)
        printNice(args.outFile)
        self.tempfile = args.inFile
        self.parseFile1 = args.outFile
        
    #argument parser, with error catching
    def parseArgs(self):
        self.args = self.argParser.parse_args()
        try:
            self.args.func(self.args)
        except AttributeError:
            self.argParser.print_help()
            exit()
    
    #checks if running file or mysql sub function
    def isFile(self):
        printNice("isFile")
        printNice(self.file)
        printNice("isFile")
        return self.file
    
    #main loop function
    def main(self):
        self.parseArgs()
        
        if self.isFile() == False:
            self.dumpDB()
        
        #run always
        self.parseDump()
        
        if self.isFile() == False:
            self.mkUser()
            self.importDB()
        
    
if __name__ == '__main__':    
    app = ascii2utf8()

    sys.exit(app.main())
