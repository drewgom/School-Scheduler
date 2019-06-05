# This will create a fresh CSV that will serve as the database for all objects in the project.
# Do not run this once it is already created, unless you want to make your database fresh (perhaps it would be simpler if you just had your school in your database)
def initcsvs():
	import csv


	coursefile = "courses.csv"
	groupsfile = "groups.csv"

	with open(coursefile, mode = 'w') as courses:
		coursefile_writingStream = csv.writer(courses, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

		# writes the header
		coursefile_writingStream.writerow(['ID','University','Year','Term','Department','CourseName','CourseNumber','Units'])

	courses.close()


	with open(groupsfile, mode = 'w') as groups:
		groupsfile_writingStream = csv.writer(groups, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

		# writes the header
		groupsfile_writingStream.writerow(['ID','courseID', 'SemClassNumber', 'SemType', 'SemDays', 'SemStartTime', 'SemEndTime', 'SemLocation', 'SemInstructor', 'LabClassNumber', 'LabType', 'LabDays', 'LabStartTime','LabEndTime', 'LabLocation', 'LabInstructor'])

	groups.close()

	

def export_courses(listOfCourses):
	import csv


	coursefile = "courses.csv"
	groupsfile = "groups.csv"


	# TODO: check for the size. if the size is greater than 2, then look for the largest ID to start as the root ID
	with open(coursefile, mode = 'a') as courses:
		coursefile_appendStream = csv.writer(courses, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)


		courseID = getNextID(coursefile)
		groupID = getNextID(groupsfile)

		for crse in listOfCourses:
			# adds the class to the CSV
			coursefile_appendStream.writerow([str(courseID),crse.school,crse.year,crse.term,crse.department,crse.courseName,crse.courseNumber,str(crse.units)])

			# for every course, we need to add each section / group. we will do this in a seperate CSV by using a courseID as a foreign key

			with open(groupsfile, mode = 'a') as groups:
				groupsfile_appendStream = csv.writer(groups, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

				for grp in crse.listOfGroups:
					
					groupsfile_appendStream.writerow([str(groupID),str(courseID), grp.SemClassNumber, grp.SemType, grp.SemDays, grp.SemStartTime, grp.SemEndTime, grp.SemLocation, grp.SemInstructor, grp.LabClassNumber, grp.LabType, grp.LabDays, grp.LabStartTime, grp.LabEndTime, grp.LabLocation, grp.LabInstructor])

					groupID += 1

			courseID += 1


			groups.close()
	courses.close()













def getNextID(filename):
	import csv

	# The first opening gets the number of rows
	with open(filename, 'r') as givenCSV:
		rowCount = sum(1 for row in givenCSV)
	givenCSV.close()
	return rowCount
'''
	if rowCount == 0:
		raise Exception("the CSV you gave is empty.")

	elif rowCount == 1:
		return int(1)

	else:
		listOfIDs = []

		with open(filename, 'r') as givenCSV:
			data = [row for row in csv.reader(givenCSV)]
		givenCSV.close()

		for row in data:
			listOfIDs.append()
		return int(0)
'''




getNextID("courses.csv")

