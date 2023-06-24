import numpy as np
from typing import List

from utils.signal_constants import BandType


class InputModel:

    # ca si chestie, mi am dat seama ca faptul ca probabilitatea
    # pentru clasare nu ar trebui sa conteze. din cauza ca avem chestia aia
    # P(xi|Ck), probabilitatea de a fi o anumita valoare nu depinde de clasa Ck
    # la fel si banda de semnal.
    def __init__(self, ae: float, se: float, psd: float, rms: float, corr: float, outcome: str, band: BandType) -> None:
        self.ae: float = ae
        self.se: float = se
        self.psd: float = psd
        self.rms: float = rms
        self.corr: float = corr
        self.outcome: str = outcome
        self.band = band

    @classmethod
    def from_list(cls, feature_list: List, outcome: str, band: BandType):
        return cls(feature_list[0], feature_list[1], feature_list[2], feature_list[3], feature_list[4], outcome, band)
    
    def get_feature_list(self):
        return np.array([self.ae, self.se, self.psd, self.rms, self.corr])
    
    def get_feature_sublist(self):
        return np.array([self.ae, self.psd, self.rms])