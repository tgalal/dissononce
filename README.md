# Dissononce 

[![Build Status](https://travis-ci.org/tgalal/dissononce.svg?branch=master)](https://travis-ci.org/tgalal/dissononce)
[![PyPI](https://img.shields.io/pypi/v/dissononce.svg)](https://pypi.python.org/pypi/dissononce)

Dissononce is a python implementation for [Noise Protocol Framework](https://noiseprotocol.org/).
A main goal of this project is to provide a simple, easy to read and understand practical reference for
Noise enthusiasts, implementers and users. Therefore this project attempts to stick to the following guidelines:

- Syntax that resembles as closely as possible definitions and pseudo code mentioned in Noise Specs.
- As minimal python "magic" as possible (explicit is better than implicit).
- Code that is simple, easy to read, follow and understand.
- Flexibility to easily adopt future changes to Noise specifications.
- Deviations from Noise Specs (additions, opinionated specs and API changes..etc) are isolated from original
implementation/API and are optional to use.
- Deviations from Noise Specs do not influence adjustments to original implementation/API that conflict with Noise Specs.

## META-INF
```
dissononce version: 0.34.0
noise revision: 34
released: 2019-04-13
requires:
- python>=2.5,<=3.7
- cryptography==2.6.1
uses:
- transitions==0.6.9
```

## Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Crypto Functions](#crypto-functions)
  - [Processing](#processing)
  - [Handshake Patterns](#handshake-patterns)
  - [Modifiers](#modifiers)
  - [Extras](#extras)
    - [Crypto functions by name](#meta-crypto-functions-by-name)
    - [Noise Protocol by name](#meta-noise-protocols-by-name)
    - [GuardedHandshakeState](#processing-guardedhandshakestate)
    - [SwitchableHandshakeState](#processing-switchablehandshakestate)
    - [NoGenDH](#nogendh)
- [Examples](#examples)
- [Testing](#testing)
- [Logging](#logging)
- [Appendix](#appendix)


## Installation

From source:

```
python setup.py install
```
Using Pip:
```
pip install dissononce
```

## Usage

### Crypto Functions

Each set of Crypto functions (DH, Cipher, Hash) is enclosed inside an own base class, where an implementation subclasses
that base class to implement the methods.

- DH-functions base class: ```dissononce.dh.dh.DH```
- Cipher-functions base class: ```dissononce.cipher.cipher.Cipher```
- Hash-functions base class: ```dissononce.hash.hash.Hash```

Example instantiating objects for X25519 ```DH```, AESGCM ```Cipher``` and SHA256 ```Hash```:

```python
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.hash.sha256 import SHA256Hash

cipher = AESGCMCipher()
dh = X25519DH()
hash = SHA256Hash()
```

See [Appendix](#appendix) for other Crypto functions.

### Processing

```HandshakeState```, ```SymmetricState``` and ```CipherState``` should ideally be constructed in a composition-manner,
where Crypto-functions dependencies are also to be instantiated before passing them to their dependants.

- A ```CipherState``` requires a ```Cipher``` object
- A ```SymmetricState``` requires a ```CipherState``` and a ```Hash``` object.
- A ```HandshakeState``` requires a ```SymmetricState``` and a ```DH``` object.

```python
from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.processing.impl.symmetricstate import SymmetricState
from dissononce.processing.impl.cipherstate import CipherState
from dissononce.cipher.chachapoly import ChaChaPolyCipher
from dissononce.dh.x448.x448 import X448DH
from dissononce.hash.sha512 import SHA512Hash


handshakestate = HandshakeState(
    SymmetricState(
        CipherState(
            ChaChaPolyCipher()
        ),
        SHA512Hash()
    ),
    X448DH()
)
```

See [Extras](#extras) for alternative methods of construction.

### Handshake Patterns

The ```HandshakePattern``` class allows authoring of patterns using a simple syntax, similar to how patterns are
described in Noise spec.

- message_patterns is a tuple/list of tuples of token(s).
- initiator_pre_messages is a tuple of tokens
- responder_pre_message_pattern is a tuple of tokens

```python
from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern

k1k1 = HandshakePattern(
      name='K1K1',
      initiator_pre_messages=('s',),
      responder_pre_message_pattern=('s',),
      message_patterns=(
          ('e',),
          ('e', 'ee', 'es'),
          ('se',)
    )
)

print(k1k1)

```
```
K1K1:
  -> s
  <- s
  ...
  -> e
  <- e, ee, es
  -> se
```

See [Appendix](#appendix) for already defined Handshake Patterns.

### Modifiers

A ```Modifier``` accepts a ```HandshakePattern``` and creates a new one with a modified name, and a modified set of
message and premessage patterns

**Fallback**


```python
from dissononce.processing.modifiers.fallback import FallbackPatternModifier
from dissononce.processing.handshakepatterns.interactive.XX import XXHandshakePattern


xx = XXHandshakePattern()
xx_fallback = FallbackPatternModifier().modify(xx)
print(xx_fallback)
```
```
XXfallback:
  -> e
  ...
  <- e, ee, s, es
  -> s, se
```


**PSK**

```python
from dissononce.processing.modifiers.psk import PSKPatternModifier
from dissononce.processing.handshakepatterns.interactive.NN import NNHandshakePattern


nn = NNHandshakePattern()
nn_psk0 = PSKPatternModifier(0).modify(nn)
nn_psk02 = PSKPatternModifier(2).modify(nn_psk0)
print(nn_psk02)

```
```
NNpsk0+psk2:
  -> psk, e
  <- e, ee, psk

```

As usual, the modified ```HandshakePattern``` is used to (re)initialize a ```HandshakeState```:
```python

handshakestate.initialize(
    handshake_pattern=nn_psk02,
    initiator=True,
    prologue=b'',
    psks=(psk0, psk2)
)

```

### Extras

Classes and functions that are not part of Noise Protocol specification but are part of this implementation are referred
to as "Extras" or "Deviations". Examples for Extras are helpers, classes that simplify usage of the library or wrappers
that enforce some rules or design patterns. Extras should be decoupled as much as possible from the base spec
implementation and never referenced from there.

#### meta: Crypto-functions by name:

As an alternative to directly instantiating the Crypto-functions objects, they could also be created by name using
a factory designated to each type of Crypto-functions:

```python
from dissononce.extras.meta.hash.factory import HashFactory
from dissononce.extras.meta.dh.factory import DHFactory
from dissononce.extras.meta.cipher.factory import CipherFactory


cipher = CipherFactory().get_cipher('AESGCM')
hash = HashFactory().get_hash('SHA256')
dh = DHFactory().get_dh('25519')

```

#### meta: Protocol by name:

A Noise Protocol, that is:

- DH, Cipher, Hash instance
- CipherState instance
- SymmetricState instance
- HandshakeState instance
- HandshakePattern

can be created by name. Use ```NoiseProtocolFactory``` to get a a ```NoiseProtocol``` instance which encloses
instances of ```DH```, ```Cipher```, ```Hash```, ```HandshakePattern```, and exposes methods for creating
```CipherState```, ```SymmetricState```, and ```HandshakeState```.

```python
from dissononce.extras.meta.protocol.factory import NoiseProtocolFactory

protocol = NoiseProtocolFactory().get_noise_protocol('Noise_XX_25519_AESGCM_SHA256')
handshakestate = protocol.create_handshakestate()

```

#### processing: GuardedHandshakeState

```python
from dissononce.extras.processing.handshakestate_guarded import GuardedHandshakeState

guarded = GuardedHandshakeState(handshakestate)
guarded.read_message(b'', bytearray())

```
```
> AssertionError: Cannot read_message while in initialize phase.
```

```GuardedHandshakeState``` wraps an existing ```HandshakeState``` to enforce a correct flow of the handshake process.
This includes making sure the ```HandshakeState``` is initialized before usage, and that the flow order of
```write_message``` and ```read_message``` invocations match the ```HandshakePattern``` being used. A violation will
result in an AssertionError getting raised.

#### processing: SwitchableHandshakeState

```python
from dissononce.extras.processing.handshakestate_switchable import SwitchableHandshakeState
from dissononce.processing.handshakepatterns.interactive.XX import XXHandshakePattern
from dissononce.processing.modifiers.fallback import FallbackPatternModifier
from dissononce.extras.meta.protocol.factory import NoiseProtocolFactory

protocol = NoiseProtocolFactory().get_noise_protocol('Noise_IK_25519_AESGCM_SHA256')
switchable = SwitchableHandshakeState(protocol.create_handshakestate())

## Begin IK, then fallback to XX if necessary using:

switchable.switch(
    handshake_pattern=FallbackPatternModifier().modify(XXHandshakePattern()),
    initiator=True,
    prologue=b''
)

```

```SwitchableHandshakeState``` facilitates transforming an ongoing Handshake into using a different pattern. Given
the new```HandshakePattern```, it analyses the required initiator and responder pre-messages, and maintains them
across the transformation for use in the new Handshake. This is typically used for example when doing
a ```IK``` handshake then switching to ```XXfallback``` where  ```re``` is to be used as a initiator pre-message.

#### dh: NoGenDH

```python
from dissononce.extras.dh.dh_nogen import NoGenDH
from dissononce.dh.x25519.x25519 import X25519DH

nogenX25515 = NoGenDH(X25519DH(), X25519DH().generate_keypair().private)

```

A ```NoGenDH``` wraps an existing ```DH``` object, but disables keypairs generation functionality by fixing all 
generated  keypairs to a single value determined by the```PrivateKey``` passed to it at construction. 
This is used in tests where ephemeral values from test vectors must be used.

## Examples

Inside [examples](examples) directory there are examples for some Noise protocols carrying out a handshake and
transporting some messages for demonstration.

## Testing

### Test Vectors

Vectors used for testing are found under test/vectors. The data is of JSON type, and is formatted according
to [Noise Test Vectors Specification](https://github.com/noiseprotocol/noise_wiki/wiki/Test-vectors). At the moment
there are 2 Test Vectors files:

- Tests Vectors from [cacophony](https://github.com/centromere/cacophony) under [tests/vectors/cacophony.txt](tests/vectors/cacophony.txt)
- Test Vectors from [snow](https://github.com/mcginty/snow) under [tests/vectors/snow.txt](tests/vectors/snow.txt)

## Logging

Enable debug-level logging for a detailed insight of a handshake process. The debug output syntax and formatting is 
intended to be as close as possible to the language used in Noise specs. This might be useful for when using dissononce 
as a reference implementation where one wants to understand what's going on internally and to easily relate to
Noise specs.

```
>>> import dissononce, logging
>>> dissononce.logger.setLevel(logging.DEBUG)
>>> handshakestate.initialize(XXHandshakePattern(), True, b'', X448DH().generate_keypair())

I dissononce.processing.impl.handshakestate - Derived Noise Protocol name Noise_XX_448_ChaChaPoly_SHA512
XX:
  -> e
  <- e, ee, s, es
  -> s, se

>>> handshakestate.write_message(b'',bytearray())

I dissononce.processing.impl.handshakestate - WriteMessage(payload, message_buffer)
D dissononce.processing.impl.handshakestate -     Processing token 'e'
D dissononce.processing.impl.handshakestate -         e=GENERATE_KEYPAIR()
D dissononce.processing.impl.handshakestate -         message_buffer.append(e.public_key)
D dissononce.processing.impl.handshakestate -         MixHash(e.public_key)
D dissononce.processing.impl.handshakestate -     buffer.append(EncryptAndHash(payload))
```

## Appendix

### Cipher functions

- [AESGCM](dissononce/cipher/aesgcm.py)
- [ChaChaPoly](dissononce/cipher/chachapoly.py)
 
### Hash functions

- [Blake2b](dissononce/hash/blake2b.py)
- [Blake2s](dissononce/hash/blake2s.py)
- [SHA256](dissononce/hash/sha256.py)
- [SHA512](dissononce/hash/sha512.py)

### DH functions

- [x448](dissononce/dh/x448/x448.py)
- [x25519](dissononce/dh/x25519/x25519.py)

### Handshake Patterns

Interactive:

- [IK](dissononce/processing/handshakepatterns/interactive/IK.py), [IN](dissononce/processing/handshakepatterns/interactive/IN.py), [IX](dissononce/processing/handshakepatterns/interactive/IX.py)
- [KK](dissononce/processing/handshakepatterns/interactive/KK.py), [KN](dissononce/processing/handshakepatterns/interactive/KN.py), [KX](dissononce/processing/handshakepatterns/interactive/KX.py)
- [NK](dissononce/processing/handshakepatterns/interactive/NK.py), [NN](dissononce/processing/handshakepatterns/interactive/NN.py), [NX](dissononce/processing/handshakepatterns/interactive/NX.py)
- [XK](dissononce/processing/handshakepatterns/interactive/XK.py), [XN](dissononce/processing/handshakepatterns/interactive/XN.py), [XX](dissononce/processing/handshakepatterns/interactive/XX.py)

Oneway:

- [K](dissononce/processing/handshakepatterns/oneway/K.py), [N](dissononce/processing/handshakepatterns/oneway/N.py), [X](dissononce/processing/handshakepatterns/oneway/X.py)

Deferred:

- [I1K](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/I1K.py), 
[I1K1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/I1K1.py), 
[I1N](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/I1N.py),
[I1X](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/I1X.py), 
[I1X1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/I1X1.py), 
[IK1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/IK1.py), 
[IX1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/IX1.py)
- [K1K](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/K1K.py), 
[K1K1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/K1K1.py), 
[K1N](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/K1N.py), 
[K1X](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/K1X.py), 
[K1X1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/K1X1.py), 
[KK1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/KK1.py), 
[KX1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/KX1.py)
- [NK1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/NK1.py), 
[NX1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/NX1.py)
- [X1K](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/X1K.py), 
[X1K1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/X1K1.py), 
[X1N](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/X1N.py), 
[X1X](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/X1X.py), 
[X1X1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/X1X1.py), 
[XK1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/XK1.py), 
[XX1](https://github.com/tgalal/dissononce/blob/master/dissononce/processing/handshakepatterns/deferred/XX1.py)

### Modifiers

- [fallback](dissononce/processing/modifiers/fallback.py)
- [psk](dissononce/processing/modifiers/psk.py)

## References

- [noise specs revision 34](https://github.com/noiseprotocol/noise_spec/releases/tag/v34)
- [noise mailing list](https://moderncrypto.org/mail-archive/noise/)
- [noiseprotocol for python3](https://github.com/plizonczyk/noiseprotocol)
- [noise-java](https://github.com/rweather/noise-java)
