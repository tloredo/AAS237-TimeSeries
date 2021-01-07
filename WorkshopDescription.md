# Exploring and modeling astrononomical time series data

This one-day workshop will introduce participants to a range of standard
and state-of-the-art methods and tools for exploratory and statistical
analysis of time series data arising in astronomy. Three sessions will
cover:

* periodograms and related Fourier methods
* new methods for
  irregularly sampled time series and individual-event data, and 
* new tools
  for spectro-temporal analysis of photon counting and event data.
The sessions will include tutorial introductions to the motivating astronomy and key statistical and signal processing ideas, and software demonstrations, including hands-on exercises using Python packages developed for astronomical time series analysis.

Brief descriptions of the three planned sessions are as follows.

***Time series exploration using periodograms:*** 
Periodograms---data-derived functions resembling a Fourier power
spectrum---arise in multiple contexts in time series data analysis. This
session will cover three such contexts: detecting and characterizing
periodic signals, estimating the power spectrum for a signal with a
continuous power spectrum, and approximate modeling of time series with
Gaussian process models. Each context uses periodograms, but each
requires different post-processing of a periodogram to quantify evidence
in the data. Failing to distinguish different use cases has led to
persistant misunderstandings about periodograms. The session will
address these topics analytically and with Python exercises.  Presenter:
 Tom Loredo, Cornell Center for Astrophysics and Planetary Science,
Cornell University.

***New methods for analyzing irregularly sampled time series and point data:*** This session will present: (1) An algorithm for computing the
complex Fourier transform of unevenly sampled time series; its magnitude
is the well-known Lomb-Scargle periodogram, but its phase gives the
useful but rarely studied phase spectrum. (2) Various uses of the
discrete correlation function for unevenly sampled time series. (3)
Recent developments in Scargle's popular Bayes Blocks framework,
including applications with high-energy data, and LIGO data.  Software
demonstrations will use MATLAB, though several algorithms are also being
ported to Python.  Presenter: Jeffrey Scargle, NASA Ames Research
Center.

***New tools for spectro-temporal analysis of X ray time series data:***
This session will describe methods for modeling photon counting and
individual-photon event data from sources with time-evolving energy
spectra in high-energy astrophysics ("spectral-timing data"). Methods
covered will include dynamic power spectra, cross spectra, covariance
spectra, spectral lag estimation, and related methods. The session will
demonstrate methods using the Python Stingray package, including
demonstrations of tools for simulating light curves and time-tagged
event data with diverse types of variability.  Presenter: Daniela
Huppenkothen, Center for Data-Intensive Research in Astronomy and
Cosmology (DIRAC), University of Washington.