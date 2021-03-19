"""
Import this script to set figure formats uniformly throughout all scripts/notebooks
Color scheme is based on PBF website, using https://www.colorhexa.com/
"""

import seaborn as sns
import matplotlib.pyplot as plt


def get_color_dictionary():
    colorDict = {'main':'#324dba', #title_blue
                 'dark':'#263a8c', #darker_blue
                 'light':'#3291ba', #sky_blue
                 'complement':'#32ba9f' #green
                 }
    return colorDict


plt.style.use('ggplot')

sns.set_theme(rc={
    'axes.facecolor': 'None',
    'figure.facecolor': 'white',
    'axes.edgecolor': 'lightgrey',
    'axes.grid': False, 
    'axes.spines.right': False, 
    'axes.spines.top': False, 
})

