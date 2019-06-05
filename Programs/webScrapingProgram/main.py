import csulb_scraper
import datatransfer
import c

def main():

	#initial creation of courses.csv
	datatransfer.initcsvs()

	s2017 =  csulb_scraper.getCourses("CECS","Spring","2017")
	s2019 =  csulb_scraper.getCourses("CECS", "Spring", "2019")
	
	#prints the courses to show to the console that they exist
	#csulb_scraper.printCoursesInList(listOfCourses)

	datatransfer.export_courses(s2017)
	datatransfer.export_courses(s2019)

main()