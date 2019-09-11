'''
	Data stored in each class:

	CLASS:
		course name
		course code
		units
		list of groups

	GROUP:
		If there IS NOT both a lab and a sem:
			Section Number
			Class #
			Type
			Days
			Start time
			End time
			Location
			Instructor

		If there IS both a lab and a sem:
			find the one that is tagged sem and assign everything in that row to the first elements.
			

			Sem Section Number
			Sem Class #
			Sem Type
			Sem Days
			Sem Start time
			Sem End time
			Sem Location
			Sem Instructor

			Lab Section Number
			Lab Class #
			Lab Type
			Lab Days
			Lab Start time
			Lab End time
			Lab Location
			Lab Instructor



	LOCATION:

	TEACHER:


'''


class course:
	# creates the first ID - every time a new class object is created, the class's ID becomes the static ID and then it increments it


	# defines the constructor
	def __init__(self,school,term,year,department,courseName,courseNumber,units,listOfSections):
		self.school = school
		self.term = term
		self.year = year
		self.department = department
		self.courseName = courseName
		self.courseNumber = courseNumber
		self.units = units
		self.listOfSections = listOfSections




class section:

	

	def __init__(self,classNumber,sectionType,days,startTime,endTime,location,instructor):
		self.classNumber = classNumber
		self.sectionType = sectionType
		self.days = days
		self.startTime = startTime
		self.endTime = endTime
		self.location = location
		self.instructor = instructor
		# self.coenrolledSections = coenrolledSections


class location:



	def __init__(self,name):
		self.name = name





class teacher:

	

	def __init__(self,name):
		self.name = name






class school:



	def __init__ (self,school_name,school_abv):
		self.school_name = school_name
		self.school_abv = school_abv


