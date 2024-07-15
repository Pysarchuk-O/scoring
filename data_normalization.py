'''
Модуль нормалізації даних

'''

import pandas as pd
import numpy as np

def normalization(d_segment_sample_cleaning):

    # ----------------------------------- ІІ. ФОРМУВАННЯ СКОРИНГОВОЇ МОДЕЛІ ------------------------------

    # 2.1. Парсінг файлу індикаторів (критеріїв) скорингової карти
    d_data_description_minimax = pd.read_excel('d_segment_data_description_cleaning_minimax.xlsx')  # інфологічна модель

    # відбір критеріїв
    d_segment_data_description_minimax = d_data_description_minimax.loc[
        (d_data_description_minimax['Minimax'] == 'min')
        | (d_data_description_minimax['Minimax'] == 'max')]
    d_segment_data_description_minimax.index = range(0,
                                                     len(d_segment_data_description_minimax))  # балансування індексів в сегменті 0-n
    print('----------------- DataFrame d_segment_data_description_minimax  ----------------')
    print(d_segment_data_description_minimax)
    print('-----------------------------------------------------------------')
    d_segment_data_description_minimax.to_excel(
        'd_segment_data_description_minimax.xlsx')  # збереження очищених показників

    # відбір даних за критеріями
    d = d_segment_data_description_minimax['Field_in_data']
    cols = d.values.tolist()  # перетворення стовпчика DataFrame у рядок
    d_segment_sample_minimax = d_segment_sample_cleaning[cols]
    print('----------------- DataFrame d_segment_sample_minimax  ----------------')
    print(cols)
    print(d_segment_sample_minimax)
    print('-----------------------------------------------------------------')
    d_segment_sample_minimax.to_excel('d_segment_sample_minimax.xlsx')  # збереження очищених даних

    # 2.2. Парсінг файлу індикаторів (критеріїв) скорингової карти
    # мінімальні, максимальні значення стовпчиків DataFrame
    d_segment_sample_min = d_segment_sample_minimax[cols].min()
    d_segment_sample_max = d_segment_sample_minimax[cols].max()
    print('----------------- DataFrame: d_segment_sample_min  ----------------')
    print(d_segment_sample_min)
    print('----------------- DataFrame: d_segment_sample_max  ----------------')
    print(d_segment_sample_max)

    # 2.3.Нормування критеріїв
    m = d_segment_sample_minimax['loan_amount'].size
    n = d_segment_data_description_minimax['Field_in_data'].size
    d_segment_sample_minimax_Normal = np.zeros((m, n))  # перехід в розрахунках до масиву numpy

    delta_d = 0.3  # коефіцієнт запасу при нормуванні
    for j in range(0, len(d_segment_data_description_minimax)):
        columns_d = d_segment_data_description_minimax['Minimax'][j]
        if columns_d == 'min':
            columns_m = d_segment_data_description_minimax['Field_in_data'][j]
            for i in range(0, len(d_segment_sample_minimax)):
                max_max = d_segment_sample_max[j] + (2 * delta_d)
                d_segment_sample_minimax_Normal[i, j] = (delta_d + d_segment_sample_minimax[columns_m][i]) / (max_max)
        else:
            for i in range(0, len(d_segment_sample_minimax)):
                min_min = d_segment_sample_max[j] + (2 * delta_d)
                d_segment_sample_minimax_Normal[i, j] = (1 / (delta_d + d_segment_sample_minimax[columns_m][i])) / (
                    min_min)

    print(d_segment_sample_minimax_Normal)
    np.savetxt('d_segment_sample_minimax_Normal.txt', d_segment_sample_minimax_Normal)  # файл нормованих параметрів

    # ---------------------------- структура нормованого масиву ----------------------------------------------
    '''
    d_segment_sample_minimax_Normal[i, j]:
    m = d_segment_sample_minimax['loan_amount'].size              - кількість позичальників
    n = d_segment_data_description_minimax['Field_in_data'].size  - кількість індикаторів скорингової таблиці
    d_segment_sample_minimax_Normal=np.zeros((m, n))              - перехід в розрахунках до масиву numpy    
    '''
    return d_segment_sample_minimax_Normal, d_segment_data_description_minimax
