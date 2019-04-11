'''
List of functions:
	main:
		runs whatever you currently want the program to run
	getCourses:
		webscrapes the course catalog, returns a list of course objects with all the data filled out







'''




def main():
	listOfCourses =  getCourses()
	
	
	printCoursesInList(listOfCourses)






def getCourses():
	import c
	from urllib.request import urlopen as uReq
	from bs4 import BeautifulSoup as soup


	#saves the CECS department's shedule into a variable
	class_url = 'http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2017/By_Subject/CECS.html#note1'



	#opening up connection, grabbing the HTML
	uClient = uReq(class_url)
	page_html = uClient.read()
	uClient.close()

	#turning the page html into a soup that I can manipulate
	page_soup = soup(page_html, "html.parser")


	#declares the list of courses
	listOfCourses = []

	# tempCBL = a list that has every course block from the page
	tempCBL = page_soup.findAll("div", {"class" : "courseBlock"})


	for courseBlk in tempCBL:

		#This gets all the data I want to store later and puts it into a 
		courseName = (courseBlk.find("span", {"class" : "courseTitle"})).text.strip()
		courseCode = (courseBlk.find("span", {"class" : "courseCode"})).text.strip()
		units = (courseBlk.find("span", {"class" : "units"})).text.strip()


		listOfGroups = getGroups(courseBlk)


		#constructs a temporary course obejct that is the current course we just grabbed saved as an object



		#TO DO: add "listOfGroups" to constructor
		tempCourse = c.course(courseName,courseCode,units)
		listOfCourses.append(tempCourse)



	return listOfCourses



























