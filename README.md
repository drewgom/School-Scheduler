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
So, based off of how important these things are to you, this will try an optimize the performance. When the project is completed, you should be able to give a certain weight to each of these parameters, and then using the weights, 

## Getting the data:
I used web scraping to get the data used in this program. Since every school has different websites, I would have to create a different web scraper for each school.

Since I go to CSULB, the first school used was CSULB.

The file `csulb_scraper.py` will have a main function. When that gets run, then the user will have a CSV saved with the sections offered by a specificed subject in a specified semester
