Feature: Hello
  As a PA user
  I want my PA to be able to understand and say hello
  So that it feels more human
  
  Background:
    Given the service is started
      And brain is connected

  Scenario: Human says hello
     When brain asks to translate "Привет" from human
     Then the result is intent "hello"


  Scenario: PA says hello
     When brain asks to translate "hello" to human
     Then the result is text "Ой, приветик!"
