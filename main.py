
import datetime
from utils import functions

def main():

    size = 15000000
    missing_weight = 0.03 
    waiting_weight = 0.08
    returned_weight= 0.11

    dataframe = functions.generate_random_data(size, missing_weight, waiting_weight, returned_weight)
    print(dataframe)
    # functions.insert_data_into_bigQuery(dataframe)

    # pie chart to see if the data follows the weights
    returned, delivered, missing, waiting= functions.get_chart_data(dataframe)
    y = np.array([returned, delivered, missing, waiting])
    mylabels = ["Returned", "Delivered", "Missing", "Waiting"]

    plt.pie(y, labels=mylabels)
    plt.show() 


if __name__ == '__main__':
    import sys
    import logging
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    sys.exit(int(main() or 0))