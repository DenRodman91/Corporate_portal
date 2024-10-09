import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import logging
from dash import dash_table
from plotly.subplots import make_subplots
from datetime import timedelta
from dash.dependencies import Input, Output

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# Настройка соединения с базой данных (замените на свои значения)
engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')

# Извлечение данных
def fetch_data():
    query = """
        SELECT `Кабинет`, `ДатаЗаказа`, `Заказы, шт`, `Заказы, руб` FROM СВОД WHERE `ДатаЗаказа` >= CURRENT_DATE() - interval 30 day
    """
    return pd.read_sql(query, engine)

df = fetch_data()
# Преобразование даты, если она не в формате datetime
df['ДатаЗаказа'] = pd.to_datetime(df['ДатаЗаказа'], format='%d-%m-%Y')

def dash(app):
    app.layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='cabinet-filter',
            options=[{'label': i, 'value': i} for i in df['Кабинет'].unique()],
            value=df['Кабинет'].unique(),
            multi=True,
            placeholder="Выберите кабинет"
        ), width=6),
        dbc.Col(dcc.DatePickerRange(
            id='date-filter',
            start_date = (df['ДатаЗаказа'].max() - timedelta(days=10)).date(),
            end_date=df['ДатаЗаказа'].max().date()
        ), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-graph'), width=12)
    ]),
    dbc.Row([
    dbc.Col(dash_table.DataTable(
        id='sales-table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.groupby(['ДатаЗаказа', 'Кабинет']).agg({'Заказы, шт':'sum', 'Заказы, руб':'sum'}).reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'}, # Для горизонтальной прокрутки
    ), lg=6, md=12, xs=12),
])
])

    @app.callback(
        [Output('sales-graph', 'figure'),
        Output('sales-table', 'data'),],

        [Input('cabinet-filter', 'value'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date')]
    )
    def update_graph(selected_cabinets, start_date, end_date):
        filtered_df = fetch_data()
        filtered_df['ДатаЗаказа'] = pd.to_datetime(filtered_df['ДатаЗаказа'])

        if selected_cabinets:
            if not isinstance(selected_cabinets, list):
                selected_cabinets = [selected_cabinets]
            filtered_df = filtered_df[filtered_df['Кабинет'].isin(selected_cabinets)]
        
        filtered_df = filtered_df[(filtered_df['ДатаЗаказа'] >= start_date) & (filtered_df['ДатаЗаказа'] <= end_date)]
        
        # Агрегация данных
        aggregated = filtered_df.groupby('ДатаЗаказа').agg({'Заказы, шт':'sum', 'Заказы, руб':'sum'}).reset_index()

        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Добавление графика продаж в штуках
        fig.add_trace(
            go.Scatter(
                x=aggregated['ДатаЗаказа'], 
                y=aggregated['Заказы, шт'], 
                name='Продажи штук',
                mode='lines+markers',
                line=dict(color='blue'),
                marker=dict(color='blue'),
                fill='tozeroy',
                fillcolor='rgba(255, 248, 4, 0.2)'
            ),
            secondary_y=False,
        )

        # Добавление графика продаж в рублях
        fig.add_trace(
            go.Scatter(
                x=aggregated['ДатаЗаказа'], 
                y=aggregated['Заказы, руб'], 
                mode='lines+markers',
                marker=dict(color='red'),
                line=dict(color='red'),
                fill='tozeroy',
                fillcolor='rgba(255, 0, 0, 0.2)',
                name='Продажи в рублях'
            ),
            secondary_y=True,
        )

        # Настройка шкалы оси Y для продаж в штуках
        fig.update_yaxes(title_text="Продажи штук", range=[500, 1500], secondary_y=False)

        # Настройка заголовков осей и общего заголовка графика
        fig.update_layout(title_text='Продажи по датам')
        fig.update_xaxes(title_text="Дата")
        fig.update_yaxes(title_text="Продажи в рублях", secondary_y=True)


        return fig, filtered_df.groupby(['ДатаЗаказа', 'Кабинет']).agg({'Заказы, шт':'sum', 'Заказы, руб':'sum'}).reset_index().to_dict('records')