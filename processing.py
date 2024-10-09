import sqlite3
import pandas as pd
from datetime import timedelta



def WB_restructure(df, cab, proch_id_):
    df['Дата продажи'] = pd.to_datetime(df['Дата продажи'], errors='coerce')
    df['Дата продажи'].fillna(df['Дата продажи'].max(), inplace=True)
    categ = {
            'ACPK':'Такой то товар',
            }
    categ2 = {'acpk': 'Такой то товар',
 }
    art_dont_touch = ['12345']
    if cab != 'WBPIAT':
        df['Артикул2'] = df['Артикул поставщика'].str[:-1]
    else:
        df['Артикул2'] = df['Артикул поставщика']
    df['Дата продажи'] = pd.to_datetime(df['Дата продажи'], errors='coerce')
    max_date = df['Дата продажи'].max()
    min_date = max_date - timedelta(days=7)
    def process_artikul(artikul):
        if artikul in art_dont_touch:
            return artikul
        else:
            try:
                return ''.join(filter(str.isalpha, artikul))  
            except:
                artikul
    df['Артикул3'] = df['Артикул2'].apply(process_artikul)
    proch_izd= []
    for i in proch_id_:
        if i == '':
            i = "0"
        g = str(i).replace(',', '.')
        proch_izd.append(float(g))
    df['Предмет2'] = df['Артикул3'].map(categ2)


    hran___ = proch_izd[0]
    pl_pr___ = proch_izd[2] 
    reklama___ = proch_izd[1]  
    tranzit___ = proch_izd[3]
    prochie___ = proch_izd[4]
    df['Дата продажи'].fillna(max_date, inplace=True)
    df['Комиссия'] = df['Вайлдберриз реализовал Товар (Пр)'] - df['К перечислению Продавцу за реализованный Товар']
    k = ['продажа', 'авансовая оплата за товар без движения','сторно возвратов','компенсация подмененного товара','частичная компенсация брака','корректная продажа']
    k2  = ['возврат','сторно продаж','авансовая оплата за товар без движения']

    col_vo_pr = (df["Тип документа"].str.lower() == "продажа") & (df["Обоснование для оплаты"].str.lower().isin(k)) 
    col_vo_voz = (df["Тип документа"].str.lower() == "возврат") & (df["Обоснование для оплаты"].str.lower().isin(k2)) 

    col_vo_pr2 = (df["Тип документа"].str.lower() == "продажа") & (df["Обоснование для оплаты"].str.lower().isin(k)) & (df["Дата продажи"] >= min_date) & (df["Дата продажи"] <= max_date)
    col_vo_voz2 = (df["Тип документа"].str.lower() == "позврат") & (df["Обоснование для оплаты"].str.lower().isin(k2)) & (df["Дата продажи"] >= min_date) & (df["Дата продажи"] <= max_date)
    
    filtered_df = df[col_vo_pr]
    filtered_df2 = df[col_vo_voz]

    filtered_df2323 = df[col_vo_pr2]
    filtered_df2232323 = df[col_vo_voz2]

    res_range = filtered_df2323['Кол-во'].sum() - filtered_df2232323['Кол-во'].sum()


    df_rep = pd.DataFrame()
    df_rep1 = df[['Дата продажи', 'Предмет2']]
    df_rep = df_rep1.drop_duplicates(subset=['Дата продажи', 'Предмет2'])

    df_rep['Кабинет'] = cab
   
    df_rep = df_rep.rename(columns={'Дата продажи':'Дата'})
    new_cost = df[df["Обоснование для оплаты"].str.lower() == 'Возмещение издержек по перевозке']['Возмещение издержек по перевозке'].sum()
    dopl = df['Доплаты'].sum()
    strafi = df['Общая сумма штрафов'].sum() 
    
    for i in df['Дата продажи'].unique():
        for it in df['Предмет2'].unique():
            month = str(max_date).split('-')[1]

            test_qaun = (df["Тип документа"].str.lower() == "продажа") & (df["Обоснование для оплаты"].str.lower().isin(k)) & (df["Обоснование для оплаты"].str.lower() != 'частичное возмещение по браку') & (df['Дата продажи'] == i) & (df['Предмет2'] == it)
            test_qaun2 = (df["Тип документа"].str.lower() == "возврат") & (df["Обоснование для оплаты"].str.lower().isin(k2)) &(df["Обоснование для оплаты"].str.lower() != 'частичное возмещение по браку') & (df['Дата продажи'] == i) & (df['Предмет2'] == it)
            filtered_df = df[test_qaun]
            filtered_df2 = df[test_qaun2]
            resu2 = filtered_df['Кол-во'].sum()-filtered_df2['Кол-во'].sum()

            viruchka = filtered_df['Вайлдберриз реализовал Товар (Пр)'].sum()-filtered_df2['Вайлдберриз реализовал Товар (Пр)'].sum()
            
            test_qaun66 = (df["Обоснование для оплаты"].str.lower() == 'частичное возмещение по браку') & (df['Дата продажи'] == i) & (df['Предмет2'] == it)
            test_qaun266 = (df["Обоснование для оплаты"].str.lower() == 'частичное возмещение по браку') & (df['Дата продажи'] == i) & (df['Предмет2'] == it)
            filtered_df3434 = df[test_qaun66]
            filtered_df23434 = df[test_qaun266]
            
            vozmesh_sht = filtered_df3434['Кол-во'].sum()-filtered_df23434['Кол-во'].sum()
            vozmesh = filtered_df3434['Вайлдберриз реализовал Товар (Пр)'].sum()-filtered_df23434['Вайлдберриз реализовал Товар (Пр)'].sum()
            
            conditionLogRF =  (df['Обоснование для оплаты'].str.lower() == "логистика") &  (df['Страна'] == 'Россия') 
            conditionLogINT =  (df['Обоснование для оплаты'].str.lower() == "логистика") &  (df['Страна'] != 'Россия') 
        
            sum_Loh_RF = df.loc[conditionLogRF, 'Услуги по доставке товара покупателю'].sum() - df[(df['Обоснование для оплаты'].str.lower() == "логистика сторно") &  (df['Страна'] == 'Россия') ]['Услуги по доставке товара покупателю'].sum()
            sum_Loh_INT = df.loc[conditionLogINT, 'Услуги по доставке товара покупателю'].sum() - df[(df['Обоснование для оплаты'].str.lower() == "логистика сторно") & (df['Страна'] != 'Россия') ]['Услуги по доставке товара покупателю'].sum()
            


            cond = (df["Тип документа"].str.lower() == "продажа") & (df["Обоснование для оплаты"].str.lower() != "частичное возмещение по браку") & (df['Дата продажи'] == i) & (df['Предмет2'] == it)
            cond2 = (df["Тип документа"].str.lower() == "возврат") & (df["Обоснование для оплаты"].str.lower() != "Частичное возмещение по браку") & (df['Дата продажи'] == i) & (df['Предмет2'] == it)
            filtered_df1 = df[cond]
            filtered_df2 = df[cond2]
            if i >= min_date and i <= max_date:
                hhh = new_cost/res_range
                hranenie = float(hran___)/res_range
                reklama = float(reklama___)/res_range
                pl_priemka_ = float(pl_pr___)/res_range
                tranzit = float(tranzit___)/res_range
                otherOTHER = float(prochie___)/res_range
                sum_Loh_RF = sum_Loh_RF/res_range
                sum_Loh_INT = sum_Loh_INT/res_range
            else:
                sum_Loh_INT = 0 
                sum_Loh_RF = 0
                otherOTHER = 0
                hranenie = 0
                reklama = 0
                pl_priemka_ = 0 
                tranzit = 0
            comis = filtered_df1['Комиссия'].sum()-filtered_df2['Комиссия'].sum()

            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Реализация'] = resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'ВрзвратыНаСкладПоБракуМП'] = vozmesh_sht
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Выручка'] = viruchka
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'ВозмещениеМПзаВозвраты'] = vozmesh
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Комиссия'] = comis
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'ЛогистикаВНУТР'] = sum_Loh_RF*resu2 + hhh*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'ЛогистикаВНЕШ'] = sum_Loh_INT*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Штрафы'] = strafi/res_range*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Доплаты'] = dopl/res_range*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Хранение'] = hranenie*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Реклама'] = reklama*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'СтоимостьПлатнойПриемки'] = pl_priemka_*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'УслугиДоставкиТранзитныхПоставок'] = tranzit*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'ПРОЧИЕпрочие'] = otherOTHER*resu2
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет2'] == it), 'Месяц'] = month


        
    
    conn = sqlite3.connect('db/reports.db')
    df_rep.to_sql('reportsMP', con = conn, index=False, if_exists = 'append')
    df_rounded = df_rep.round(1)
    return df_rounded




