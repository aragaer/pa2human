# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Server can now listen to TCP socket.
- Dockerfile

## [0.2.0] - 2018-11-04
### Added
- 'dont-understand' phrase
- 'good morning' phrase

### Changed
- RiveScript is now used instead of hardcoded replies
- Using yet-another-io-channels-library instead of Twisted

### Fixed
- Fixed the code to work on python 3.4

## 0.1.0 - 2018-08-22
### Added
- readme
- license
- This changelog
- requirements.txt and requirements-dev.txt
- --socket argument to specify which socket should be created
- initial implementation of translation service

[Unreleased]: https://github.com/aragaer/pa2human/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/aragaer/pa2human/compare/v0.1.0...v0.2.0
