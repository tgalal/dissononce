# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project (kinda) adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.34.3] - 2019-04-24

### Changed

- Fix GuardedhandshakeState might throw an error on py2 if future is installed
- Depend on cryptography>=2.5 instead of cryptography

## [0.34.2] - 2019-04-17

### Changed

- Relocate experimental and dangerous packages to extras
- Move stable algorithms out of stable package as the package is now redundant

## [0.34.1] - 2019-04-17

### Added

- Namespace crypto alg according to support
- PrivateKey for each DH for consistency

### Changed

- Fix responder handshake hash not being checked in vectors tests
- Move pattern examples from examples/ to examples/patterns/
- Move implementations under dh to dh/stable/
- Move implementations under cipher to cipher/stable/
- Move implementations under hash to hash/stable/

## [0.34.0] - 2019-04-15
```
noise revision: 34
requires:
- python2.5-3.x
- cryptography
uses:
- transitions
```
