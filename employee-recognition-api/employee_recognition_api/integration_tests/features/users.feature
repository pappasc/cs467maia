Feature: Integration Tests - USERS
# Skipping PUT /users/<user_id>/signature, as this would be a highly complex automated test.

# 200 OK
Scenario Outline: GET /users, 200
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>

    Examples: 
        | endpoint      | status_code | keys      | 
        | users         | 200         | user_ids  | 
        | users/1       | 200         | first_name,last_name,user_id,signature_path,created_timestamp,email_address | 
        | users/1/login | 200         | password  | 


Scenario Outline: POST & DELETE /users, 200
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to <endpoint>

    Examples: 
        | endpoint      | status_code | keys      | body  |
        | users         | 200         | user_id   | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |

Scenario Outline: PUT /users, 200
    When I make a POST <endpoint> request with body  { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"}
    When I make a PUT <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to <endpoint>
    Examples: 
        | endpoint      | status_code | keys      | body  |
        | users         | 200         | user_id   | { "first_name": "test1", "last_name": "test1", "email_address": "test1@oregonstate.edu", "signature_path": "test1.jpg"} |


Scenario Outline: PUT /users/<user_id>/login, 200
    When I make a POST <endpoint> request with body  { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"}
    When I make a PUT <endpoint> login request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to <endpoint>
    Examples:  
        | endpoint      | status_code | keys      | body  |       
        | users         | 200         | user_id   | { "password": "encryptme2"}


# 400 BAD REQUEST
Scenario Outline: GET /users
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint      | status_code | keys      | field   | message                | 
        | users/3       | 400         | errors    | user_id | user_id does not exist |
        | users/3/login | 400         | errors    | user_id | user_id does not exist | 

Scenario Outline: POST /users; malformed request (many)
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint      | status_code | keys      | field           | message       | body  |  
        | users         | 400         | errors    | first_name      | invalid value | { "first_name": "", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | last_name       | invalid value | { "first_name": "test", "last_name": "", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | email_address   | invalid value | { "first_name": "test", "last_name": "test", "email_address": "", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | password        | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "tes", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | password        | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "testytestytestytesty", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | signature_path  | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": ""} |
        | users         | 400         | errors    | signature_path  | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.png"} |

Scenario Outline: POST /users; malformed request (single)
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result has <number> errors 

    Examples: 
        | endpoint      | status_code | keys      | number      | body  |  
        | users         | 400         | errors    | 6           | { "first_name": "", "last_name": "", "email_address": "", "created_timestamp": "2018-05-00:00:00", "password": "en", "signature_path": "test.j"} |
        
Scenario Outline: PUT /users, malformed request (single)
    When I make a POST <endpoint> request with body {"first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} 
    When I make a PUT <endpoint> request with body <body>
    Then I clean up my POST to <endpoint>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>
    

    Examples: 
        | endpoint      | status_code | keys      | field           | message       | body  |  
        | users         | 400         | errors    | first_name      | invalid value | { "first_name": "", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | last_name       | invalid value | { "first_name": "test", "last_name": "", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | email_address   | invalid value | { "first_name": "test", "last_name": "test", "email_address": "", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | password        | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "tes", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | password        | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "testytestytestytesty", "signature_path": "test.jpg"} |
        | users         | 400         | errors    | signature_path  | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": ""} |
        | users         | 400         | errors    | signature_path  | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.png"} |


Scenario Outline: PUT /users; malformed request (many)
    When I make a POST <endpoint> request with body {"first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} 
    When I make a PUT <endpoint> request with body <body>
    Then I clean up my POST to <endpoint>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result has <number> errors 

    Examples: 
        | endpoint      | status_code | keys      | number      | body  |  
        | users         | 400         | errors    | 6           | { "first_name": "", "last_name": "", "email_address": "", "created_timestamp": "2018-05-00:00:00", "password": "en", "signature_path": "test.j"} |
        
Scenario Outline: DELETE /users
    When I make a DELETE <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint      | status_code | keys      | field   | message                | 
        | users/3       | 400         | errors    | user_id | user_id does not exist |
        