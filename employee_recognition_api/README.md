# employee-recognition-api

## status codes
employee-recognition-api will send the following status codes in these situations:
- 200: successful api request & response
- 400: malformed api request, or api request can't be performed (i.e. trying to select, update, or delete something that doesn't exist)
- 401: stretch goal, implemented if api keys are implemented 
- 403: user / admin attempts to access api they don't have access to
- 404: endpoint doesn't exist 
- 500: internal service error (service isn't up)

## endpoints

examples requests/responses to each endpoint of employee-recognition-api

### any 

any enpoint may return these statuses/responses

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 404    | application/json | ```{ "errors": [ { "reason": "not found" }] } ```                                                                                               |
| 500    | n/a              | n/a                                                                                                                                             | 

### users

GET /users
- **function:** returns list of all user ids
- **request:** ```curl -X GET <url>/users```
- **response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "user_ids": [ { "user_id": 1, first_name": "Natasha", "last_name": "Kvavle", "email_address": "kvavlen@oregonstate.edu, "created_timestamp": "2019-04-15 08:52:00", "signature_path": "kvavlen_sig.jpg" } ] } ```                                                                                                                                 |

GET /users/{user_id}
- **function:** returns user's information based on user_id
- **example request:** ```curl -X GET <url>/users/1```
- **example response:**

| status | content-type     | example body                                                                                                                                                                         |
| -------| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 200    | application/json | ```{ "user_id": 1, first_name": "Natasha", "last_name": "Kvavle", "email_address": "kvavlen@oregonstate.edu, "created_timestamp": "2019-04-15 08:52:00", "signature_path": "kvavlen_sig.jpg" }``` |
| 400    | application/json | ```{ "errors": [ { "field": "user_id", "message": "user_id does not exist" } ] }```                                                                                                  |

GET /users/{user_id}/login
- **function:** returns user's password based on user_id
- **example request:** ```curl -X GET <url>/users/1/login```
- **example response:**

| status | content-type     | example body                                                                                                                                                                         |
| -------| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 200    | application/json | ```{ "password": "encryptme" }```                                                                                                                      |
| 400    | application/json | ```{ "errors": [ { "field": "user_id", "message": "user_id does not exist" } ] }```                                                                    |

POST /users 
- **function:** adds new user, returns user_id
- **note:** expectation is that you're sending encrypted password
- **example request:** ```curl -H 'Content-Type: application/json' -X PUT <url>/users -d '{ "first_name": "Sasha", "last_name": "green", "email_address": "greens@oregonstate.edu", "created_timestamp": "2018-04-16 00:00:00", "password": "encryptme" }'``` 
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "user_id": 3 }```                                                                                                                          |
| 400    | application/json | ```{ "errors": [ { "field": "created_timestamp", "message": "invalid value" } ] }```                                                            |


PUT /users/{user_id}/signature 
- **note:** I'm the least confident about this endpoint, and may make changes to make more secure
- **function:** update user's information (signature) based on user_id
- **example request:** ```curl -H 'Content-Type: image/jpeg' -X PUT <url>/users/3/signature --upload-file "greens_sig.jpg"```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "user_id": 3 }```                                                                                                                          |
| 400    | application/json | ```{ "errors": [ { "field": "user_id", "message": "user_id does not exist" } ] }```                                                             |

PUT /users/{user_id}
- **function:** update user's information based on user_id
- **note:** leaving in the unchanged values as this will be pre-populated in form
- **example request:** ```curl -H 'Content-Type: application/json' -X PUT <url>/users/1 -d '{ "first_name": "Sarah", "last_name": "Kvavle", "email_address": "kvavlen@oregonstate.edu, "password": "encryptme", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "kvavlen_sig.jpg" }'```
- **response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "user_id": 3 }```                                                                                                                          |
| 400    | application/json | ```{ "errors": [ { "field": "user_id", "message": "user_id does not exist" } ] }```                                                             |

DELETE /users/{user_id}
- **function:** delete user based on user_id, but delete is not cascading and will not delete awards created by user
- **example request:** ```curl -H 'Content-Type: application/json' -X DELETE <url>/users/3```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "user_id": null }```                                                                                                                       |
| 400    | application/json | ```{ "errors": [ { "field": "user_id", "message": "user_id does not exist" } ] }```                                                             |

### admins

GET /admins
- **function:** returns admin's information based on admin_id
- **example request:** ```curl -X GET <url>/admins```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "admin_ids": [ { "admin_id": 1, first_name": "Conner", "last_name": "Pappas", "email_address": "pappasc@oregonstate.edu, "created_timestamp": "2019-04-15 08:52:00" } ] }```  |

