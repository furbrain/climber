# Climber
This software allows you to record vaccinations in bulk and then upload them to [Pinnacle/Outcomes4Health](https://outcomes4health.org/o4h/),
massively reducing the administrative burden associated with the NHS Covid-19 Vaccination program

This software is optimised to work with [AccuBook](https://support.accurx.com/en/collections/2671154-accubook-booking-patients-in-for-vaccinations),
but can also work directly with appointment lists from EMIS

It is written by Phil Underwood - I have a passion for coding and work as a GP within the NHS

## Data Security
I take data security very seriously. This software does not write any patient identifiable information to disk. It does not store any
usernames or passwords. The only time patient data is sent over the internet is during the upload process to Outcomes4Health. No information
whatsoever is sent to myself.

## Limitations
This software assumes that all vaccinations are done with the patient's consent, are done into the left deltoid, and are not done in a residential home. You will need to keep
a manual record of all patients for whom this is not correct and correct them after the upload, or mark the record as invalid before scanning,
and perform all of the data entry manually for these patients.

## Installation
Firstly you need to ensure that you have an up-to-date version of Microsoft Edge (*not* legacy). Most computers should have this
installed, but if not you can get it [here](https://www.microsoft.com/en-us/edge)
Download the installer from [Github](https://github.com/furbrain/climber/releases/latest) - you will need to download and run
`climber_install.exe`. Windows will like alert you that this is untrusted code - look for something like "see more" or "run anyway".
(PS you should not do this unless you *really* trust the source of the software you are installing)

## Before the vaccination session
Before starting the software, you will need to log into accubook, choose `Booked List`, and click export next to the session you want to
set up. Save this file (should be session-xxxx.csv) somewhere safe. You may want to create a folder for each vaccination session on a secure
drive.
Once this is done, run Climber - you'll find it from the Start Menu. You will see multiple tabs along the top of the app, and we generally move through them from
left to right

On the `Vaccinators` tab, enter the initials and names of your vaccinators for the planned session. It is important that Pinnacle is able to identify
your vaccinators, so once you have done this click on the `Confirm Vaccinators` button. This will fire up an Edge browser on the login
page for Pinnacle - log in and navigate to the Covid 20/21 vaccination service page. Click `OK` and you will see the software take control
of Edge and check that all of your vaccinators are recognised. It is important that all vaccinators log in at least once into Pinnacle, so
they can enter their GMC/NMC numbers and are fully registered on the system

Once you get the all-clear you can move on to the next tab `Create Forms`

## Creating the forms
* Click `Import Appointments` and select the csv file you saved earlier
* You will see all the appointment slots created and you will get a total number of patients booked in at the bottom
* Click `Create Forms` - this will create a pdf file, which you can either save or print out. This is what you will use to record
  attendance and vaccinator during the vaccination session itself
* Notice the black circles at each corner of the form. These are really important for the scanning process later on and its vital 
  that the forms print out cleanly and clearly.
  
## During the session
* As patients arrive and are directed to a vaccinator, simple make a cross in the relevant box on the form
* If you make a mistake add a cross to another box in the form, or write in the boxes who actually did the vaccination.
  These patients will not be uploaded automatically and you will need to do these manually later
* If any patients do not attend, leave their boxes blank. They will also not be uploaded.

## After the session
* Scan all of the completed forms back in as jpg files - this will depend on your scanning software. They should be scanned in at 300dpi
  as either grayscale or black and white images. Save these to a secure folder
* If you have closed the climber software previously, you will need to restart it and re-enter the vaccinator details - it is important
  that you enter them in the same order as they appear on the forms. You will also need to repeat the `Import appointments` step, but you
  do not need to recreate the pdf forms
* Now select the `Submit Scans` tab and choose `Read Scanned Forms`. Select all the scanned images you just created. Climber will now start
  reading them, but this process may take up to 20 minutes or so. Have a cup of tea while you wait!
* Once everything is scanned in, you can now select patients to upload; I would suggest just click on a few of them to start with to check
  everything is working ok. You will need to log into Pinnacle again. 
* Enter the details of the batch of vaccine you are working with and the date of the clinic; for AstraZeneca vaccines just use the same
  date for expiry and use-by dates.
* Press OK and wait while all of your vaccination data is uploaded to Pinnacle. This can take several hours, but no supervision is required

## After the upload
* Not all patient details will successfully upload. You can check the `Completed`tab for a list of all patients who successfully uploaded.
* Unsuccessful uploads, DNAs, and incorrectly filled forms will be in the `Errors` tab. Here you can click `Print Errors` to get a PDF
  summary of any failed uploads and any badly completed forms (with images of the relevant bit of form). You can use this to manually enter
  any missing details.
