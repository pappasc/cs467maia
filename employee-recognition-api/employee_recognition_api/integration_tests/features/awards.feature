# awards.feature
@awards
Feature: Integration Tests - AWARDS

# 200 OK
Scenario Outline: GET /awards, 200
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>

    Examples: 
        | endpoint           | status_code | keys        | 
        | awards/1           | 200         | authorizing_user_id,distributed,awarded_datetime,receiving_user_id,award_id,type       | 
        | awards/authorize/1 | 200         | award_ids   | 
        | awards/receive/1   | 200         | award_ids   |
        | awards/type/week   | 200         | award_ids   |
        | awards/datetime/2018-04-01 | 200  | award_ids   |
        | awards/distributed/false | 200    | award_ids   |  


Scenario Outline: POST & DELETE /awards, 200
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then I clean up my POST to awards
    
    Examples: 
        | endpoint          | status_code | keys       | body  |
        | awards/no-email   | 200         | award_id   | { "authorizing_user_id": 2, "receiving_user_id": 1, "type": "week", "awarded_datetime": "2021-05-01 12:00:00" } |


Scenario Outline: GET /awards, 200 but empty
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>

    Examples: 
        | endpoint              | status_code   | keys         | 
        | awards/receive/1000   | 200           | award_ids    | 
        | awards/authorize/1000 | 200           | award_ids    |  

# 400 BAD REQUEST
Scenario Outline: GET /awards
    When I make a GET <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint       | status_code | keys     | field   | message   | 
        | awards/2       | 400        | errors    | award_id | award_id does not exist |

Scenario Outline: POST /awards; malformed request (single)
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint              | status_code | keys      | field           | message       | body  |  
        | awards/no-email       | 400         | errors    | awarded_datetime | invalid value | { "authorizing_user_id": 2, "receiving_user_id": 1, "type": "week", "awarded_datetime": "2020-05-12:00:00" } |
        | awards/no-email       | 400         | errors    | type        | invalid value | { "authorizing_user_id": 2, "receiving_user_id": 1, "type": "asdf", "awarded_datetime": "2020-05-01 12:00:00" } |
        
Scenario Outline: POST /awards; malformed request (many)
    When I make a POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result has <number> errors 

    Examples: 
        | endpoint          | status_code | keys      | number      | body  |  
        | awards/no-email   | 400         | errors    | 2           | { "authorizing_user_id": 2, "receiving_user_id": 1, "type": "asdf", "awarded_datetime": "2020-05-12:00:00" }  |

Scenario Outline: POST /awards; Too Many Awards
    When I make a POST <endpoint> request with body <body>
    When I make another POST <endpoint> request with body <body>
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>
    Then I clean up my POST to awards

    Examples: 
        | endpoint           | status_code | keys      | field       | message | body  |  
        | awards/no-email    | 400         | errors    | type        | there is already an award of type 'week' between 2022-05-09 00:00:00 and 2022-05-16 00:00:00 | { "authorizing_user_id": 2, "receiving_user_id": 1, "type": "week", "awarded_datetime": "2022-05-12 00:00:00" }  |
        | awards/no-email    | 400         | errors    | type        | there is already an award of type 'month' between 2022-05-01 00:00:00 and 2022-06-01 00:00:00 | { "authorizing_user_id": 2, "receiving_user_id": 1, "type": "month", "awarded_datetime": "2022-05-12 00:00:00" }  |

Scenario Outline: DELETE /awards
    When I make a DELETE <endpoint> request
    Then I get a status code of <status_code>
    Then the result has keys <keys>
    Then the result field is <field>
    Then the result message is <message>

    Examples: 
        | endpoint      | status_code | keys      | field    | message                 | 
        | awards/3      | 400         | errors    | award_id | award_id does not exist |
        


