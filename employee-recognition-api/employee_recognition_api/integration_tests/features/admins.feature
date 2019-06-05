# admins.feature
@admins
Feature: Integration Tests - ADMINS

# 200 OK
Scenario Outline: GET /admins, 200
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>

    Examples: 
        | endpoint       | status_code | keys       | 
        | admins         | 200         | admin_ids  | 
        | admins/1       | 200         | created_timestamp,first_name,last_name,email_address,admin_id | 
        | admins/1/login | 200         | password   | 


Scenario Outline: POST & DELETE /admins, 200
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to <endpoint>

    Examples: 
        | endpoint      | status_code | keys       | body  |
        | admins        | 200         | admin_id   | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme"} |

Scenario Outline: PUT /admins, 200
    When I make a POST <endpoint> request with body { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme"} 
    When I make a PUT <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to <endpoint>
    Examples: 
        | endpoint      | status_code | keys      | body  |
        | admins        | 200         | admin_id   | { "first_name": "test1", "last_name": "test1", "email_address": "test1@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme1"}  |

Scenario Outline: PUT /admins/<admin_id>/login, 200
    When I make a POST <endpoint> request with body  { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme"} 
    When I make a login-only PUT <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to <endpoint>
    Examples:  
        | endpoint      | status_code | keys      | body  |       
        | admins        | 200        | admin_id   | { "password": "encryptme2" } |


# 400 BAD REQUEST
Scenario Outline: GET /admins
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint       | status_code | keys     | field   | message                | 
        | admins/3       | 400        | errors    | admin_id | admin_id does not exist |
        | admins/3/login | 400        | errors    | admin_id | admin_id does not exist | 

Scenario Outline: POST /admins; malformed request (single)
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint      | status_code | keys      | field           | message       | body  |  
        | admins        | 400         | errors    | first_name      | invalid value | { "first_name": "", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | admins        | 400         | errors    | last_name       | invalid value | { "first_name": "test", "last_name": "", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | admins        | 400         | errors    | email_address   | invalid value | { "first_name": "test", "last_name": "test", "email_address": "", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme", "signature_path": "test.jpg"} |
        | admins        | 400         | errors    | password        | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "tes", "signature_path": "test.jpg"} |
        | admins        | 400         | errors    | password        | invalid value | { "first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "testytestytestytesty", "signature_path": "test.jpg"} |
        
Scenario Outline: POST /admins; malformed request (many)
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result has <number> errors 

    Examples: 
        | endpoint      | status_code | keys      | number      | body  |  
        | admins        | 400         | errors    | 5           | { "first_name": "", "last_name": "", "email_address": "", "created_timestamp": "2018-05-00:00:00", "password": "en"} |

Scenario Outline: PUT /admins, malformed request (single)
    When I make a POST <endpoint> request with body {"first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme"} 
    When I make a PUT <endpoint> request with body <body>
    Then I clean up my POST to <endpoint>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>
    
    Examples: 
        | endpoint      | status_code | keys      | field           | message       | body  |  
        | admins        | 400         | errors    | first_name      | invalid value | { "first_name": "", "last_name": "test", "email_address": "test@oregonstate.edu"} |
        | admins        | 400         | errors    | last_name       | invalid value | { "first_name": "test", "last_name": "", "email_address": "test@oregonstate.edu"} |
        | admins        | 400         | errors    | email_address   | invalid value | { "first_name": "test", "last_name": "test", "email_address": "" } |

Scenario Outline: PUT /admins; malformed request (many)
    When I make a POST <endpoint> request with body {"first_name": "test", "last_name": "test", "email_address": "test@oregonstate.edu", "created_timestamp": "2018-05-08 00:00:00", "password": "encryptme" }
    When I make a PUT <endpoint> request with body <body>
    Then I clean up my POST to <endpoint>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result has <number> errors 

    Examples: 
        | endpoint      | status_code | keys      | number      | body  |  
        | admins        | 400         | errors    | 3           | { "first_name": "", "last_name": "", "email_address": "" } |
        
Scenario Outline: DELETE /admins
    When I make a DELETE <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint      | status_code | keys      | field    | message                 | 
        | admins/3      | 400         | errors    | admin_id | admin_id does not exist |
        