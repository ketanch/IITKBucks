## TASK 6
The server program has 2 end points:

**1. /add :** Receives POST request and adds a key-value pair to database if key doesn't exists already. If database gets updated 
corresponding key-value is also sent to /add end of peers.

**1. /list :** Receives GET request and returns all the database fields as response.

This program also maintains a **LOGFILE** which contains server side logs.
