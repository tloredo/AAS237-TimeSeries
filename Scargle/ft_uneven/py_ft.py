import numpy as np 

# call ft_uneven for a single time series and ft_uneven_bulk for multiple time series


# This Block of methods is used to parse the arguments for bulk calculations


def indexed(array2d):
    def dummy(index):
        return array2d[index]
    return dummy 


def not_indexed(array):
    def dummy(index):
        return array 
    return dummy


def is_none():
    def dummy(index):
        return None 
    return dummy


def select_indexed(array):
    if array is None:
        return is_none()
    if type(array[0]) == list or type(array[0]) == np.ndarray:
        return indexed(times)
    else:
        return not_indexed(times)


# main methods for ft_uneven calculation


# values, times, omegas: list or ndarray(1 dim), ft_sign, time_zero: float, weights: list or ndarray(1 dim), return_ls, lin_weights: boolean
def ft_uneven(values, times, omegas, ft_sign, time_zero, weights=None, return_ls=False, lin_weights=False):

    num_val = len(values)
    num_omg = len(omegas)

    # raise error if no frequencies are given
    if num_omg == 0:
        raise ValueError('omegas argument cannot be empty')

    lss = np.zeros(num_omg)
    fts = np.zeros(num_omg, dtype=np.cdouble)

    # if there are no weights given
    if weights is None:
        for i in range(num_omg):
            omg = omegas[i]
            # if omg is not 0
            if omg:
                csum = np.sum(np.cos(2.0 * omg * times))
                ssum = np.sum(np.sin(2.0 * omg * times))
                tau = 0.5 * np.arctan2(ssum, csum)

                sumr = np.sum(values * np.cos(omg * times - tau))
                sumi = np.sum(values * np.sin(omg * times - tau))

                scos2 = np.sum((np.cos(omg * times - tau))**2)
                ssin2 = np.sum((np.sin(omg * times - tau))**2)

                ft_real = sumr/(2**0.5 * scos2**0.5)
                ft_imag = ft_sign * sumi/(2**0.5 * ssin2**0.5)
                phi_this = tau - omg * time_zero

                fts[i] = (ft_real + ft_imag * 1j) * np.exp(1j*phi_this)
                lss[i] = (sumr**2/scos2) + (sumi**2/ssin2)
                
            else:
                fts[i] = np.sum(values)/np.sqrt(num_val)
                lss[i] = fts[i]**2

    else:
        #if lin_weights:
        values = weights * values
        for i in range(num_omg):
            omg = omegas[i]
            #if not lin_weights:
                #values = weights * values
            # if omg is not 0
            if omg:
                csum = np.sum(weights * np.cos(2.0 * omg * times))
                ssum = np.sum(weights * np.sin(2.0 * omg * times))
                tau = 0.5 * np.arctan2(ssum, csum)

                sumr = np.sum(values * cos(omg * times - tau))
                sumi = np.sum(values * sin(omg * times - tau))

                scos2 = np.sum(weights * (np.cos(omg * times - tau))**2)
                ssin2 = np.sum(weights * (np.sin(omg * times - tau))**2)

                ft_real = sumr/(2**0.5 * scos2**0.5)
                ft_imag = ft_sign * sumi / (2**0.5 * ssin2**0.5)
                phi_this = tau - omg * time_zero

                fts[i] = (ft_real + ft_imag * 1j) * np.exp(1j*phi_this)
                lss[i] = (sumr**2/scos2) + (sumi**2/ssin2)

            else:
                fts[i] = np.sum(values)/np.sqrt(num_val)
                lss[i] = fts[i]**2

    if return_ls:
        return fts, lss
    else:
        return fts


# values: list (containing lists or ndarrays(1 dim)) or ndarray(2 dim) or ndarray(1 dim containing ndarrays (1 dim))
# times, omegas: list (containing lists or ndarrays(1 dim)) or ndarray(2 dim) or ndarray(1 dim containing ndarrays (1 dim)) or list or ndarray (1 dim)
# if times, omegas is 1-dim, times and omegas are used for all time series
#ft_sign, time_zero: float, weights: list or ndarray(1 dim), return_ls, lin_weights: boolean

# mulitthreading required multiprocessing module (should be preinstalled)
def ft_uneven_bulk(values, times, omegas, ft_sign, time_zero, weights=None, return_ls=False, lin_weights=False, multithreading=False):
    # parse times, omegas and weights 
    times = select_indexed(times)
    omegas = select_indexed(omegas)
    weights = select_indexed(weights)

    # different ways of envoking calculations depending if multiprocessing should be used
    if not multithreading:
        # straight forward, one loop going over each times series one at the time
        results = []
        for i in range(len(values)):
            results.append(ft_uneven(values[i], times(i), omegas(i), ft_sign, time_zero, weights=weights(i), return_ls=return_ls, lin_weights=lin_weights))
    else:
        from multiprocessing import Pool 
        pool = Pool()
        n = len(values)
        results = pool.starmap(ft_uneven, zip(values, [times(i) for i in range(n)], [omegas(i) for i in range(n)], \
            [ft_sign]*n, [time_zero]*n, [weights(i) for i in range(n)], [return_ls]*n, [lin_weights]*n))
    return results


# test if code runs
if __name__ == '__main__':
    ran = np.random.standard_normal
    values = ran(size=(100, 100))
    times = ran(size=(100))
    omegas = ran(size=(100))

    ft_uneven_bulk(values, times, omegas, 1, 0)

