# pa2human [![Build Status](https://travis-ci.org/aragaer/pa2human.svg?branch=master)](https://travis-ci.org/aragaer/pa2human) [![codecov](https://codecov.io/gh/aragaer/pa2human/branch/master/graph/badge.svg)](https://codecov.io/gh/aragaer/pa2human) [![BCH compliance](https://bettercodehub.com/edge/badge/aragaer/pa2human?branch=master)](https://bettercodehub.com/)

Service that can translate text between human and bot.

## Usage

The service can listen to either TCP or UNIX socket.

`pa2human.py --socket host:port`
`pa2human.py --socket path/to/socket`

The service looks for colon (`:`) in the argument. It might break if
path to UNIX socket contains a colon.

### Protocol

Each message must be in one line, ending with newline. If message is
not a valid JSON, service silently closes the connection.

Message must contain either `text` or `intent` field. If neither is
present the service returns an error message. If both are present,
`intent` is ignored.

#### Human-to-PA

If message contains `text` field the service treats it as a
human-entered command and attempts to translate it to intent. The
response will have the following format: `{"intent": INTENT}`

Translation files from human to PA are located in pa2human directory.

#### PA-to-Human

If message contains `intent` field the service treats it as a
bot-generated response and attemts to produce a human-readable
text. The response will have the following format: `{"text":
TRANSLATION}`

Translation files from human to PA are located in human2pa directory.

#### Error

If message is a valid JSON but has neither `text` nor `intent` fields
the result is error. The response will have the following format:
`{"error": ERROR}`
