from dissononce.processing.handshakepatterns.oneway.N import NHandshakePattern
from dissononce.processing.handshakepatterns.interactive.NN import NNHandshakePattern
from dissononce.processing.handshakepatterns.interactive.NK import NKHandshakePattern
from dissononce.processing.handshakepatterns.interactive.NX import NXHandshakePattern

from dissononce.processing.handshakepatterns.oneway.K import KHandshakePattern
from dissononce.processing.handshakepatterns.interactive.KN import KNHandshakePattern
from dissononce.processing.handshakepatterns.interactive.KK import KKHandshakePattern
from dissononce.processing.handshakepatterns.interactive.KX import KXHandshakePattern

from dissononce.processing.handshakepatterns.oneway.X import XHandshakePattern
from dissononce.processing.handshakepatterns.interactive.XN import XNHandshakePattern
from dissononce.processing.handshakepatterns.interactive.XK import XKHandshakePattern
from dissononce.processing.handshakepatterns.interactive.XX import XXHandshakePattern

from dissononce.processing.handshakepatterns.interactive.IN import INHandshakePattern
from dissononce.processing.handshakepatterns.interactive.IK import IKHandshakePattern
from dissononce.processing.handshakepatterns.interactive.IX import IXHandshakePattern

from dissononce.processing.handshakepatterns.deferred.NK1 import NK1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.NX1 import NX1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.X1N import X1NHandshakePattern
from dissononce.processing.handshakepatterns.deferred.X1K import X1KHandshakePattern
from dissononce.processing.handshakepatterns.deferred.XK1 import XK1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.X1K1 import X1K1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.X1X import X1XHandshakePattern
from dissononce.processing.handshakepatterns.deferred.XX1 import XX1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.X1X1 import X1X1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.K1N import K1NHandshakePattern
from dissononce.processing.handshakepatterns.deferred.K1K import K1KHandshakePattern
from dissononce.processing.handshakepatterns.deferred.KK1 import KK1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.K1K1 import K1K1HandshakePattern

from dissononce.processing.handshakepatterns.deferred.K1X import K1XHandshakePattern
from dissononce.processing.handshakepatterns.deferred.KX1 import KX1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.K1X1 import K1X1HandshakePattern

from dissononce.processing.handshakepatterns.deferred.I1N import I1NHandshakePattern
from dissononce.processing.handshakepatterns.deferred.I1K import I1KHandshakePattern
from dissononce.processing.handshakepatterns.deferred.IK1 import IK1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.I1K1 import I1K1HandshakePattern


from dissononce.processing.handshakepatterns.deferred.I1X import I1XHandshakePattern
from dissononce.processing.handshakepatterns.deferred.IX1 import IX1HandshakePattern
from dissononce.processing.handshakepatterns.deferred.I1X1 import I1X1HandshakePattern


NAME_PATTERN_N = 'N'
NAME_PATTERN_K = 'K'
NAME_PATTERN_X = 'X'

NAME_PATTERN_NN = 'NN'
NAME_PATTERN_NK = 'NK'
NAME_PATTERN_NX = 'NX'
NAME_PATTERN_XN = 'XN'
NAME_PATTERN_XK = 'XK'
NAME_PATTERN_XX = 'XX'
NAME_PATTERN_KN = 'KN'
NAME_PATTERN_KK = 'KK'
NAME_PATTERN_KX = 'KX'
NAME_PATTERN_IN = 'IN'
NAME_PATTERN_IK = 'IK'
NAME_PATTERN_IX = 'IX'
NAME_PATTERN_NK1 = 'NK1'
NAME_PATTERN_NX1 = 'NX1'
NAME_PATTERN_X1N = 'X1N'
NAME_PATTERN_X1K = 'X1K'
NAME_PATTERN_XK1 = 'XK1'
NAME_PATTERN_X1K1 = 'X1K1'
NAME_PATTERN_X1X = 'X1X'
NAME_PATTERN_XX1 = 'XX1'
NAME_PATTERN_X1X1 = 'X1X1'
NAME_PATTERN_K1N = 'K1N'
NAME_PATTERN_K1K = 'K1K'
NAME_PATTERN_KK1 = 'KK1'
NAME_PATTERN_K1K1 = 'K1K1'
NAME_PATTERN_K1X = 'K1X'
NAME_PATTERN_KX1 = 'KX1'
NAME_PATTERN_K1X1 = 'K1X1'
NAME_PATTERN_I1N = 'I1N'
NAME_PATTERN_I1K = 'I1K'
NAME_PATTERN_IK1 = 'IK1'
NAME_PATTERN_I1K1 = 'I1K1'
NAME_PATTERN_I1X = 'I1X'
NAME_PATTERN_IX1 = 'IX1'
NAME_PATTERN_I1X1 = 'I1X1'

MAP_PATTERN = {
    # interactive
    NAME_PATTERN_NN: NNHandshakePattern, NAME_PATTERN_NK: NKHandshakePattern, NAME_PATTERN_NX: NXHandshakePattern,
    NAME_PATTERN_XN: XNHandshakePattern, NAME_PATTERN_XK: XKHandshakePattern, NAME_PATTERN_XX: XXHandshakePattern,
    NAME_PATTERN_KN: KNHandshakePattern, NAME_PATTERN_KK: KKHandshakePattern, NAME_PATTERN_KX: KXHandshakePattern,
    NAME_PATTERN_IN: INHandshakePattern, NAME_PATTERN_IK: IKHandshakePattern, NAME_PATTERN_IX: IXHandshakePattern,
    # oneway
    NAME_PATTERN_N: NHandshakePattern,   NAME_PATTERN_K: KHandshakePattern,   NAME_PATTERN_X: XHandshakePattern,
    # deferred
    NAME_PATTERN_NK1: NK1HandshakePattern, NAME_PATTERN_NX1: NX1HandshakePattern,
    NAME_PATTERN_X1N: X1NHandshakePattern, NAME_PATTERN_X1K: X1KHandshakePattern,
    NAME_PATTERN_XK1: XK1HandshakePattern,
    NAME_PATTERN_X1K1: X1K1HandshakePattern, NAME_PATTERN_X1X: X1XHandshakePattern,
    NAME_PATTERN_XX1: XX1HandshakePattern, NAME_PATTERN_X1X1: X1X1HandshakePattern,

    NAME_PATTERN_K1N: K1NHandshakePattern, NAME_PATTERN_K1K: K1KHandshakePattern, NAME_PATTERN_KK1: KK1HandshakePattern,
    NAME_PATTERN_K1K1: K1K1HandshakePattern, NAME_PATTERN_K1X: K1XHandshakePattern,
    NAME_PATTERN_KX1: KX1HandshakePattern, NAME_PATTERN_K1X1: K1X1HandshakePattern,

    NAME_PATTERN_I1N: I1NHandshakePattern, NAME_PATTERN_I1K: I1KHandshakePattern, NAME_PATTERN_IK1: IK1HandshakePattern,
    NAME_PATTERN_I1K1: I1K1HandshakePattern, NAME_PATTERN_I1X: I1XHandshakePattern,
    NAME_PATTERN_IX1: IX1HandshakePattern, NAME_PATTERN_I1X1: I1X1HandshakePattern
}
