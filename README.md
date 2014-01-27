Benjamin-Scheduler
==================

The Benjamin School Text Message Scheduler

This project was designed to extract a text from the PDF of The Benjamin School Schedule. It then extracts the users
information from a MYSQL Database (Name, Phone Number, Carrier). In a Final Compile, It would compile and send the
schedule to each user that signed up (Via. Website). The Schedule will arrive at a set time (6:45). 

In the Future, we are planning to allow users of the service to add their own times when they would like it sent and,
their personal schedule. We are also planning to allow teachers to input the homework for the students and send it via. 
Text message. All of these projects are future versions.

Version 1.0
=================
  - Extracts Text from a PDF File (Benjamin Scheduler)
  - Sends a Email Via. Gmail Account
  - Reterieves MYSQL Data from Database (User Info - Phone, Name, Carrier)
  
  **Know Bugs**
  - PDF extractor crashes when given a unknown day (Not Realtive to Algorithm) 
  - Only can send a message every 3 - 5 seconds (Caused by Google Email)

Version 1.1
=================
