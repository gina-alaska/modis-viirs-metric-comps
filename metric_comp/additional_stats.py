import numpy as np

# Extra Statistics Functions!


def calc_non_zero_mean(np_array):
    np_array_non_zero = np_array[np_array > 0]
    return round(np.mean(np_array_non_zero), 4)


def calc_non_zero_max(np_array):
    np_array_non_zero = np_array[np_array > 0]
    return np.max(np_array_non_zero)


def calc_non_zero_min(np_array):
    np_array_non_zero = np_array[np_array > 0]
    return np.min(np_array_non_zero)


def calc_std_dev(np_array):
    degrees_of_freedom = 1
    return round(np.std(np_array, ddof=degrees_of_freedom), 4)


def calc_non_zero_std_dev(np_array):
    degrees_of_freedom = 1
    np_array = np_array[np_array > 0]
    return round(np.std(np_array, ddof=degrees_of_freedom), 4)


'''
def calc_median(np_array):
    return np.median(np_array)

def calc_non_zero_median(np_array):
    np_array_non_zero = np_array[np_array > 0]
    return np.median(np_array_non_zero)
'''

additional_statistics_functions = {
    'non_zero_mean': calc_non_zero_mean,
    'non_zero_max': calc_non_zero_max,
    'non_zero_min': calc_non_zero_min,
    'std_dev': calc_std_dev,
    'non_zero_std_dev': calc_non_zero_std_dev
    # 'median': calc_median,
    # 'non_zero_median': calc_non_zero_median
}