GET /admins/{admin_id}
- **function:** returns admin's information based on admin_id
- **example request:** ```curl -X GET <url>/admins/1```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "admin_id": 1, first_name": "Conner", "last_name": "Pappas", "email_address": "pappasc@oregonstate.edu, "created_timestamp": "2019-04-15 08:52:00" }```  |
| 400    | application/json | ```{ "errors": [ { "field": "admin_id", "message": "admin_id does not exist" } ] }```                                                           |

GET /admins/{admin_id}/login 
- **function:** returns admin's information based on admin_id
- **example request:** ```curl -X GET <url>/admins/1/login```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "password": "encryptme }```  |
| 400    | application/json | ```{ "errors": [ { "field": "admin_id", "message": "admin_id does not exist" } ] }```                                                           |

POST /admins
- **function:** adds new admin, returns admin_id
- **example request:** ```curl -H 'Content-Type: application/json' -X POST <url>/users -d '{ "first_name": "Tara", "last_name": "Nova", "email_address": "novat@oregonstate.edu", "password": "encrypteme", "created_timestamp": "2018-04-17 00:00:00" }'```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "admin_id": 2 }```                                                                                                                         |
| 400    | application/json | ```{ "errors": [ { "field": "created_timestamp", "message": "invalid value" } ] }```                                                            |

PUT /admins/{admin_id}
- **function:** returns admin's information based on admin_id
- **example request:** ```curl -H 'Content-Type: application/json' -X PUT <url>/users/2 -d '{ "first_name": "Ann", "last_name": "Nova", "email_address": "novat@oregonstate.edu", "password": "encrypteme", "created_timestamp": "2018-04-17 00:00:00" }'```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "admin_id": 2 }```                                                                                                                         |
| 400    | application/json | ```{ "errors": [ { "field": "password", "message": "string length maximum exceeded" } ] }```                                                    |

DELETE /admins/{admin_id}
- **function:** deletes admin based on admin_id
- **example request:** ```curl -H 'Content-Type: application/json' -X DELETE <url>/users/2 -d '{"creds": { "employee_type": "admin", "id": 2, "password": "encryptme" } }'```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "admin_id": null }```                                                                                                                      |
| 400    | application/json | ```{ "errors": [ { "field": "admin_id", "message": "admin_id does not exist" } ] }```                                                           |

### awards 

GET /awards/{award_id}  
- **function:** returns award's information based on award_id
- **example request:** ```curl -X GET <url>/award_id/1```
- **example response:**

| status | content-type     | example body                                                                                                                                                |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" } ```  |
| 400    | application/json | ```{ "errors": [ { "field": "award_id", "message": "award_id does not exist" } ] }```                                                                       |

GET /awards/authorize/{authorizing_user_id}
- **function:** returns a list of awards authorized by user_id
- **example request:** ```curl -X GET <url>/awards/authorize/1```
- **example response:**

