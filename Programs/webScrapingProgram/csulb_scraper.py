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
	semester_url = 'http://web.csulb.edu/depts/enrollment/registration/class_schedule/' + trm + '_' + yr + '/By_Subject/' + dpt +'.html#note1'

	#opening up connection, grabbing the HTML
	uClient = uReq(semester_url)
	page_html = uClient.read()
	uClient.close()

	#turning the page html into a soup that I can manipulate
	page_soup = soup(page_html, "html.parser")

	#declares the list of courses
	listOfCourses = []

	# tempCBL = a list that has every course block from the page
	tempCBL = page_soup.findAll("div", {"class" : "courseBlock"})

	for courseBlk in tempCBL:

		#This gets all the data I want to store later and puts it into variables

		# TODO: store the correct course number in the variable
		# TODO: save every variable as the correct data type
		school = "CSULB"
		term = trm
		year = yr
		department = dpt
		courseName = (courseBlk.find("span", {"class" : "courseTitle"})).text.strip()
		courseNumber = (courseBlk.find("span", {"class" : "courseCode"})).text.strip()
		units = stripUnits((courseBlk.find("span", {"class" : "units"})).text.strip())

		listOfGroups = getGroups(courseBlk)

		#constructs a temporary course obejct that is the current course we just grabbed saved as an object

		#TO DO: add "listOfGroups" to constructor
		tempCourse = c.course(school,term,year,department,courseName,courseNumber,units,listOfGroups)
		listOfCourses.append(tempCourse)


	return listOfCourses


def getGroups(courseBlk):
	import c

	#declares the list of groups that gets returned later on
	listOfGroups = []

	# declares isLAB
	isLAB = False


	# this goes through every class that does not have groups, and if it does have a lab, then it gets flagged by making isLAB true
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

			SemStartTime, SemEndTime = findTrueTime(row[4].text.strip())
			SemLocation = c.location(row[6].text.strip())
			SemInstructor = c.teacher(row[7].text.strip())

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

		SemStartTime, SemEndTime = findTrueTime(semRow[4].text.strip())
		SemLocation = c.location(semRow[6].text.strip())
		SemInstructor = c.teacher(semRow[7].text.strip())


		LabClassNumber = labRow[0].text.strip()
		LabType = labRow[2].text.strip()
		LabDays = labRow[3].text.strip()

		# TO DO: write in an algorithm to find the start and end times.

		LabStartTime, LabEndTime = findTrueTime(labRow[4].text.strip())
		LabLocation = c.location(labRow[6].text.strip())
		LabInstructor = c.teacher(labRow[7].text.strip())

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

			SemStartTime, SemEndTime = findTrueTime(semRow[4].text.strip())
			SemLocation = c.location(semRow[6].text.strip())
			SemInstructor = c.teacher(semRow[7].text.strip())


			LabClassNumber = labRow[0].text.strip()
			LabType = labRow[2].text.strip()
			LabDays = labRow[3].text.strip()

			# TO DO: write in an algorithm to find the start and end times.

			LabStartTime, LabEndTime = findTrueTime(labRow[4].text.strip())
			LabLocation = c.location(labRow[6].text.strip())
			LabInstructor = c.teacher(labRow[7].text.strip())

			tempGroup = c.group(SemClassNumber, SemType, SemDays, SemStartTime, SemEndTime, SemLocation, SemInstructor, LabClassNumber, LabType, LabDays, LabStartTime, LabEndTime, LabLocation, LabInstructor)

			listOfGroups.append(tempGroup)






		#listOfGroups.append(tempGroup)

	
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




