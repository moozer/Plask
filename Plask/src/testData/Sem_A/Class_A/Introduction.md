Author: Some Author
Email: my@email.com
startweek: 34
endweek: 4

This is the *Introduction.md* file.

It should contain general description of the semester.

Meta data is required:

* Author: the name of the author
* Email: the email address
* startweek: the first week number of the semester
* endweek: the last week number of the semester

Optional metadata (for all section):

* status: writes the status text in *italics*. Used for stuff like "TBD", "Draft" or "review the part about ...". A magic value is "exclude", which will hide the section.

A note on SemesterSchedule.csv

* Internal structure is
	
	* Course: the course name
	* Teacher: the teachers initials
	* ECTS: a float value of the ECTS size of the course
	* Weeks: the weeks where the course is running (with the same number of lessons). Support dash and comma, ie. 4-7,9 for weeks 4,5,6,7 and 9	
	* Lessons: the number of lessons in the week(s) specified in the "weeks" column
	* Link: The link to the course plan. 
		
		* "." is the default internal Plask reference
		* "noplan" means it should appear in the course list, but no plan is supplies
		* "exclude" course should not appear as a separate course (but will appear in the schedule)
		* other values is used as URL.
		
	
