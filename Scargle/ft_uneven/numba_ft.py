import numpy as np 
from numba import njit, prange


# for data types of parameters see py_ft:
# py_ft.ft_uneven == numba_ft.ft_uneven (without the return_ls argument)
# py_ft.ft_uneven_bulk == ft_uneven_bulk_adaptive
# prefer numpy arrays for increased speed


# This Block of methods is used to parse the arguments for bulk calculations


@njit
def indexed(length, d2=False):
    length = int(length)
    @njit 
    def dummy_d1(index):
        return slice(0, length, 1)

    @njit
    def dummy_d2(index):
        return slice(index, index+1, 1)

    if d2:
        return dummy_d2
    return dummy_d1


@njit
def indexing(length, index, d2):
    if d2:
        return slice(index, index+1, 1)
    return slice(0, length, 1)


def is2d(array):
    return type(array[0]) == list or type(array[0]) == np.ndarray

    
# calculates ft for non-uniform sampled times. Only one time series
@njit
def ft_uneven(values, times, omegas, ft_sign, time_zero, weights=None, lin_weights=False):

    num_val = len(values)
    num_omg = len(omegas)

    # raise error if no frequencies are given
    if num_omg == 0:
        raise ValueError('omegas argument cannot be empty')

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
                
            else:
                fts[i] = np.sum(values)/np.sqrt(num_val)

    else:
        #if lin_weights:
        values = weights * values
        for i in range(num_omg):
            omg = omegas[i]
            #if not lin_weights:
            #    values = weights * values
            # if omg is not 0
            if omg:
                csum = np.sum(weights * np.cos(2.0 * omg * times))
                ssum = np.sum(weights * np.sin(2.0 * omg * times))
                tau = 0.5 * np.arctan2(ssum, csum)

                sumr = np.sum(values * np.cos(omg * times - tau))
                sumi = np.sum(values * np.sin(omg * times - tau))

                scos2 = np.sum(weights * (np.cos(omg * times - tau))**2)
                ssin2 = np.sum(weights * (np.sin(omg * times - tau))**2)

                ft_real = sumr/(2**0.5 * scos2**0.5)
                ft_imag = ft_sign * sumi / (2**0.5 * ssin2**0.5)
                phi_this = tau - omg * time_zero

                fts[i] = (ft_real + ft_imag * 1j) * np.exp(1j*phi_this)

            else:
                fts[i] = np.sum(values)/np.sqrt(num_val)
    return fts#, num_omg


# functions for looping over bulk, diffent functions for diffent forms of times and omega

# times and omega are both 2d
def _bulk_intern(values, times, omegas, ft_sign, time_zero, weights=None, lin_weights=False):
    results = np.zeros((len(values), len(omegas)), dtype=np.complex128)
    if weights is None:
        for i in prange(len(values)):
            results[i, :len(omegas[i])] = ft_uneven(values[i], times[i], omegas[i], ft_sign, time_zero, weights=None, lin_weights=lin_weights) 
    else:
        for i in prange(len(values)):
            results[i, :len(omegas[i])] = ft_uneven(values[i], times[i], omegas[i], ft_sign, time_zero, weights=weights[i], lin_weights=lin_weights) 
    return results


# times is 2d, omega is 1d
def _bulk_intern_fixed_omg(values, times, omegas, ft_sign, time_zero, weights=None, lin_weights=False):
    results = np.zeros((len(values), len(omegas)), dtype=np.complex128)
    if weights is None:
        for i in range(len(values)):
            results[i] = ft_uneven(values[i], times[i], omegas, ft_sign, time_zero, weights=None, lin_weights=lin_weights) 
    else:
        for i in range(len(values)):
            results[i] = ft_uneven(values[i], times[i], omegas, ft_sign, time_zero, weights=weights[i], lin_weights=lin_weights) 
    return results