def OZ_restructure(df, cab):
    categ = {
            'ACPK':'Такой то товар'
            }
    art_dont_touch = ['12345']
    
    def process_artikul(artikul):
        if artikul in art_dont_touch or artikul == 'nan' or artikul == '':
            return artikul
        else:
            try:
                
                return ''.join(filter(str.isalpha, artikul[:-2]))  
            except:
                artikul
    df['Артикул2'] = df['Артикул'].apply(process_artikul)     

    df['Предмет'] = df['Артикул2'].map(categ)


    df_rep = pd.DataFrame()
    df_rep1 = df[['Дата начисления', 'Предмет']]
    df_rep = df_rep1.drop_duplicates(subset=['Дата начисления', 'Предмет'])
    df_rep['Кабинет'] = cab
    df_rep = df_rep.rename(columns={'Дата начисления':'Дата'})
    df_rep = df_rep.dropna(subset=['Предмет'])
    h = ['Доставка покупателю' ]
    h2 = ['Получение возврата, отмены, невыкупа от покупателя']
    for i in df['Дата начисления'].unique():
        for it in df['Предмет'].unique():
            month = str(i).split('-')[1]
            cond1 = (df["Тип начисления"].isin(h)) & (df['Дата начисления'] == i) & (df['Предмет'] == it)
            cond2 = (df["Тип начисления"].isin(h2)) & (df['Дата начисления'] == i) & (df['Предмет'] == it)
            cond3 = (df['Дата начисления'] == i) & (df['Предмет'] == it)
            cond6 = (df['Дата начисления'] == i)
            cond4 = (df["Тип начисления"] == 'Услуга размещения товаров на складе') & (df['Дата начисления'] == i) & (df['Предмет'] == it)
            cond5 = ((df["Тип начисления"] == 'Услуги продвижения товаров') | (df["Тип начисления"] == 'Продвижение в поиске')) & (df['Дата начисления'] == i)

            cond7 = (df["Тип начисления"].isin(h)) & (df['Дата начисления'] == i) 
            cond8 = (df["Тип начисления"].isin(h2)) & (df['Дата начисления'] == i)

            filtered_df1 = df[cond1]
            filtered_df2 = df[cond2]
            filtered_df4 = df[cond4]
            filtered_df5 = df[cond5]
            filtered_df6 = df[cond6]
            filtered_df7 = df[cond7]
            filtered_df8 = df[cond8]
            real____date = filtered_df1['Количество'].sum()
            real____range = filtered_df7['Количество'].sum()
            real = filtered_df1['Количество'].sum()-filtered_df2['Количество'].sum()
            real2 = filtered_df7['Количество'].sum()-filtered_df8['Количество'].sum()
            filtered_df3 = df[cond3]
            proffit = filtered_df3['За продажу или возврат до вычета комиссий и услуг'].sum()
            comis = filtered_df3['Комиссия за продажу'].sum()
            PR = filtered_df5['Итого'].sum()/real2*real

            logisti = (filtered_df6['Сборка заказа'].sum() + filtered_df6['Обработка отправления (Drop-off/Pick-up) (разбивается по товарам пропорционально количеству в отправлении)'].sum() + filtered_df6['Магистраль'].sum() + filtered_df6['Последняя миля (разбивается по товарам пропорционально доле цены товара в сумме отправления)'].sum() + filtered_df6['Обратная магистраль'].sum() + filtered_df6['Обработка возврата'].sum() + filtered_df6['Обработка отмененного или невостребованного товара (разбивается по товарам в отправлении в одинаковой пропорции)'].sum() + filtered_df6['Обработка невыкупленного товара'].sum() + filtered_df6['Логистика'].sum() + filtered_df6['Обратная логистика'].sum() )/real____range*real____date


            condition_OZ = ((df["Тип начисления"] == "Доставка товаров на склад Ozon (кросс-докинг)") | (df["Тип начисления"] == "Услуга по бронированию места и персонала для поставки с неполным составом в составе ГМ")  | (df["Тип начисления"] == "Услуга размещения товаров на складе")) & (df['Дата начисления'] == i)
            filtered_OZ = df[condition_OZ]
            hranen = filtered_OZ['Итого'].sum()/real____range*real____date

            condition_OZ3 = ((df["Тип начисления"] == "Оплата эквайринга") | (df["Тип начисления"] == "Подписка Premium Plus") | (df["Тип начисления"] == "Утилизация")  | (df["Тип начисления"] == "Корректировки стоимости услуг") | (df["Тип начисления"] == "Услуга по бронированию места и персонала для поставки с неполным составом в составе ГМ")) & (df['Дата начисления'] == i)
            filtered_OZ3 = df[condition_OZ3]
            prochie_uderganiya = filtered_OZ3['Итого'].abs().sum()/real____range*real____date

            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Реализация'] = real____date
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Выручка'] = proffit
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Комиссия'] = abs(comis)
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Логистика'] = abs(logisti)
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Хранение'] = abs(hranen)
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Реклама'] = abs(PR)
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'ПрочиеУдержания'] = abs(prochie_uderganiya)
            df_rep.loc[(df_rep['Дата'] == i) & (df_rep['Предмет'] == it), 'Месяц'] = month
    conn = sqlite3.connect('db/reports.db')
    df_rep.to_sql('reportsOZ', con = conn, index=False, if_exists = 'append')
    df_rounded = df_rep.round(1)


    return df_rounded

def YM_resturture(df, cab):
    pass



def reestrMP(df, cab, proch_izd_ = []):
    if cab in ['cab']:
        ch = WB_restructure(df, cab, proch_izd_)
        return ch
    elif cab in ['cab']:
        ch = OZ_restructure(df, cab)
        return ch
    elif cab in ['cab']:
        ch = YM_resturture(df, cab)
        return ch
