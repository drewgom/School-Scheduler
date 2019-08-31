'''
Essential functions:
	getCourses:
		- webscrapes the course catalog, returns a list of course objects with all the data filled out
	getGroups:
		- takes a course and returns an array of all the sections that students can sign up for


Helpful functions:








'''





###############################################################################################################################
###############################################################################################################################
#------------------------------------------------------ESSENTIAL FUNCTIONS----------------------------------------------------#
###############################################################################################################################
###############################################################################################################################

def getCourses(dpt,trm,yr):
	import c
	from urllib.request import urlopen as uReq
	from bs4 import BeautifulSoup as soup


	#saves the CECS department's shedule into a variable
	semester_url = 'http://web.csulb.edu/depts/enrollment/registration/class_schedule/' + trm + '_' + yr + '/By_Subject/' + dpt +'.html'

	#opening up connection, grabbing the HTML
	uClient = uReq(semester_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")

	#declares the list of courses
	listOfCourses = []

	# tempCBL = a list that has every course block from the page
	tempCBL = page_soup.findAll("div", {"class" : "courseBlock"})

	for courseBlk in tempCBL:
		courseName = (courseBlk.find("span", {"class" : "courseTitle"})).text.strip()
		courseNumber = (courseBlk.find("span", {"class" : "courseCode"})).text.strip()
		units = stripUnits((courseBlk.find("span", {"class" : "units"})).text.strip())

		listOfGroups = getGroups(courseBlk)

		#constructs a temporary course obejct that is the current course we just grabbed saved as an object

		#TO DO: add "listOfGroups" to constructor
		tempCourse = c.course("CSULB",trm,yr,dpt,courseName,courseNumber,units,listOfGroups)
		listOfCourses.append(tempCourse)


	return listOfCourses


def getGroups(courseBlk):
	import c

	#declares the list of groups that gets returned later on
	listOfGroups = []

	# We need to determine if we need to enroll in a lab for this course as well. We can
	# do this by checking for these phrases in the course block's group message:
	# 	- 'Enrollment required for SEM,LAB in this group of sections.' or 
	# 	- 'Enrollment required for LEC,LAB in this group of sections.'

	# If neither of those phrases are in the group message, then we are able to scrape the sections by themeselves. Otherwise,
	# coenrollment is required, thus every section needs to have a list of the courses that the student can coenroll in. Every SEM or
	# LEC can be coenrolled to any of the labs in its section table.
	
	# We do this by creating a boolean. If it finds that coenrollment is required, then we have to do the code that links the labs to
	# their seminar or lecture.

	coenroll = False


	# This sections tests for coenrollment. It does this by seeing if there is a group message on the website. If there is,
	# then we need to see if the message is one of the messages that indicates that coenrollment is necessary.

	gm = (courseBlk.find("div", {"class" : "groupMessage"}))

	if (gm != None):
		name = courseBlk.find("span", {"class" : "courseTitle"}).text.strip()
		message = gm.find("p").text.strip()
		if (message == "Enrollment required for SEM,LAB in this group of sections.") or (message == "Enrollment required for LEC,LAB in this group of sections."):
			coenroll = True
			print(name + "    " + message)


	if coenroll:
		# Since we know that coenrollment is required, we now need to go through every section table and create the section objects
		listOfSectionTables = courseBlk.findAll("table", {"class" : "sectionTable"})

		#Now, we need to find which spot in the table all of our variables are in. We need to store:
		for table in listOfSectionTables:
			for rowNum in range(0,len(table)-1):
				if rowNum == 0:
					SecNumSpot = findSpot("SEC.",table)
					ClassNumSpot = findSpot("CLASS #", table)
					TypeSpot = findSpot("TYPE", table)
					DaysSpot = findSpot("DAYS", table)
					TimeSpot = findSpot("TIME", table)
					LocationSpot = findSpot("LOCATION", table)
					InstructorSpot = findSpot("INSTRUCTOR", table)

					

	return listOfGroups



###############################################################################################################################
###############################################################################################################################
#-------------------------------------------------------HELPFUL FUNCTIONS-----------------------------------------------------#
###############################################################################################################################
###############################################################################################################################

# The times on the website are stored as one string. This needs to be seperated in to two seperate variables for later,
# when we are trying to compare the start time and end time
def findTrueTime(stringTime):

	startTime = "Start"
	endTime = "End"

	# This code looks for the index of the "-" which delineates the start and end time.
	i = stringTime.find("-")

	# If there is no dash to be found, then that means there currently is not an assigned time

	if (i == -1):
		startTime = stringTime
		endTime = stringTime

		return startTime, endTime

	else:
		startTime = stringTime[:i]
		endTime = stringTime[(i+1):]


	# We now need to have our program pick the proper suffix: AM or PM.
	# We can always do this by finding the index of "M" and then subtracting one to get the letter "A" or "P".

	m = stringTime.find("M")

	endSuffix = stringTime[(m-1):]



	# Our challenge now is trying to figure out what hour the class starts and ends.
	# We can search for a ":", and everything before that will be the hour of the time. However, this is not perfect since
	# this won't happen in all cases. If there is not a ":", then we need to just find the time before either i(for start times) 
	# or m-1 (for end times)

	j = startTime.find(":")
	k = endTime.find(":")



	if (j == -1):
		startHour = startTime
	else:
		startHour = startTime[:j]
	if (k == -1):
		endHour = endTime[:(m-1)]
	else:
		endHour = endTime[:k]


	# We might run in to issues when there is a class that starts at an AM time and ends at a PM time. However,
	# The only number that can really cause us an issue is 12 - since for all other numbers, we can run a test on whether
	# or not the end time is less than the start time - if the end time isn't in the 12 hour, then the start time here is 
	# always going to be less than the end time.

	# Although this solution is not perfect, it will work for our case.

	if (endHour == "12"):
		if (int(startHour) < int(endHour)):
			startSuffix = "AM"
		else:
			startSuffix = "PM"
	elif (int(endHour) < int(startHour) and startHour != "12"):
		startSuffix = "AM"
	else:
		startSuffix = endSuffix


	# We now add the suffix to the start time

	startTime = startTime + startSuffix

	return startTime, endTime


def printCoursesInList(listOfCourses):
	

	for crse in listOfCourses:
		print(crse.school,crse.term,crse.year,crse.department,crse.courseNumber,crse.courseName,crse.units)


# the amount of units comes off of the website as "X Units". I would rather have this saved as
# an int.

def stripUnits(tempUnits):

	tempUnits = tempUnits[0]
	tempUnits = int(tempUnits)
	return tempUnits





def findSpot(kw, table):
	listOfth = table.findAll("th")
	spot = 0
	for th in listOfth:
		if th.text.strip() == kw:
			return spot
		spot = spot + 1


