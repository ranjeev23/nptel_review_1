#get the registernumber, coursecode,coursename,certifcatemarks
select s.regno,cour.c_code,cour.c_name,cert.marks
from student s
join certificate cert on cert.email_id=s.email_id
join course cour on cert.c_code=cour.c_code;

#when the correct button is pressed
insert into nptel_marks values ('email','c_code',10,11);
update certificate set verified = 'ver' where email_id = 'std_email_id' and c_code = 'course_code';

#when wrong button is pressed 
insert into rejected values('std_email_id','c_code','teacher_email_id','issue');
update certificate set verified = 'rej' where email_id = 'std_email_id' and c_code = 'course_code';

#when scan qr code button is pressed
select qr_code_url from certificate where email_id = 'email_id_std' and c_code = 'course_code';

#load an image