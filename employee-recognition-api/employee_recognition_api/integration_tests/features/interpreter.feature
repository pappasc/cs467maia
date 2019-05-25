@interp

Feature: Integration Tests - INTERPRETER (Amazon AWS)

Scenario: POST, GET, DELETE /image, 200
    When I make an AWS POST /image/test.jpg request
    Then I get a status code of 200
    Then the result is success
    When I make an AWS GET /image/test.jpg request
    Then I get a status code of 200
    Then the result is success
    When I make an AWS DELETE /image/test.jpg request
    Then I get a status code of 200
    Then the result is success

Scenario: POST /pdf, 200
   	When I make an AWS POST /pdf request
    Then I get a status code of 200
    Then the result is a PDF

Scenario: GET /image, 400
    When I make an AWS GET /image/test.jpg request
    Then I get a status code of 400
    Then the result is failure

Scenario: POST /pdf, 400 
	When I make a bad AWS POST /pdf request
	Then I get a status code of 400 
	Then the result is empty

# DELETE doesn't have a 400 response at this time
