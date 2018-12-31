Feature: Socket
  As a PA administrator
  I want pa2human to correctly create the socket
  So that other PA components could use it

  Scenario: Start
    Given I have a socket path to use
     When I start pa2human with that path
     Then the socket appears
      And the socket accepts connections

  Scenario: Multiple connections
    Given I have a socket path to use
     When I start pa2human with that path
      And I wait for socket to appear
     Then the socket accepts a connection
      And the socket accepts another connection

  Scenario: Stop
    Given I have a socket path to use
     When I start pa2human with that path
      And I wait for socket to appear
      And I stop pa2human
     Then the socket doesn't exist
