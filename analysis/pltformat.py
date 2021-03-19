"""
Import this script to set figure formats uniformly throughout all scripts/notebooks
Color scheme is based on PBF website, using https://www.colorhexa.com/
"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('ggplot')

sns.set_theme(rc={
    'axes.facecolor': 'None',
    'figure.facecolor': 'white',
    'axes.edgecolor': 'lightgrey',
    'axes.grid': False, 
    'axes.spines.right': False, 
    'axes.spines.top': False, 
})

# Currently unused, I think?
title_blue = '#324dba'
darker_blue = '#263a8c'
sky_blue = '#3291ba'
green = '#32ba9f'

