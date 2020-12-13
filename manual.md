# Climber
Software to automate entry of vaccination data into Pinnacle/Outcomes4Health

##Workflow
This software allows you to print out a list of patients, from your preferred clinical system.
As the patients are vaccinated, your clinic co-ordinator records in pen which vaccinator
has given them a vaccine. The completed forms are then scanned, and the data is entered into Pinnacle.

##Caveats
The software will record every patient as receiving their vaccine in the left arm, and giving their own consent. Your
vaccinators will need to keep a list of patients who received their vaccine in
other sites (eg right arm) and those whose consent was recorded for best interests.
Any patient who ends up not getting vaccinated must also be recorded.

These "exceptions" can then be adjusted after the main data entry process.

##Instructions
###Set up vaccinators
On the first tab (labelled "Vaccinators") enter initials for each vaccinator, and their name *as it appears in pinnacle*.
There is a limit of seven vaccinators

###Import patient data from Emis
***FIXME***
You will need to ensure that under Appointments config you have selected DOB, NHS number and name in patient details
For each vaccination session on EMIS, right click on the session header and select
`print include patient details`
Save the patient lists on your computer
Do this for each session you are running concurrently.
From the second tab (labelled "Make Forms"), click "Import Session", and choose all the rtf files you have previously saved

###Import patient data from SystmOne
Not sure here, you need to generate a csv with following columns:
* Time of appointment
* Patient Name
* Date of Birth
* NHS Number
From the second tab (labelled "Make Forms"), click "Import Session", and choose all the csv files you have previously saved

###Create Forms
At this point you should see all the appointment data in a list, ordered by appointment time.
Click "Create Forms", a pdf with all the appointments will be generated. 
Print this out on A4 Paper, make sure that all the circles at the corners print correctly

###Vaccinate
As patients arrive and you direct them to a vaccinator, put a cross or other
mark in the box corresponding to that vaccinator (their initials are at the top of the form)
If you make a mistake put a mark in another box and this entry will be rejected, and will need to be 
entered manually.

###Scan
Scan the completed forms in at 300dpi, save the files as png, jpeg or tiff. Climber can
cope with multi-page tiffs.

###Read Forms
On the third tab click "Load forms", and select all the images you want to read.
The computer will read the data of the forms, this may take some time, depending on how powerful your
computer is. Once the data is read in, you will see it in a list
