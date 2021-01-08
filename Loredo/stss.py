"""
SinusoidTimeSeriesSimulator class for basic periodogram experiments.

2021-01-06:  Created by Tom Loredo (based on ThinnedSchusterPDF.py)
"""

from numpy import *
from scipy.stats import norm
from scipy.fft import rfft, rfftfreq


twopi = 2*pi


class SinusoidTimeSeriesSimulator:
    """
    Generate regularly-sampled time series of a sinusoid with additive Gaussian
    noise, and compute the Schuster periodogram and related quantities.
    """

    def __init__(self, dt, n, tau, A, phi, sig):
        self.dt = dt
        self.n = n
        self.T = (n-1.)*dt  # duration
        self.tau = tau
        self.nu = 1./tau  # frequency
        self.w = twopi/tau  # angular frequency
        self.A = A
        self.phi = phi
        self.sig, self.var = sig, sig**2

        # n/2 Fourier frequencies spaced by 1/(N*dt) ~ 1/T:
        self.ffreqs = linspace(0, 0.5/dt, n//2)

        # 0-mean normal RV:
        self.norm = norm(scale=sig)

        # Define sampling scheme and noise-free signal.
        self.times = linspace(0., self.T, n)
        self.signal = self.tsignal()

    def tsignal(self, nt=None):
        """
        Evaluate the true signal model.
        """
        if nt is None:
            return self.A*cos(self.w*self.times + self.phi)
        else:
            times = linspace(0., self.T, nt)
            return times, self.A*cos(self.w*times + self.phi)

    def simulate(self):
        """
        Simulate an observation of the sinusoidal signal, storing
        results as attributes.
        """
        self.noise = self.norm.rvs(self.n)
        self.y = self.signal + self.noise

    def pgram(self, f):
        """
        Compute the Schuster periodogram the slow way, for an arbitrary
        frequency grid.
        """
        f = asarray(f)
        scalar_in = f.ndim == 0

        freqs = atleast_1d(f)
        pg = empty_like(freqs)
        for i, f in enumerate(freqs):
            wt = twopi*f*self.times
            C = sum(self.y * cos(wt))
            S = sum(self.y * sin(wt))
            pg[i] = (C**2 + S**2)/self.n

        if scalar_in:
            return pg[0]
        else:
            return pg

    def pgram_fft(self, over=1):
        """
        Compute the periodogram using a DFT, for the Fourier frequencies,
        possibly oversampled by `over`, via zero-padding.
        """
        if over == 1:
            y = self.y
        else:
            nz = over*self.n
            y = pad(self.y, ((0, nz)))
        dft = rfft(y)
        freqs = rfftfreq(y.shape[0], d=self.dt)
        return freqs, abs(dft**2)/self.n

    def pgram_lml(self, over=1.):
        """
        Evaluate the Schuster periodogram and the log marginal likelihood
        for frequency.
        """
        # Frequency grid, oversampled if requested:
        if over == 1.:
            freqs = self.ffreqs
        else:
            freqs = linspace(0, 0.5/self.dt, over*self.n)
        df = freqs[1] - freqs[0]

        pgram = self.pgram(freqs)
        # Log marginal likelihood for frequency:
        lml = pgram/self.sig
        # Marginal posterior PDF for frequency:
        lml_max = lml.max()
        mpp = exp(lml - lml_max)
        Z = trapz(mpp, dx=df)
        mpp = mpp/Z
        # Value at true freq:
        mpp_t = exp(self.pgram(self.nu)/self.sig - lml_max)/Z
        return freqs, pgram, lml, mpp, mpp_t
