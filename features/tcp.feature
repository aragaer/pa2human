Feature: Socket
  As a PA administrator
  I want pa2human to listen to TCP socket
  So that other PA components could use it across network

  Scenario: Start
     When I start pa2human with tcp socket
     Then pa2human prints that it is listening
      And the socket accepts connections

  Scenario: Multiple connections
     When I start pa2human with tcp socket
     Then pa2human prints that it is listening
      And the socket accepts a connection
      And the socket accepts another connection
