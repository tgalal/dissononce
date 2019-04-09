from dissononce.processing.modifiers.psk import PSKPatternModifier
from dissononce.processing.modifiers.fallback import FallbackPatternModifier


NAME_MODIFIER_psk0 = 'psk0'
NAME_MODIFIER_psk1 = 'psk1'
NAME_MODIFIER_psk2 = 'psk2'
NAME_MODIFIER_psk3 = 'psk3'
NAME_MODIFIER_FALLBACK = 'fallback'


MAP_MODIFIER = {
    NAME_MODIFIER_psk0: lambda: PSKPatternModifier(0),
    NAME_MODIFIER_psk1: lambda: PSKPatternModifier(1),
    NAME_MODIFIER_psk2: lambda: PSKPatternModifier(2),
    NAME_MODIFIER_psk3: lambda: PSKPatternModifier(3),
    NAME_MODIFIER_FALLBACK: FallbackPatternModifier
}
