import numpy as np 
from numba import cuda
import numba 
import math 
import cmath


# only call non_uniform_call_cuda
# equivivalt to py_ft.ft_uneven_bulk
# all times and omegas that are not on pos 0 for each time series, will lead to erros
# this is not checked in the code to aviod slow-down
# returned value is an ndarray (2-dim), which is not cropped according to the amount of omegas
# additional space is filled with 0 (0+0j)


# times and omegas are only allowed to be 0 for the first element of each time_series
# types => values : 2d float64, times : 2d float64, omegas : 2d float64, fts : complex128, ft_sign : int, t_zeros = float64
@cuda.jit
def non_uniform_ft_cuda_no_weights(values, times, omegas, fts, ft_sign, t_zero):
    x, y = cuda.grid(2)
    if x < omegas.shape[0] and y < omegas.shape[1] and (y == 0 or omegas[x, y] != 0):
        if omegas[x, y] == 0:
            count = 1
            summe = values[x, 0]
            while count < omegas.shape[1] and times[x, count] != 0:
                summe += values[x, count]
                count += 1
            fts[x, y] = complex(summe/math.sqrt(float(count)))
        else:
            max_time = 1
            while max_time < omegas.shape[1] and times[x, max_time] != 0:
                max_time += 1
            csum = 0
            ssum = 0
            for i in range(max_time):
                csum += math.cos(2.0 * omegas[x, y] * times[x, i])
                ssum += math.sin(2.0 * omegas[x, y] * times[x, i])
            tau = 0.5 * math.atan2(ssum, csum)

            sumr = 0
            sumi = 0
            scos2 = 0
            ssin2 = 0

            for i in range(max_time):
                sumr += values[x, i] * math.cos(omegas[x, y] * times[x, i] - tau)
                sumi += values[x, i] * math.sin(omegas[x, y] * times[x, i] - tau)
                scos2 += math.pow(math.cos(omegas[x, y] * times[x, i] - tau), 2)
                ssin2 += math.pow(math.sin(omegas[x, y] * times[x, i] - tau), 2)

            ft_real = sumr / (math.sqrt(2.0) * math.sqrt(scos2))
            ft_imag = ft_sign * sumi / (math.sqrt(2.0) * math.sqrt(ssin2))
            phi_this = tau - omegas[x, y] * t_zero

            fts[x, y] = complex(ft_real, ft_imag) * cmath.exp(complex(0, phi_this))


@cuda.jit
def non_uniform_ft_cuda_with_weights(values, weights, times, omegas, fts, ft_sign, t_zero):
    x, y = cuda.grid(2)
    if x < omegas.shape[0] and y < omegas.shape[1] and (y == 0 or omegas[x, y] != 0):
        if omegas[x, y] == 0:
            count = 1
            summe = values[x, 0]
            while count < omegas.shape[1] and times[x, count] != 0:
                summe += values[x, count]
                count += 1
            fts[x, y] = complex(summe/math.sqrt(float(count)))
        else:
            max_time = 1
            while max_time < omegas.shape[1] and times[x, max_time] != 0:
                max_time += 1
            csum = 0
            ssum = 0
            for i in range(max_time):
                csum += weights[x, i] * math.cos(2.0 * omegas[x, y] * times[x, i])
                ssum += weights[x, i] * math.sin(2.0 * omegas[x, y] * times[x, i])
            tau = 0.5 * math.atan2(ssum, csum)

            sumr = 0
            sumi = 0
            scos2 = 0
            ssin2 = 0

            for i in range(max_time):
                sumr += values[x, i] * math.cos(omegas[x, y] * times[x, i] - tau)
                sumi += values[x, i] * math.sin(omegas[x, y] * times[x, i] - tau)
                scos2 += weights[x, i] * math.pow(math.cos(omegas[x, y] * times[x, i] - tau), 2)
                ssin2 += weights[x, i] * math.pow(math.sin(omegas[x, y] * times[x, i] - tau), 2)

            ft_real = sumr / (math.sqrt(2.0) * math.sqrt(scos2))
            ft_imag = ft_sign * sumi / (math.sqrt(2.0) * math.sqrt(ssin2))
            phi_this = tau - omegas[x, y] * t_zero

            fts[x, y] = complex(ft_real, ft_imag) * cmath.exp(complex(0, phi_this))


