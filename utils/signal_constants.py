from enum import Enum

CHANNEL_INDEXES = {
    "Fp1": 1,
    'AF3': 2,
    'F3': 3,
    'F7': 4,
    'FC5': 5,
    'FC1': 6,
    'C3': 7,
    'T7': 8,
    'CP5': 9,
    'CP1': 10,
    'P3': 11,
    'P7': 12,
    'PO3': 13,
    'O1': 14,
    'Oz': 15,
    'Pz': 16,
    'Fp2': 17,
    'AF4': 18,
    'Fz': 19,
    'F4': 20,
    'F8': 21,
    'FC6': 22,
    'FC2': 23,
    'Cz': 24,
    'C4': 25,
    'T8': 26,
    'CP6': 27,
    'CP2': 28,
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
