### To Run this Manually run the following commands:


#### BASH:
Dump Database:
 * `mysqldump -u{{USER}}  -p --add-drop-table --skip-lock-tables --opt --quote-names --skip-set-charset 
--default-character-set=latin1 {{Database Name}}  > {{Tmp File}}`

Parse Database:
 * `sed  -i 's|MyISAM|InnoDB|g' {{Tmp File}}`
 * `sed  -i 's|varchar(8000)|varchar(4000)|g' {{Tmp File}}
 * `sed  -i 's|latin1|utf8|g' {{Tmp File}}

Import Database:
 * `mysql -u {{USER}} -p --default-character-set=utf8 {{Database Name}} < {{Tmp File}}`


#### Powershell:
Dump Database:
 * `mysqldump -u{{USER}}  -p --add-drop-table --skip-lock-tables --opt --quote-names --skip-set-charset 
--default-character-set=latin1 {{Database Name}}  > {{Tmp File}}`

Parse Database:
 * `cat {{Tmp File}} | % { $_ -replace "MyISAM","InnoDB" } > {{TMP 2}}`
 * `cat {{TMP 2}} | % { $_ -replace "varchar(8000)","varchar(4000)" } > {{TMP 3}}`
 * `cat {{TMP 3}} | % { $_ -replace "latin1","utf8" } > {{TMP 4}}`

Import Database:
 * `mysql -u {{USER}} -p --default-character-set=utf8 {{Database Name}} < {{Tmp 4}}`