def non_uniform_ft_call_cuda(values, times, omegas, ft_sign, t_zero, kernel=(16, 16), weights=None):
    # make values in the right shape and stuff
    if type(values) == list:
        if len([True for x in values if type(x) != list]) != 0:
                raise TypeError(f'values needs to contain only lists if it is 1-dimensonal')
        max_len = max([len(x) for x in values])
        temp = np.zeros((len(values), max_len))
        for i in range(len(values)):
            for k in range(len(values[i])):
                temp[i, k] = values[i][k]
        values = temp

    elif type(values) == np.ndarray:
        if len(values.shape) == 1:
            if len([True for x in values if type(x) != list]) != 0:
                raise TypeError(f'values needs to contain only lists if it is 1-dimensonal')
            max_len = max([len(x) for x in values])
            temp = np.zeros((len(values), max_len))
            for i in range(len(values)):
                for k in range(len(values[i])):
                    temp[i, k] = values[i][k]
            values = temp

        elif len(values.shape) != 2:
            raise TypeError(f'values is expected to be 2-dimensional, but recived array was {len(values.shape)} dimesions')

    else: 
        raise TypeError(f'values is expected to be list or numpy ndarray, but type is {type(values)}')

    # make times
    if type(times) == list:
        if len([True for x in times if type(x) != list]) == 0:
            max_len = max([len(x) for x in times])
            temp = np.zeros((len(times), max_len))
            for i in range(len(times)):
                for k in range(len(times[i])):
                    temp[i, k] = times[i][k]
            times = temp
        elif len([True for x in times if type(float(x)) != float]):
            temp = np.zeros((len(values), len(times)))
            for i in range(len(values)):
                temp[i, :] = times[:]
            times = temp
        else:
            raise TypeError(f'times needs to contain only lists or floats if it is 1-dimensonal')

    elif type(times) == np.ndarray:
        if len(times.shape) == 1:
            if len([True for x in times if type(x) != list]) == 0:
                max_len = max([len(x) for x in times])
                temp = np.zeros((len(times), max_len))
                for i in range(len(times)):
                    for k in range(len(times[i])):
                        temp[i, k] = times[i][k]
                times = temp
            elif times.dtype == np.float64 or times.dtype == np.float32 or times.dtype == np.int32:
                temp = np.zeros((len(values), len(times)))
                for i in range(len(values)):
                    temp[i, :] = times[:]
                times = temp
            else:
                raise TypeError(f'times needs to contain only lists or floats if it is 1-dimensonal')

        elif len(times.shape) != 2:
            raise TypeError(f'times is expected to be 2-dimensional, but recived array was {len(times.shape)} dimesions')

    else: 
        raise TypeError(f'times is expected to be list or numpy ndarray, but type is {type(times)}')

    # make omegas
    if type(omegas) == list:
        if len([True for x in omegas if type(x) != list]) == 0:
            max_len = max([len(x) for x in omegas])
            temp = np.zeros((len(omegas), max_len))
            for i in range(len(omegas)):
                for k in range(len(omegas[i])):
                    temp[i, k] = omegas[i][k]
            omegas = temp
        elif len([True for x in omegas if type(float(x)) != float]):
            temp = np.zeros((len(values), len(omegas)))
            for i in range(len(values)):
                temp[i, :] = omegas[:]
            omegas = temp
        else:
            raise TypeError(f'omegas needs to contain only lists or floats if it is 1-dimensonal')

    elif type(omegas) == np.ndarray:
        if len(omegas.shape) == 1:
            if len([True for x in omegas if type(x) != list]) == 0:
                max_len = max([len(x) for x in omegas])
                temp = np.zeros((len(omegas), max_len))
                for i in range(len(omegas)):
                    for k in range(len(omegas[i])):
                        temp[i, k] = omegas[i][k]
                omegas = temp
            elif times.dtype == np.float64 or times.dtype == np.float32 or times.dtype == np.int32:
                temp = np.zeros((len(values), len(omegas)))
                for i in range(len(values)):
                    temp[i, :] = omegas[:]
                omegas = temp
            else:
                raise TypeError(f'omegas needs to contain only lists or floats if it is 1-dimensonal')

        elif len(omegas.shape) != 2:
            raise TypeError(f'omegas is expected to be 2-dimensional, but recived array was {len(omegas.shape)} dimesions')

    else: 
        raise TypeError(f'omegas is expected to be list or numpy ndarray, but type is {type(omegas)}')

    if not weights is None:
        # make times
        if type(weights) == list:
            if len([True for x in weights if type(x) != list]) == 0:
                max_len = max([len(x) for x in weights])
                temp = np.zeros((len(weights), max_len))
                for i in range(len(weights)):
                    for k in range(len(weights[i])):
                        temp[i, k] = weights[i][k]
                weights = temp
            elif len([True for x in weights if type(float(x)) != float]):
                temp = np.zeros((len(values), len(weights)))
                for i in range(len(values)):
                    temp[i, :] = weights[:]
                weights = temp
            else:
                raise TypeError(f'weights needs to contain only lists or floats if it is 1-dimensonal')

        elif type(weights) == np.ndarray:
            if len(weights.shape) == 1:
                if len([True for x in weights if type(x) != list]) == 0:
                    max_len = max([len(x) for x in weights])
                    temp = np.zeros((len(weights), max_len))
                    for i in range(len(times)):
                        for k in range(len(weights[i])):
                            temp[i, k] = weights[i][k]
                    weights = temp
                elif weights.dtype == np.float64 or weights.dtype == np.float32 or weights.dtype == np.int32:
                    temp = np.zeros((len(values), len(weights)))
                    for i in range(len(values)):
                        temp[i, :] = weights[:]
                    weights = temp
                else:
                    raise TypeError(f'weights needs to contain only lists or floats if it is 1-dimensonal')

            elif len(weights.shape) != 2:
                raise TypeError(f'weights is expected to be 2-dimensional, but recived array was {len(weights.shape)} dimesions')

        else: 
            raise TypeError(f'weights is expected to be list or numpy ndarray, but type is {type(weights)}')

    ft_sign = float(ft_sign)
    time_zero = float(t_zero)

    # check shapes
    if times.shape != values.shape:
        raise ValueError(f'times and values do not have same shape. times is {times.shape} and values is {values.shape}')
    if not weights is None and weights.shape != values.shape:
        raise ValueError(f'weights is not None and has a different shape then values. weights is {weights.shape} and values is {values.shape}')
    if times.shape[0] != omegas.shape[0]:
        raise ValueError(f'times and omegas do not have same length in first dim. times is {times.shape} and values is {omegas.shape}')
    if times.shape[1] == omegas.shape[1]:
        # this is fine this way
        result_shape = omegas.shape
    elif times.shape[1] > omegas.shape[1]:
        # this is expected
        temp = np.zeros(times.shape)
        temp[:omegas.shape[0], :omegas.shape[1]] = omegas[:, :]
        omegas = temp
        result_shape = times.shape
    elif times.shape[1] < omegas.shape[1]:
        # this is odd
        print('Waring: more frequencies then values')
        temp = np.zeros(omegas.shape)
        temp[:times.shape[0], :times.shape[1]] = times[:, :]
        times = temp
        temp = np.zeros(omegas.shape)
        temp[:values.shape[0], :values.shape[1]] = values[:, :]
        values = temp
        if not weights is None:
            temp = np.zeros(omegas.shape)
            temp[:weights.shape[0], :weights.shape[1]] = weights[:, :]
            weights = temp
        result_shape = omegas.shape
    else:
        raise Exception('unexpected behaviour')

    fts = np.zeros(result_shape, dtype=np.complex128)
    blockspergrid = math.ceil(fts.shape[0] / kernel[0]), math.ceil(fts.shape[1] / kernel[1])
    if weights is None
        non_uniform_ft_cuda_no_weights[blockspergrid, kernel](values, times, omegas, fts, ft_sign, time_zero)
    else:
        # this needs to be done on cpu, if not the multiplication will be done multiple times and desyncronised
        values = weights * values
        non_uniform_ft_cuda_with_weights[blockspergrid, kernel](values, weights, times, omegas, fts, ft_sign, time_zero)

    return fts
