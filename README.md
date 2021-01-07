# AAS237-TimeSeries

This repo contains content for a workshop on time series data analysis being held at the [237th AAS Meeting](https://aas.org/meetings/aas237), being held virtually on 8 January 2021.  

The presenters are:

* [Daniela Huppenkothen](https://huppenkothen.org/) (SRON Netherlands Institute for Space Research)
* [Tom Loredo](http://www.astro.cornell.edu/staff/loredo/) (workshop organizer, Cornell Center for Astrophysics and Planetary Science)
* [Jeff Scargle](https://www.nasa.gov/centers/ames/research/2007/scargle.html) (NASA Ames Research Center).

The workshop will have three sessions (separated by half-hour breaks):

* Time series analysis using periodograms (Loredo): 11am - 1pm ET 
* New methods for analyzing irregularly sampled time series and point
  data (Scargle): 1:30pm - 3:30pm ET
* New tools for spectro-temporal analysis of X ray time series data (Huppenkothen): 4pm - 6pm ET

The workshop will include hands-on demonstrations using Python (in Jupyter notebooks), and possibly some live demos in MATLAB (with code available for MATLAB users).

## Computer preparation for the workshop

Please prepare you computer for the workshop **before the workshop**.

**Do not postpone this until the last minute.**  Depending on what software you may already have installed, some steps of this setup may require time-consuming downloads.

We will presume participants have basic familiarity with terminal-based command line computing, and with the Python language and Jupyter notebooks.

To run the lab materials, you will need the following resources (version numbers are those we used for testing; earlier versions will likely work but it's safest to use these versions):

* Python 3.8+
* IPython 7+
* The PyData stack (NumPy, SciPy, matplotlib...)

If you already have these resources installed and are feeling adventurous, feel free to use your own installation. But please note that the limited time we have for the workshop won't allow us to help with problems associated with specific installations.

We *strongly* recommend that you use the `ts21` ("Time Series 2021") `conda` environment described below for running the lab materials. It's what we have used for developing the materials.  If you already use a different (non-`conda`) Python distribution and are worried about conflicts, consider the Miniconda option mentioned below—it will minimally alter your default command-line environment, and install the new material in an encapsulated manner.  If you are particularly concerned about conflicts, consider setting up a separate user account on your computer to use for the workshop (Anaconda installs material only in the user's account).

*We will be revising lab materials up to the time of the workshop*; please postpone downloading and running the material until then unless instructed otherwise here or via the workshop's Slack channel.

### Installing the Anaconda `ts21` environment

Set up a `ts21` environment for the workshop as follows:

* Install Anaconda with Python 3.8: [Downloads | Anaconda](https://www.anaconda.com/download/).  Exceptions:

    - If you already have Anaconda installed, you do not need to re-install it, even if you are using an older Python version.
    - If you have a customized command-line environment with a non-conda Python distribution, and you'd like a setup with minimal impact in your default environment, install Miniconda with Python 3.8 instead: [Miniconda — Conda documentation](https://docs.conda.io/en/latest/miniconda.html).

* Update the `conda` command-line package manager in a terminal/shell session by running `conda update conda`. The update command may report that it is changing your Anaconda package to a "custom" version.  This will not be a problem.

* Define and install the initial `ts21` environment by using `conda` at the command line as follows (here "$" represents the prompt).
  ```bash
  $ conda create -n ts21 anaconda
  ```

* Verify that the environment works by activating it.  In your Terminal Window, run:
  ```bash
  $ conda activate ts21
  ```
  
* Add the `stingray` package to the environment (this will also add several dependencies, such as `statsmodels`, `emcee`, and `corner`; note that you must run this command in the *activated* environment):

  ```bash
  $ conda install -c conda-forge stingray
  ```
  If you're *not* using conda to manage your Python distribution, see the [installation instructions in the Stingray documentation](https://stingray.readthedocs.io/en/latest/stingray/docs/install.html).

* We may provide some test code to run in the near future; stay tuned on Slack for announcements.

* You may quit your terminal session, or deactivate the environment by running `conda deactivate`.

At this point you should be set up.