# times is 1d, omgega is 2d
def _bulk_intern_fixed_time():
    results = np.zeros((len(values), len(omegas)), dtype=np.complex128)
    if weights is None:
        for i in prange(len(values)):
            results[i, :len(omegas[i])] = ft_uneven(values[i], times, omegas[i], ft_sign, time_zero, weights=None, lin_weights=lin_weights) 
    else:
        for i in prange(len(values)):
            results[i, :len(omegas[i])] = ft_uneven(values[i], times, omegas[i], ft_sign, time_zero, weights=weights[i], lin_weights=lin_weights) 
    return results


# times and omega are both 1d
def _bulk_intern_fixed_time_omg(values, times, omegas, ft_sign, time_zero, weights=None, lin_weights=False):
    results = np.zeros((len(values), len(omegas)), dtype=np.complex128)
    if weights is None:
        for i in prange(len(values)):
            results[i] = ft_uneven(values[i], times, omegas, ft_sign, time_zero, weights=None, lin_weights=lin_weights) 
    else:
        for i in prange(len(values)):
            results[i] = ft_uneven(values[i], times, omegas, ft_sign, time_zero, weights=weights[i], lin_weights=lin_weights) 
    return results


# here the fucntions from above are given to the compiler, one multithreaded, one single threaded each
_bulk_intern_single = njit(_bulk_intern)
_bulk_intern_parallel = njit(parallel=True)(_bulk_intern)

_bulk_intern_s_f_omg = njit(_bulk_intern_fixed_omg)
_bulk_intern_p_f_omg = njit(parallel=True)(_bulk_intern_fixed_omg)

_bulk_intern_s_f_t = njit(_bulk_intern_fixed_time)
_bulk_intern_p_f_t = njit(parallel=True)(_bulk_intern_fixed_time)

_bulk_intern_s_f_tomg = njit(_bulk_intern_fixed_time_omg)
_bulk_intern_p_f_tomg = njit(parallel=True)(_bulk_intern_fixed_time_omg)


# makes a bulk calculation of ft_uneven. Can run multithreaded: USE THIS
# this function is not compiled to allow different input types giving a adaptive version
# but it can't be called from another function compiled with njit
def ft_uneven_bulk_adaptive(values, times, omegas, ft_sign, time_zero, weights=None, lin_weights=False, multithreading=True):
    # fixed omg, fixed time, multithreading
    func_dict = {
    (True, True, True): _bulk_intern_p_f_tomg,
    (True, True, False): _bulk_intern_s_f_tomg,
    (True, False, True): _bulk_intern_p_f_omg,
    (True, False, False): _bulk_intern_s_f_omg,
    (False, True, True): _bulk_intern_p_f_t,
    (False, True, False): _bulk_intern_s_f_t,
    (False, False, True): _bulk_intern_single,
    (False, False, False): _bulk_intern_parallel
    }

    # check with function can be run, depneding on the from of times and omega
    t_form = not is2d(times)
    omg_form = not is2d(omegas)

    results = func_dict[(omg_form, t_form, multithreading)](values, times, omegas, ft_sign, time_zero, weights=weights, lin_weights=False)

    # restructure and remove 0 from results, then return
    if type(omegas) == np.ndarray and len(omegas.shape) == 2 or omg_form:
        return results
    else:
        res_list = []
        for i in range(len(results)):
            res_list.append(results[:len(omegas[i])])
        return res_list
    

# test if code runs
if __name__ == '__main__':
    ran = np.random.standard_normal
    values = ran(size=(100, 100))
    times = ran(size=(100))
    omegas = ran(size=(100))

    print(type(values))

    #ft_uneven_bulk(values, times, omegas, 1, 0)
    ft_uneven(values[0], times, omegas, 1, 0)
    print(len(omegas))
    njit(parallel=True)(_bulk_intern_fixed_time_omg)(values, times, omegas, 1, 0)
    ft_uneven_bulk_adaptive(values, times, omegas, 1, 0)
