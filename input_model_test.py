class InputModel:

    # ca si chestie, mi am dat seama ca faptul ca probabilitatea
    # pentru clasare nu ar trebui sa conteze. din cauza ca avem chestia aia
    # P(xi|Ck), probabilitatea de a fi o anumita valoare nu depinde de clasa Ck
    # la fel si banda de semnal.
    def __init__(self, ae: float, se: float, psd: float, rms: float, corr: float, outcome: str) -> None:
        self.ae: float = ae
        self.se: float = se
        self.psd: float = psd
        self.rms: float = rms
        self.corr: float = corr
        self.outcome: str = outcome
