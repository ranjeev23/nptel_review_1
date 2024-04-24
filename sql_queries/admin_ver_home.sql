select s.dig_id,s.st_name,s.sem, s.acc_year,cour.c_name,cert.c_code,s.acc_year from student s
join certificate cert on cert.email_id = s.email_id
join course cour on cert.c_code = cour.c_code;