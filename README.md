# Dissononce

Dissononce is a python implementation for Noise Protocol Framework. It's intended that the implementation is to 
resemble definitions and Pseudo code mentioned in the original spec as close as possible. Code should be simple, easy 
to read and understand, but hopefully also flexible enough to easily adopt future changes to Noise specifications.

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Functions](#crypto-functions)
  - [Processing](#processing)
  - [HandshakePattern](#handshakepattern)
  - [Modifiers](#modifiers)
  - [Extras](#extras)
    - [Crypto functions by name](#functions-by-name)
    - [Noise Protocol by name](#noise-protocols-by-name)
    - [GuardedHandshakeState](#guardedhandshakestate)
    - [SwitchableHandshakeState](#switchablehandshakestate)
    - [NoGenDH](#nogendh)
- [Testing](#testing)
- [Logging](#logging)
- [Appendix](#appendix)

## Requirements

- python2.5-3.x
- cryptography

## Installation

## Usage

### Crypto Functions

instantiate:

```python
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.hash.sha256 import SHA256Hash

cipher = AESGCMCipher()
dh = X25519DH()
hash = SHA256Hash()
```

### Processing

Bootstrap by composition.  

```python
from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.processing.impl.symmetricstate import SymmetricState
from dissononce.processing.impl.cipherstate import CipherState
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.hash.sha256 import SHA256Hash


handshakestate = HandshakeState(
    SymmetricState(
        CipherState(
            AESGCMCipher()
        ),
        SHA256Hash()
    ),
    X25519DH()
)
```

### HandshakePattern

The ```HandshakePattern``` class allows authoring of patterns with a simple syntax, similar to how patterns are 
described in Noise spec.

- Although it's common practice for tokens to be declared somewhere as constants and imported for use, 
I think ```'ee'``` is cleaner and simpler than to import and use ```TOKEN_EE``` from somewhere.
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


### Modifiers

A modifier accepts a HandshakePattern and creates a new one with a modified name, and a modified set of message and 
premessage patterns

Fallback


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


PSK

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

As usual, the modified pattern can also be used to initialize a HandshakeState:
```python

handshakestate.initialize(
    handshake_pattern=nn_psk02,
    initiator=True,
    prologue=b'',
    psks=(psk0, psk2)
)

```

### Extras

Class and functions that are not part of Noise Protocol specification, but are part of this implementation are referred
to as "Extras'. Examples for Extras are helpers, classes that simplify usage of the library or wrappers that enforce
some rules. Extras should are to be decoupled as much as possible from the base spec implementation, they should not
interfere with the base implementation flow or introduce conflicts with Noise specification.

#### meta: Instantiate functions by name:

```python
from dissononce.extras.meta.hash.factory import HashFactory
from dissononce.extras.meta.dh.factory import DHFactory
from dissononce.extras.meta.cipher.factory import CipherFactory


cipher = CipherFactory().get_cipher('AESGCM')
hash = HashFactory().get_hash('SHA256')
dh = DHFactory().get_dh('25519')

```

#### meta: Instantiate Protocol by name:

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

GuardedHandshakeState wraps a HandshakeState and enforces that ```initialize```, ```read_message```, 
```write_message``` are executed in correct sequence depending on the given ```HandshakePattern```.

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

SwitchableHandshakeState facilitates transforming an ongoing Handshake into using a different pattern. Given then new
```HandshakePattern```, it analyses the required initiator and responder pre-keys, and maintains them across the 
transformation for use in the new Handshake. This is typically used for example when doing an IK then falling back to 
XX, where  ```re``` is to be used as prekey in ```XXfallback```.


#### dh: NoGenDH

```python
from dissononce.extras.dh.dh_nogen import NoGenDH
from dissononce.dh.x25519.x25519 import X25519DH

nogenX25515 = NoGenDH(X25519DH(), X25519DH().generate_keypair().private)

```

A ```NoGenDH``` wraps an existing ```DH``` object, but disables keypairs generation functionality by fixing all 
generated  keypairs to a single value determined by the```PrivateKey``` passed to it at construction. 
This is used in tests where ephemeral values from test vectors must be used.


## Example


## Testing

Vectors, Tox

## Logging

- doc Logging

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
- [mailing list](https://moderncrypto.org/mail-archive/noise/)
- [noiseprotocol for python3](https://github.com/plizonczyk/noiseprotocol)
- [noise-java](https://github.com/rweather/noise-java)
