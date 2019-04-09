# Dissononce

Dissononce is a python implementation for Noise Protocol Framework. It's intended that the implementation is to 
resemble definitions and Pseudo code mentioned in the original spec as close as possible. Code should be simple, easy 
to read and understand, but hopefully also flexible enough to easily adopt future changes to Noise specifications.

## Requirements

- python2.5-3.x
- cryptography

## Supported specs

Revision 34

### Cipher functions

- AESGCM
- ChaChaPoly
 
### Hash functions

- Blake2b
- Blake2s
- SHA256
- SHA512

### DH functions

- x448
- x25519

### Handshake Patterns

Interactive

- IK, IN, IX
- KK, KN, KX
- NK, NN, NX
- XK, XN, XX

Oneway

- K, N, X

Deferred

- I1K, I1K1, I1N, I1X, I1X1, IK1, IX1
- K1K, K1K1, K1N, K1X, K1X1, KK1, KX1
- NK1, NX1
- X1K, X1K1, X1N, X1X, X1X1, XK1, XX1

### Modifiers

- fallback
- pskX

## Installation

## Usage

### Functions

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

HandshakePattern allows authoring of patterns with a simple syntax, similar to how patterns are described in Noise spec.

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

- meta
- GuardedHandshakeState
- SwitchableHandshakeState
- dh.create_public



#### Instantiate functions by name:

```python
from dissononce.extras.meta.hash.factory import HashFactory
from dissononce.extras.meta.dh.factory import DHFactory
from dissononce.extras.meta.cipher.factory import CipherFactory


cipher = CipherFactory().get_cipher('AESGCM')
hash = HashFactory().get_hash('SHA256')
dh = DHFactory().get_dh('25519')

```

#### Instantiate Protocol by name:

```python
from dissononce.extras.meta.protocol.factory import NoiseProtocolFactory

protocol = NoiseProtocolFactory().get_noise_protocol('Noise_XX_25519_AESGCM_SHA256')
handshakestate = protocol.create_handshakestate()

```

#### GuardedHandshakeState (Extras)

#### SwitchableHandshakeState (Extras)

## Example


## Testing

Vectors, Tox

## Logging

- doc Logging

## References

- noise spec
- mailing list
- noise python
- noise java

