#for verified
select n.email_id,cour.c_name,verified_marks,ssn_marks from nptel_marks n
join certificate cer on n.email_id = cer.email_id and n.c_code = cer.c_code
join course cour on cer.c_code = cour.c_code
where verified = 'ver';

#for not verified
select n.email_id,cour.c_name,verified_marks,ssn_marks from nptel_marks n
join certificate cer on n.email_id = cer.email_id
join course cour on cer.c_code = cour.c_code
where verified = 'nver';

#for rejected
select n.email_id,cour.c_name,verified_marks,ssn_marks from nptel_marks n
join certificate cer on n.email_id = cer.email_id and n.c_code = cer.c_code
join course cour on cer.c_code = cour.c_code
where verified = 'rej';