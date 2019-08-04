from distutils.core import setup
from Cython.Build import cythonize

setup(name="HeavyAl", ext_modules=cythonize('HeavyAl.pyx',compiler_directives={'language_level' : "3"}),)