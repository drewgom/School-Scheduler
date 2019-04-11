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
	#creates the first ID - every time a new class object is created, the class's ID becomes the static ID and then it increments it

	staticID = 1000

	def __init__(self,courseName,courseCode,units):
		self.courseName = courseName
		self.courseCode = courseCode
		self.units = units
		self.ID = self.staticID
		staticID = self.staticID + 1






class group:
	def __init__(self,
			SemClassNumber, 
			SemType, 
			SemDays, 
			SemStartTime, 
			SemEndTime, 
			SemLocation, 
			SemInstructor,
			LabClassNumber = None,
			LabType = None,
			LabDays = None,
			LabStartTime = None,
			LabEndTime = None,
			LabLocation = None,
			LabInstructor = None):


		self.SemClassNumber = SemClassNumber
		self.SemType = SemType
		self.SemDays = SemDays
		self.SemStartTime = SemStartTime
		self.SemEndTime = SemEndTime
		self.SemLocation = SemLocation
		self.SemInstructor = SemInstructor
		self.LabClassNumber = LabClassNumber
		self.LabType = LabType
		self.LabDays = LabDays
		self.LabStartTime = LabStartTime
		self.LabEndTime = LabEndTime
		self.LabLocation = LabLocation
		self.LabInstructor = LabInstructor



