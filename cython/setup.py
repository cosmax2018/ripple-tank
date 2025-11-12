# setup.py : automatically cythonize CA Ripple Tank
# use:  python setup.py build_ext --inplace
#       python ca_ripple_tank_fast.py

import setuptools  # important
from distutils.core import setup
from Cython.Build import cythonize

# define an extension that will be cythonized and compiled
setup(ext_modules = cythonize('tlm_ripple_tank_v1_fast.pyx',build_dir="build"),
															script_args=['build'], 
															options={'build':{'build_lib':'.'}})