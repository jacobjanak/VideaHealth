[Videa Health Logo]()

[VideaHealth](https://www.videa.ai/) is a Boston-based startup that brings AI to the field of dentistry by automating the process of dental x-ray analysis. Today, denticians have to spend countless hours analyzing these images and they still miss up to 50% of pathologies in dental x-rays. VideaHealth is helping dentists identify diseases and communicate treatment recommendations to their patients.

Group members: Tony Chau, Jeffrey Garcia, Cameron Hayes, Ke Liu, Paul Maynard, Danley Nemorin, Suncharn Pipithkul, and Jacob Janak.

We worked on VideaHealth's neural network as part of our CS 410 Intro to Software Engineering class in the Spring of 2021. Our task was to design a postprocessing algorithm to identify the type and location of teeth in an x-ray. Their team had already designed and trained a neural network that ouputted some decent results. Our job was to refine those results into a single output. This is what the data from their nueral network looked like:

[Image of raw data]()

In the above image, you can see that there are far too many boxes for the number of teeth. The nueral network is outputting every possible box that it can think of and assigning it a probability score. We used these boxes and their respective scores to trim the output down to one box per tooth. This is what the results look like after our postprocessing algorithm is run:

[Image of refined data]()

Our results were quite good, achieving both a precision and recall of about 0.79. We used a non-maximum suppression algorithm to correctly output the boxes. Non-maximum suppression is a technique to filter the predictions of object detectors. We also wrote a seperate algorithm to assign the correct numbers to each tooth according to this chart:

[Teeth chart]()







#### Setup instructions to run main.py
1. Install the dependencies<br /><br />
<code>pip install -r requirements.txt</code>
