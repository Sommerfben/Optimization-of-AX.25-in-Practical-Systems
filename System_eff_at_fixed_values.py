import numpy,random
import itertools
from decimal import Decimal
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

N_MAX = 40            #max frames per packet
n_MAX = 80          #max number of info bytes
BER = 0.01              #10^-3
AX25_OVERHEAD = 160       #AX.25 overhead bits
#TOTAL_DL_DATA = 1048576*8*0.8 #Downlink bits
TOTAL_DL_DATA = 50000
SWITCHING_IME = 1
BAUD_RATE = 19200
K_UL = AX25_OVERHEAD + 8
RUN_NUMBER = 30

def value_extractor(list, tuple_index, num_results):
    value_list = []
    if (len(list)-num_results < 1):
        for a in list:
            value_list.append(a[tuple_index])
    else :
        for a in list[len(list)-num_results:]:
            value_list.append(a[tuple_index])
    return value_list


def BER_simulator(bit_error_rate):
    x = numpy.random.randint(0, numpy.reciprocal(BER))
    if x == 1:
        return 0
    else:
        return 1

def frame_transmit(info_bits_in_frame, bit_error_rate):
    i = 0
    for i in range(info_bits_in_frame):                     #add overhead
        if(BER_simulator(bit_error_rate) == 0):
            return 0
    return 1

def FER_simulator(info_bits_in_frame,bit_error_rate):
    # 10 < n < 110 for 1% < FER < 15%
    # total_dl_bits/100 < N < total_dl_bits/10
    global AX25_OVERHEAD
    fer = 1 - (1 - bit_error_rate)**(info_bits_in_frame + AX25_OVERHEAD)
    #x = numpy.random.randint(0, numpy.reciprocal(fer))
    if random.random() < fer:
        return 0
    else:
        return 1

def fer_packet_transmit(number_of_frames_per_packet, info_bits_in_frame, bit_error_rate):
    global AX25_OVERHEAD
    bits_transmitted = 0
    while k < number_of_frames_per_packet:
        if (FER_simulator(bit_error_rate, info_bits_in_frame, AX25_OVERHEAD)):
            k = k - 1
        bits_transmitted = bits_transmitted + info_bits_in_frame + AX25_OVERHEAD
        k= k + 1
    return bits_transmitted

def packet_transmit(number_of_frames_per_packet, info_bits_in_frame, bit_error_rate):
    global AX25_OVERHEAD
    global BAUD_RATE
    global K_UL
    bits_transmitted = 0
    k = 0
    while k < number_of_frames_per_packet:
        if (FER_simulator(info_bits_in_frame, bit_error_rate) == 0):
            bits_transmitted = bits_transmitted + info_bits_in_frame + AX25_OVERHEAD + BAUD_RATE * 2 + K_UL
        else:
            bits_transmitted = bits_transmitted + info_bits_in_frame + AX25_OVERHEAD
            k = k + 1
    bits_transmitted = bits_transmitted + BAUD_RATE * 2 + K_UL
    return bits_transmitted

def main():
    global n_MAX
    global N_MAX
    global BER
    N = N_MAX
    n = n_MAX
    total_downlinked_bits = 0
    minimum_downlinked_bits = TOTAL_DL_DATA * 999999 #Some arbitarily huge number
    answer = []
    last_five_results = []
    best_values = []
    total_downlinked_bits = 0
    for i in range(int(TOTAL_DL_DATA/(n+1)/(N+1))):
        total_downlinked_bits = total_downlinked_bits + packet_transmit(N+1,n+1,BER)
    my_tuple = (n+1,N+1,total_downlinked_bits)
    answer.append(my_tuple)
    print(str(my_tuple) + ' %.2E' % Decimal(my_tuple[2]))

    if minimum_downlinked_bits > total_downlinked_bits:
        minimum_downlinked_bits = total_downlinked_bits
        best_values = my_tuple
    N = N + 1
    print("minimum_downlinked_bits = " + '%.2E' % Decimal(minimum_downlinked_bits))
    return(best_values)


def stat_analysis():
    global RUN_NUMBER
    global TOTAL_DL_DATA
    results = []
    eff = []
    for i in range(RUN_NUMBER):
        results.append(main())
    print(results)

    Downlinked_bits = value_extractor(results, 2,1000)
    n_values = value_extractor(results, 0,1000)
    eff = [TOTAL_DL_DATA/y for y in Downlinked_bits]
    plt.bar(range(RUN_NUMBER),Downlinked_bits, align='center', alpha=0.5)
    plt.ylabel('Total bits downlinked')
    plt.xlabel('Run number')
    plt.title('Total bits needed to downlink a fixed data payload')

    plt.show()

stat_analysis()
