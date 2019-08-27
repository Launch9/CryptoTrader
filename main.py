import pyximport
pyximport.install(setup_args={'include_dirs':['']}, language_level='3str')
from StatsGiver import StatsGiver

from App import App

mainApp = App()

mainApp.run()

