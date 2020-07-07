# chaox-automatic-sign-in

Most of the courses this semester are in chaoxing, so I wrote a script to cope with the check-in of the courses published by the teacher, so that I can get more sleep time.

## Chaox Killer

For [http://mooc1-api.chaoxing.com/](http://mooc1-api.chaoxing.com/)

## Features

Regularly monitor and automatically complete the registration of multiple courses.

Bypass check-in with verification (gesture check-in, photo sign-in wait)



## How to use

 1. Speed(s) is the frequency of monitoring
 2. After starting the main program, if it is the first time to start "Cookies", it will display "unknown", which needs to be obtained manually.
 3. Login http://i.mooc.chaoxing.com/s”pace/
 4. Open F12, enter the network item and then refresh, select the html file, open any one.You can view your cookies.
 5. Copy the cookie and fill in the corresponding location in the program. Click the bottom button to complete
updated.

THEN

If you can get the course successfully, it means the operation is successful.

 1. Select a course and click **"ADD"** to add it to the monitoring queue.
 
 2. And **"CLEAR"** can clear the task with one click.
 
 3. After setting the frequency, you can click "START" to start monitoring.
 
 4. In addition, you can set the time you want to start monitoring through the area above the task queue, the correct format is %Year-%month-%day\space%hour:%minute

## Remarks

 1. Although the location check-in can be successful, the teacher will display the unsubmitted location information.
 
 2. Gesture sign-in can be directly successful, but it may be found that the sign-in is successful before the gesture is announced.
 
 3. The transparent layer is uploaded when the photo is checked in.
 
 4. This version needs to keep the computer on standby all the time, and the server version can be used to practice the author.

## Author information

 1. NAME: BoogieLing'o
 2. Contact email: boogieLing_o@qq.com

If you can actively communicate with me after you find the problem, I will be grateful.

Development environment: Ubuntu 18.04.4 LTS

Development language: Python 3.6.9