def getGroups(courseBlk):
	import c


	#declares the list of groups that gets returned later on

	listOfGroups = []
	
	# declares isLAB
	isLAB = False


	# this goes through every class that does not have groups, and if it does have a lab, then it gets flagged by making isLAB false
	if (courseBlk.find("div", {"class" : "groupMessage"}) == None):
		

		table = courseBlk.findAll("td")


		for td in table:
			td = td.text.strip()
			if (td == "LAB"):
				isLAB = True

		

	# This set of if else statements runs the following:
	# 		1) If it has no group messages and there is no labs, then it is only seminars
	# 		2) If it has no group messages and there is labs, there is just 1 section of the class
	# 		3) If neither are true, then it must have a group message. So, that menas that there are multiple groups



	if (courseBlk.find("div", {"class" : "groupMessage"}) == None and isLAB == False):
		#print("The course " + (courseBlk.find("span", {"class" : "courseTitle"})).text.strip() + " (" + (courseBlk.find("span", {"class" : "courseCode"})).text.strip() +") does NOT have GROUPS and does NOT have LABS")

		# TO DO: make every row in a section table become an element in an array, and skip over the first element
		#			for each line where you are going to add in the seminar, for each element in the list, delcare a temporary group
		#			and then add that to the list of groups to be returned

		table = courseBlk.findAll("tr")


		# This for loop iteratively goes through each row in the table (that isnt the header) and then assigns that row to the the 'row' variable.
		# It then cooresponds the correct td to each of the values in a temp group object
		for i in range(0,len(table)-1):
			row = table[i+1]

			row = row.findAll("td")
	

			# After we get each row, we get the data we need for the group
			SemClassNumber = row[0].text.strip()
			SemType = row[2].text.strip()
			SemDays = row[3].text.strip()

			# TO DO: write in an algorithm to find the start and end times.

			SemStartTime = row[4].text.strip()
			SemEndTime = row[4].text.strip()
			SemLocation = row[6].text.strip()
			SemInstructor = row[7].text.strip()

			tempGroup = c.group(SemClassNumber, SemType, SemDays, SemStartTime, SemEndTime, SemLocation, SemInstructor)


			# tempGroup is added to lisfOfGroups
			listOfGroups.append(tempGroup)



	elif (isLAB == True):
		#print("The course " + (courseBlk.find("span", {"class" : "courseTitle"})).text.strip() + " (" + (courseBlk.find("span", {"class" : "courseCode"})).text.strip() + ") does NOT have GROUPS but HAS LABS")

		# This gets both rows that are on the website, and saves them as semRow and labRow

		table = courseBlk.findAll("tr")

		semRow = table[1].findAll("td")
		labRow = table[2].findAll("td")




		# we now get the data needed for tempGroup

		SemClassNumber = semRow[0].text.strip()
		SemType = semRow[2].text.strip()
		SemDays = semRow[3].text.strip()

		# TO DO: write in an algorithm to find the start and end times.

		SemStartTime = semRow[4].text.strip()
		SemEndTime = semRow[4].text.strip()
		SemLocation = semRow[6].text.strip()
		SemInstructor = semRow[7].text.strip()


		LabClassNumber = labRow[0].text.strip()
		LabType = labRow[2].text.strip()
		LabDays = labRow[3].text.strip()

		# TO DO: write in an algorithm to find the start and end times.

		LabStartTime = labRow[4].text.strip()
		LabEndTime = labRow[4].text.strip()
		LabLocation = labRow[6].text.strip()
		LabInstructor = labRow[7].text.strip()

		tempGroup = c.group(SemClassNumber, SemType, SemDays, SemStartTime, SemEndTime, SemLocation, SemInstructor, LabClassNumber, LabType, LabDays, LabStartTime, LabEndTime, LabLocation, LabInstructor)

		listOfGroups.append(tempGroup)

	else:
		#print("The course " + (courseBlk.find("span", {"class" : "courseTitle"})).text.strip() + " (" + (courseBlk.find("span", {"class" : "courseCode"})).text.strip() + ") HAS GROUPS")
		
		# We will get all the section tables that are in each course block and put them in a list.
		# For each section table, we will essentailly do the exact same thing we did in the block of code above

		listOfSectionTables = courseBlk.findAll("table", {"class" : "sectionTable"})

		for st in listOfSectionTables:
			st = st.findAll("tr")

			semRow = st[1].findAll("td")
			labRow = st[2].findAll("td")


			# we now get the data needed for tempGroup

			SemClassNumber = semRow[0].text.strip()
			SemType = semRow[2].text.strip()
			SemDays = semRow[3].text.strip()

			# TO DO: write in an algorithm to find the start and end times.

			SemStartTime = semRow[4].text.strip()
			SemEndTime = semRow[4].text.strip()
			SemLocation = semRow[6].text.strip()
			SemInstructor = semRow[7].text.strip()


			LabClassNumber = labRow[0].text.strip()
			LabType = labRow[2].text.strip()
			LabDays = labRow[3].text.strip()

			# TO DO: write in an algorithm to find the start and end times.

			LabStartTime = labRow[4].text.strip()
			LabEndTime = labRow[4].text.strip()
			LabLocation = labRow[6].text.strip()
			LabInstructor = labRow[7].text.strip()

			tempGroup = c.group(SemClassNumber, SemType, SemDays, SemStartTime, SemEndTime, SemLocation, SemInstructor, LabClassNumber, LabType, LabDays, LabStartTime, LabEndTime, LabLocation, LabInstructor)

			listOfGroups.append(tempGroup)






		#listOfGroups.append(tempGroup)

	
	return listOfGroups






















#def findStartTime(time):



#def findEndTime(time):






def printCoursesInList(listOfCourses):
	for crse in listOfCourses:
		print(crse.courseCode + " - " + crse.courseName + " " + crse.units + " " + str(crse.ID))






def exportData(listOfCourses):
	import csv

	# everything in listOfCourses is currently an object. We need to make a 2 dimensional list where each row is a course,
	# and each column is an attribute.


	listForCSV = []

	with open('courses.csv', 'w') as csvOfCourses:
		csvWriter = csv.writer(csvOfCourses)


	





main()



