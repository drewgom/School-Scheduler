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

	index = 0
	for courseBlk in tempCBL:

		if index > 0:
			break

		courseName = (courseBlk.find("span", {"class" : "courseTitle"})).text.strip()
		courseNumber = (courseBlk.find("span", {"class" : "courseCode"})).text.strip()
		units = stripUnits((courseBlk.find("span", {"class" : "units"})).text.strip())

		listOfSections = getSections(courseBlk)

		#constructs a temporary course obejct that is the current course we just grabbed saved as an object

		#TO DO: add "listOfSections" to constructor
		tempCourse = c.course("CSULB",trm,yr,dpt,courseName,courseNumber,units,listOfSections)
		listOfCourses.append(tempCourse)

		print(tempCourse.courseName)
		print(" ")
		print(" ")
		print(" ")
		print(" ")
		index += 1

	return listOfCourses













def getSections(courseBlk):
	# The first thing we are going to do once we recieve a course block is to turn it in to a list of tables. This is becuase 
	# Each table is a self-contained group, so typically if coenrollemnt is required, then it is allowed within the group

	listOfTables = courseBlk.findAll("table" , {"class" : "sectionTable"})

	# Since python creates an iterator when using a for loop, I decided to just use a while loop so that I could modify each
	# table object in the list.
	for i in range(len(listOfTables)):
		listOfTables[i] = makeTableToList(listOfTables[i])

	print(listOfTables[0][1][10])




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


'''
def makeTableToList(htmlTable):
	tableAsList = []
	htmlrows = htmlTable.findAll('tr')
	for htmlrow in htmlrows:
		htmlths = htmlrow.findAll('th')
		htmltds = htmlrow.findAll('')

		tableAsList.append(row)
	return tableAsList
'''



def makeTableToList(htmlTable):
	tableAsList = []
	htmlrows = htmlTable.findAll('tr')
	#index = 0
	for htmlrow in htmlrows:
		rowAsList = []
		htmlths = htmlrow.findAll('th')
		htmltds = htmlrow.findAll('td')
		for th in htmlths:
			thToBeAdded = th.text.strip()
			rowAsList.append(thToBeAdded)
		for td in htmltds:
			tdToBeAdded = td.text.strip()
			rowAsList.append(tdToBeAdded)


		tableAsList.append(rowAsList)

	return tableAsList