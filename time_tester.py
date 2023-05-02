import time
from raw_data_extraction.data_extraction_helper import read_binary_file
from signal_processing.feature_processing import get_approximate_entropy, get_root_mean_square


signal = read_binary_file("s01.dat")
signal = signal["data"][0][0]

start = time.time()

x = get_approximate_entropy(signal)
# x = get_root_mean_square(signal)
end = time.time()
print(end - start) 