'''
Багатокритеріальна скорингова модель для мікрокредитування:
1. Визначення інтегрованого скору клієнтів - пропорційно ймовірності ризику;
2. Бінарний поділ клієнтів на: видача кредиту / відмова в кредиті;
3. Виявлення шахрайства.

'''

from data_parsing import parsing
from data_normalization import normalization
from model import Voronin

if __name__ == '__main__':
    d_segment_sample_cleaning = parsing('sample_data.xlsx', 'data_description.xlsx')    # парсинг даних
    d_segment_sample_minimax_Normal = normalization(d_segment_sample_cleaning)[0]       # нормалізація даних
    d_segment_data_description_minimax = normalization(d_segment_sample_cleaning)[1]    # нормалізація даних

    #------------ аналіз на шахрайство ---------------
    k = len(d_segment_sample_minimax_Normal)                        # повна кількість позичальників
    # k = 260                                                         # кількість позичальників із шахраями
    # k = 150                                                         # кількість позичальників без шахраїв
    # ------------------------------------------------

    Voronin(d_segment_sample_minimax_Normal, d_segment_data_description_minimax, k)     # багатокритеріальна оцінка