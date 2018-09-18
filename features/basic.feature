Feature: Basic communication
  As a PA user
  I want my PA to be able to use human speech
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

  Scenario: PA doesn't understand
     When brain asks to translate "dont-understand" to human
     Then the result is text "Я не поняла, что ты сказал"
