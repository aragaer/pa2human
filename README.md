# pa2human

Service that can translate text between human and bot.

## Usage

To start the service run `pa2human.py --socket path/to/socket`. The
`--socket` argument is mandatory. UNIX socket will be created which
can be used to communicate to the service.

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

#### PA-to-Human

If message contains `intent` field the service treats it as a
bot-generated response and attemts to produce a human-readable
text. The response will have the following format: `{"text":
TRANSLATION}`

#### Error

If message is a valid JSON but has neither `text` nor `intent` fields
the result is error. The response will have the following format:
`{"error": ERROR}`