| status | content-type     | example body                                                                                                                                                |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_ids": [ { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" }, { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 4, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" } ] ```                    |
| 400    | application/json | ```{ "errors": [ { "field": "authorizing_user_id", "message": "authorizing_user_id does not exist" } ] }```                                                 |

GET /awards/receive/{receiving_user_id} 
- **function:** returns a list of award IDs received by user_id
- **example request:** ```curl -X GET <url>/awards/receive/2```
- **example response:**

| status | content-type     | example body                                                                                                                                                |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_ids": [ { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" }, { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 4, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" } ] ```                    |
| 400    | application/json | ```{ "errors": [ { "field": "receiving_user_id", "message": "receiving_user_id does not exist" } ] }```                                                     |

GET /awards/type/{type}
- **function:** returns a list of award IDs of given type 
- **example request:** ```curl -X GET <url>/awards/type/week```
- **example response:**

| status | content-type     | example body                                                                                                                                                |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_ids": [ { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" }, { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 4, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" } ] ```                    |
| 400    | application/json | ```{ "errors": [ { "field": "type", "message": "type does not exist" } ] }```                                                                               |

GET /awards/datetime/{datetime}
- **function:** returns a list of award IDs awarded after provided datetime
- **example request:** ```curl -X GET <url>/awards/datetime/2018-09-05&00:00:00```
- **example response:**

| status | content-type     | example body                                                                                                                                                |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_ids": [ { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" }, { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 4, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" } ] ```                    |
| 400    | application/json | ```{ "errors": [ { "field": "datetime", "message": "invalid value" } ] }```                                                                                 |

GET /awards/distributed/{distributed}
- **function:** returns a list of awards distributed (or yet to be distributed) based on boolean
- **example request:** ```curl -X GET <url>/awards/distributed/true```
- **example response:**

| status | content-type     | example body                                                                                                                                                |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_ids": [{ "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" }, { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 4, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" } ] ```                    |
| 400    | application/json | ```{ "errors": [ { "field": "distributed", "message": "invalid value" } ] }```                                                                              |

POST /awards
- **function:** adds new award, returns award_id; imposes limits on how many awards are possible, depending on the type of award (1 per week, 1 per month); note that the api will override any "distributed" parameter to false
- **example request:** ```curl -H 'Content-Type: application/json' -X POST <url>/awards -d '{ "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", "awarded_datetime": "2019-04-18 12:00:00" }'```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_id": 2 }```                                                                                                                         |
| 400    | application/json | ```{ "errors": [ { "field": "type", "message": "type does not exist" } ] }```                                                                   |
| 403    | application/json | ```{ "errors": [ { "message": "award of type {type} maximum exceeded" } ] }```                                                                  |

DELETE /awards/{award_id}
- **function:** deletes award based on award_id
- **example request:** ```curl -H 'Content-Type: application/json' -X DELETE <url>/awards/1```
- **example response:**

| status | content-type     | example body                                                                                                                                    |
| -------| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 200    | application/json | ```{ "award_id": null }```                                                                                                                      |
| 400    | application/json | ```{ "errors": [ { "field": "award_id", "message": "award_id does not exist" } ] }```                                                           |

## stretch goals
if time allows, I will be implementing some way to prevent anyone but the maia group from accessing this api (i.e. api keys, basic auth)

## references 

### re: use of markdown language
1. https://www.markdownguide.org/cheat-sheet
2. https://dillinger.io/
3. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#tables

### re: API requests/response format 
4. https://docs.couchdb.org/en/stable/intro/curl.html
5. https://philsturgeon.uk/api/2016/01/04/http-rest-api-file-uploads/
6. https://stackoverflow.com/questions/12667797/using-curl-to-upload-post-data-with-files
7. https://stackoverflow.com/questions/5143915/test-file-upload-using-http-put-method
8. https://jsonapi.org/examples/ 
9. https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask 
10. https://softwareengineering.stackexchange.com/questions/314066/restful-api-should-i-be-returning-the-object-that-was-created-updated
11. https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api 
- Modeled my responses off of examples provided in resource 11
12. https://hackernoon.com/restful-api-designing-guidelines-the-best-practices-60e1d954e7c9

### re: Google Cloud App Engine set-up 
13. https://cloud.google.com/appengine/docs/standard/python/quickstart 
14. https://console.cloud.google.com/appengine/start/deploy?language=python&environment=standard&project=maia-backend&organizationId=717626756570

### re: general references for developing API & unit tests
15. https://www.python.org/dev/peps/pep-0008/
16. https://docs.python.org/3.3/tutorial/classes.html
17. https://docs.python.org/2.7/library/unittest.html
18. https://docs.python.org/3/tutorial/datastructures.html
19. https://docs.python.org/2/tutorial/classes.html
20. https://stackoverflow.com/questions/3434581/accessing-a-class-member-variables-in-python
21. https://docs.python.org/2.7/library/unittest.html#unittest.TestCase.setUp
22. https://stackoverflow.com/questions/456481/cant-get-python-to-import-from-a-different-folder re: __init__.py usage
23. https://stackoverflow.com/questions/52305191/using-self-vs-cls-to-access-variable-in-unittest/52305252
24. https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27 re: libraries to use
25. https://github.com/pallets/flask-sqlalchemy how to use flask-sqlalchemy
26. https://docs.python.org/2/library/logging.html re: logging
27. https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python re: getting current time in python