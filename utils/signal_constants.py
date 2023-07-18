from enum import Enum

CHANNEL_INDEXES = {
    'Fp1': 1,
    'F3': 3,
    'F7': 4,
    'C3': 7,
    'T7': 8,
    'P3': 11,
    'P7': 12,
    'PO3': 13,
    'O1': 14,
    'Pz': 16,
    'Fp2': 17,
    'F4': 20,
    'F8': 21,
    'Cz': 24,
    'C4': 25,
    'T8': 26,
    'P4': 29,
    'P8': 30,
    'PO4': 31,
    'O2': 32
}

SAMPLING_RATE = 128
FILTER_ORDER = 5
SAMPLING_LOWER_BOUND = SAMPLING_RATE * 10
SAMPLING_HIGHER_BOUND = SAMPLING_RATE * 16

class BandEnum(Enum):
    ALPHA = 1,
    BETA = 2,
    GAMMA = 3


class BandType:
    def __init__(self, band_enum: BandEnum, low_frequency: float, high_frequency: float) -> None:
        self.enum_type = band_enum
        self.low_frequency = low_frequency
        self.high_frequency = high_frequency


ALPHA_BAND_TYPE = BandType(BandEnum.ALPHA, 7.5, 12.5)
BETA_BAND_TYPE = BandType(BandEnum.BETA, 13.0, 30.0)
GAMMA_BAND_TYPE = BandType(BandEnum.GAMMA, 30.0, 63.5)
