SELECT COUNT(*) FROM temp_fostaging;
SELECT COUNT(*) FROM fostaging;
SELECT COUNT(*) FROM itable;

create table itable (iitable
 BIGINT);

drop procedure if exists ROWPERROW;

delimiter ;;
CREATE PROCEDURE ROWPERROW()
BEGIN
DECLARE n BIGINT DEFAULT 0;
DECLARE i BIGINT DEFAULT 0;
SELECT COUNT(*) FROM fostaging INTO n;
#set n = 20000000;
SET i=0;
	WHILE i<n DO 
        set autocommit = 0;
		set unique_checks = 0;
		INSERT IGNORE INTO temp_fostaging SELECT * FROM fostaging LIMIT 10000000,i;
        #SELECT COUNT(*) FROM temp_fostaging;
		set unique_checks = 1;
		commit;        
		#INSERT IGNORE INTO temp_fostaging SELECT * FROM fostaging LIMIT 1000000,i;
        SET i = i + 10000000;
        insert into itable select i;
        commit;
		
        #SELECT COUNT(*) FROM temp_fostaging;
		END WHILE;
	 set autocommit = 1;
	End;
;;
delimiter = ; 

CALL ROWPERROW();

SELECT COUNT(*) FROM temp_fostaging;


SELECT CEILING(Total_InnoDB_Bytes*1.6/POWER(1024,3)) RIBPS FROM
(SELECT SUM(data_length+index_length) Total_InnoDB_Bytes
FROM information_schema.tables WHERE engine='InnoDB') A;





        
        
  
        