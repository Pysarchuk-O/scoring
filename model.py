
'''
Модуль моделі багатокритеріального скорингу

'''

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------------------------------------

# 2.4.Інтегрована багатокритеріальна оцінка - SCOR
def Voronin(d_segment_sample_minimax_Normal, d_segment_data_description_minimax, k):

    n = d_segment_data_description_minimax['Field_in_data'].size    # кількість критеріїв

    Integro = np.zeros((k))
    Scor = np.zeros((k))
    for i in range(0, k):
         Sum_Voronin = 0
         for j in range(0, n):
             Sum_Voronin = Sum_Voronin + ((1 - d_segment_sample_minimax_Normal[i, j]) ** (-1))
         Integro[i] = Sum_Voronin
         Scor[i] = 1000                             # порог прийняття рішень про видачу кредиту - емпірічний
         np.savetxt('Integro_Scor.txt', Integro)    # файл інтегрованого показника - СКОРУ

    plt.title("Multi-criteria integrated Scor")
    plt.xlabel("client")
    plt.ylabel("Scor")
    plt.grid(which='major')
    plt.plot(Integro)
    plt.plot(Scor)
    plt.show()

    return Integro


