select majorname, count(student.majorid) 'count'
from major
       left join student on student.majorid = major.majorid group by major.majorid