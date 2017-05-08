
# mysql_ascii_2_utf8 Converter

To convert a MySQL ASCII database to a MySQL UTF8 database

---

### Installing
Clone the repo with the below
`git clone https://bitbucket.org/justin531/mysql_ascii_2_utf8.git`

---

### Usage

`mysql_ascii_2_utf8 <file/mysql>`

    * file        Convert/Parse File                                                                                                                                                                                                                                             
    * mysql       Mysql:Dump/Parse/Create/Import


#### file:

    * -inFile INFILE    In File
    * -outFile OUTFILE  Out File

#### mysql:

Existing User:

  Existing MySQL User Details

    * -old_db_user OLD_DB_USER
                        The mysql User name of the existing user
    * -old_db_name OLD_DB_NAME
                        The existing Mysql Database name

New/Testing User:

  New MySQL User Details

    * -new_db_user NEW_DB_USER
                        The mysql User name of the "new/testing" user
    * -new_db_pw NEW_DB_PW  The "new/testing" user Password
    * -new_db_name NEW_DB_NAME
                        The "new/testing" Mysql Database name

Misc Options (Optional):

    * can_create            The existing Mysql user is able to create
                        users/databases


---

### Issues
Please Submit all issues to [Bitbucket.org](https://bitbucket.org/justin531/mysql_ascii_2_utf8/issues/new)

---

### TODO 
 * GUI?
 * Better documentation
