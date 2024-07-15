'''
Модуль парсингу та підготовки даних

'''

import pandas as pd
import numpy as np


def parsing(filename_sample_data, filename_data_description):

    # 1.1. Парсінг файлу вхідних даних
    d_sample_data = pd.read_excel(filename_sample_data, parse_dates=['applied_at'])
    print('d_sample_data=', d_sample_data)  # вивід усього DataFrame файлу sample_data.xls
    Title_d_sample_data = d_sample_data.columns  # імпорт імен стовпців DataFrame - d

    # 1.2. Аналіз структури вхідних даних
    print('-------------  назви стовпців DataFrame  -----------')
    print(Title_d_sample_data)  # заголовок стовпців таблиці DataFrame
    print('---------  типи даних стовпців DataFrame  -----------')
    print(d_sample_data.dtypes)  # визначення типу даних таблиці DataFrame
    print('---------  пропущені значення стовпців (суми)  ------')
    print(d_sample_data.isnull().sum())  # визначення пропусків даних DataFrame

    # 1.3. Парсінг файлу та аналіз структури скорингових індикаторів
    d_data_description = pd.read_excel(filename_data_description)
    print('---------------  d_data_description  ---------------')
    print('d_data_description=', d_data_description)  # вивід усього DataFrame файлу data_description.xls
    print('----------------------------------------------------')

    # 1.4. Первинне формування скорингової таблиці
    d_segment_data_description_client_bank = d_data_description[
        (d_data_description.Place_of_definition == 'Вказує позичальник')
        | (d_data_description.Place_of_definition == 'параметри, повязані з виданим продуктом')]
    # n_client_bank = d_segment_data_description_client_bank['Place_of_definition'].size  # розмір стовпця
    d_segment_data_description_client_bank.index = range(0,
                                                         len(d_segment_data_description_client_bank))  # балансування індексів в сегменті 0-n
    print('---------  d_segment_data_description_client_bank  -----------')
    print('d_segment_data_description_client_bank=', d_segment_data_description_client_bank)
    print('----------------------------------------------------')

    # 1.5. Очищення даних
    # 1.5.1. Аналіз перетину скорингових індикаторів та сегменту вхідних даних

    # ------ перевірка наявності індексів клієнта та кредиту з d_data_description в даних d_sample_data -------
    print('-----------------------------------------')
    b = d_segment_data_description_client_bank[
        'Field_in_data']  # 'Field_in_data' - стовчик із назвами індиаторів скорінгу

    if set(b).issubset(d_sample_data.columns):  # перевірка всього columns
        Flag_b = 'Flag_True'
    else:
        Flag_b = 'Flag_False'
    print('УВАГА! сегмент columns за співпадінням:', Flag_b)

    # ------ кількість співпадінь
    n_columns = d_segment_data_description_client_bank['Field_in_data'].size
    j = 0
    for i in range(0, n_columns):
        a = d_segment_data_description_client_bank['Field_in_data'][i]
        if set([a]).issubset(d_sample_data.columns):
            j = j + 1
    print('j = ', j)

    # ------ індекси співпадінь
    Columns_Flag_True = np.zeros((j))
    j = 0
    for i in range(0, n_columns):
        a = d_segment_data_description_client_bank['Field_in_data'][i]
        if set([a]).issubset(d_sample_data.columns):  # перевірка кожного columns
            Columns_Flag_True[j] = i
            j = j + 1
    print('Індекси співпадінь', Columns_Flag_True)

    # 1.5.2. Формування DataFrame даних з урахуванням відсутніх індикаторів скорингової таблиці
    # ------ DataFrame співпадінь
    d_segment_data_description_client_bank_True = d_segment_data_description_client_bank.iloc[
        Columns_Flag_True]
    d_segment_data_description_client_bank_True.index = range(0,
                                                              len(d_segment_data_description_client_bank_True))  # Балансування індиксів
    print('------------ DataFrame співпадінь -------------')
    print(d_segment_data_description_client_bank_True)
    print('-----------------------------------------------')

    # 1.5.3. Очищення скорингової таблиці від пропусків
    # ------- формування сегменту вхідних даних за рейтингом кліент + банк --------
    b = d_segment_data_description_client_bank_True['Field_in_data']
    d_segment_sample_data_client_bank = d_sample_data[b]
    print('---- пропуски даних сегменту DataFrame --------')
    print(d_segment_sample_data_client_bank.isnull().sum())  # визначення пропусків даних DataFrame
    print('-----------------------------------------------')

    # ------ вилучення строк та індикаторів з пропусками - СКОРИНГОВА КАРТА -------
    # Очищення індикаторів скорингової таблиці
    d_segment_data_description_cleaning = d_segment_data_description_client_bank_True.loc[
        (d_segment_data_description_client_bank_True['Field_in_data'] != 'fact_addr_start_date')]
    d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
        (d_segment_data_description_cleaning['Field_in_data'] != 'position_id')]
    d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
        (d_segment_data_description_cleaning['Field_in_data'] != 'employment_date')]
    d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
        (d_segment_data_description_cleaning['Field_in_data'] != 'has_prior_employment')]
    d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
        (d_segment_data_description_cleaning['Field_in_data'] != 'prior_employment_start_date')]
    d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
        (d_segment_data_description_cleaning['Field_in_data'] != 'prior_employment_end_date')]
    d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
        (d_segment_data_description_cleaning['Field_in_data'] != 'income_frequency_other')]
    d_segment_data_description_cleaning.index = range(0,
                                                      len(d_segment_data_description_cleaning))  # балансування індексів в сегменті 0-n
    d_segment_data_description_cleaning.to_excel(
        'd_segment_data_description_cleaning.xlsx')  # збереження очищених даних

    # Очищення вхідних даних
    d_segment_sample_cleaning = d_segment_sample_data_client_bank.drop(
        columns=['fact_addr_start_date', 'position_id', 'employment_date',
                 'has_prior_employment', 'prior_employment_start_date',
                 'prior_employment_end_date', 'income_frequency_other'])

    d_segment_sample_cleaning.index = range(0, len(d_segment_sample_cleaning))  # балансування індексів в сегменті 0-n
    d_segment_sample_cleaning.to_excel('d_segment_sample_cleaning.xlsx')        # збереження очищених даних
    print('--- Контроль наявності пропусків даних після очищення на індикаторах ---')
    print(d_segment_sample_cleaning.isnull().sum())                             # визначення пропусків даних DataFrame
    print('---------- DataFrame вхідних даних - скорингова карта -----------')
    print(d_segment_sample_cleaning)
    print('----------------- DataFrame індикатори скорингу  ----------------')
    print(d_segment_data_description_cleaning)
    print('-----------------------------------------------------------------')

    return d_segment_sample_cleaning


