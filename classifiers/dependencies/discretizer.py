class Discretizer:

    def __init__(self, bin_count: int) -> None:
        self.bin_count: int = bin_count

    def get_bin_index(self, lower_bound: float, upper_bound: float, value: float) -> int:
        bin_width: float = (upper_bound - lower_bound) / self.bin_count
        bin_index: int = int((value - lower_bound) // bin_width)
        bin_index: int = bin_index - 1 if bin_index == self.bin_count else bin_index
        return bin_index
