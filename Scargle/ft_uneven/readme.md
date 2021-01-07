Short descibtion of the different files and requirements for running them:

All files contain code to calculate the Fourier transformation for an unevenly sampled time series. 
All points can be sampled equally or weights can be used. 

ft_uneven.m:
Is the original matlab program.

py_ft.py, numba_ft.py and cuda_ft.py are written for python, but have differen requirements. 

py_ft.py:
Only requires the "numpy" module. It can either run a single time series or a bulk of time series with a single call of a function.
If running a bulk calculation, mulitprocessing can be used. For this the "multiprocessing" modul is required. 
Only when the multiprocessing is envoked the module needs to be installed.

numba_ft.py:
Requires the "numba" module, in addition to the "numpy" module. Here also single and bulk calculation can be envoked.
Multithreading can be used without requiring further modules. The numba_ft.py version runs around 3 times faster then the py_ft.py version.

cuda_ft.py:
Requires a CUDA-capable GPU, Nvidia-drivers, CUDA, and cudnn. CUDA and cudnn can be installed with conda installing "cudatoolkit". 
Only a function calculating bulk can be called, which will run on the GPU.
For this module to run properly, the times and omegas arguments can only take 0.0 as an argument in the 0th index of the array. 

The functions as well as their arguments are commeted for further information such as type of the arguments. 
