## Why I made this
This project was created to help students create an optimal school schedule. While many schools (like CSULB) give you a bunch of potential schedules, I have found my friends and I have a common problem of building the optimal schedule for *us*. I have noticed that there are a couple things that are important to my friends:
	1. Minimizing time on campus
	2. Getting out as soon as possible everyday
	3. Avoiding classes before a certain time (typically 8AMs)
	4. Rate my professor scores
	5. Minimizing walking distance on campus
	6. Not having too many hard classes in 1 semester
	7. Minimizing the number of days on campus

## How it works
So, based off of how important these things are to you, this will try an optimize the performance.

There are 3 categories that I put things in:
	- MUST HAVE
	- WOULD LIKE
	- DOES NOT CARE

## Getting the data:
I used web scraping to get the data used in this program. Since every school has different websites, I created a different file for each school. In the future, I think that I could potentially have different contributors that just followed a basic format for their own school’s info to be scraped, and then added to the database using functions in files we already have. This way, that reduced the work I have to do in the future. 

Since I go to CSULB, the first school used was CSULB.

The file `csulb_scraper.py` will have a main function. 

The most important function in any scraper file is the `getCourses()` function. This returns an array of `course` objects.
