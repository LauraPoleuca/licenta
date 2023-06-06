class Discretizer:

    def __init__(self, bin_count: int) -> None:
        self.bin_count: int = bin_count

    def get_bin_index(self, lower_bound: float, upper_bound: float, value: float):
        bin_width: float = upper_bound - lower_bound
        bin_index: float = int((value - lower_bound) // bin_width)
        bin_index: float = bin_index - 1 if bin_index == self.bin_count else bin_index
        return bin_index