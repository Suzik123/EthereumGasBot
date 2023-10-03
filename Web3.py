import pickle
import numpy as np
from web3 import Web3
import time
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import matplotlib.ticker as ticker
infura_url = '<your-api>'
web3 = Web3(Web3.HTTPProvider(infura_url))


def get_gas_price():
    gas_price = web3.eth.gas_price / 1000000000
    current_gas_price = "Current gas price: " + str(gas_price) + " gwei"
    return current_gas_price


def get_gas_Rprice():
    gas_price = web3.eth.gas_price / 1000000000
    return gas_price


def show_graph():
    with open('/root/GasInfo/gas_today_info', 'rb') as f:
        gas_today_info = pickle.load(f)

    with open('/root/GasInfo/time_info', 'rb') as f:
        time_info = pickle.load(f)

    x = np.linspace(0, 24, len(time_info))

    plt.plot(x, gas_today_info)

    x_ticks = [0, 3, 6, 9, 12, 15, 18, 21, 24]
    x_labels=[]
    for i in range(len(time_info)):
        if i%90==0:
            if time_info[i].hour+3<24:
                x_labels.append(str(time_info[i].hour+3)+":"+str(time_info[i].minute))
            else:
                x_labels.append(str(time_info[i].hour - 21) + ":" + str(time_info[i].minute))
    x_labels.append(str(time_info[719].hour+3)+":"+str(time_info[i].minute))
    print(len(x_ticks), len(x_labels))
    plt.xticks(ticks=x_ticks, labels=x_labels)
    plt.grid(True)

    for xc in plt.xticks()[0]:
        plt.vlines(x=xc, ymin=0, ymax=np.sin(xc), linestyle='--', color='gray')
    first_day = time_info[0].date()
    last_day = time_info[-1].date()
    plt.title(str(first_day) + " — " + str(last_day))
    plt.xlabel("Time")
    plt.ylabel('Gas')    
    plt.show()

    image_path = 'gas_chart.png'
    plt.savefig(image_path, format='png')
    plt.clf()
    return image_path
