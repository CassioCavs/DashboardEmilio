# Importando as bibliotecas necessárias
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# Criando a instância do aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Importando outros módulos do seu aplicativo (verifique a sua implementação real)
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# Definindo URLs e templates de temas para uso posterior
url_theme1 = dbc.themes.CYBORG
url_theme2 = dbc.themes.LUX
template_theme1 = 'cyborg'
template_theme2 = 'lux'

# Carregando os dados do arquivo CSV
df = pd.read_csv('goeldi_2.csv', sep=";")

# Adicionando uma coluna para contar as entradas por ano
df['count'] = 1

# Agrupando o DataFrame pela coluna 'year' e somando as contagens
df_grouped = df.groupby('year')['count'].sum().reset_index()

# Defina o layout da aplicação usando o framework Bootstrap
app.layout = dbc.Container([
    ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
    dbc.Row([
        dbc.Col([
            # Indicadores para as métricas de ocorrência
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='occurrence-metrics',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number",
                                    value=df.shape[0],
                                    title="Occurrences",
                                    number={'suffix': ""},
                                )
                            ],
                            'layout': go.Layout(title='OCCURRENCE METRICS')
                        }
                    ),
                ], width=3),
                dbc.Col([
                    dcc.Graph(
                        id='occurrence-metrics-2',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number",
                                    value=df['acceptedTaxonKey'].notna().sum() / df.shape[0] * 100,
                                    title="With taxon match",
                                    number={'suffix': "%"},
                                )
                            ],
                            'layout': go.Layout(title='')
                        }
                    ),
                ], width=3),
                dbc.Col([
                    dcc.Graph(
                        id='occurrence-metrics-3',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number",
                                    value=df['decimalLatitude'].notna().sum() / df.shape[0] * 100,
                                    title="With coordinates",
                                    number={'suffix': "%"},
                                )
                            ],
                            'layout': go.Layout(title='')
                        }
                    ),
                ], width=3),
                dbc.Col([
                    dcc.Graph(
                        id='occurrence-metrics-4',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number",
                                    value=df['year'].notna().sum() / df.shape[0] * 100,
                                    title="With year",
                                    number={'suffix': "%"},
                                )
                            ],
                            'layout': go.Layout(title='')
                        }
                    ),
                ], width=3),
            ]),
        ])
    ]),

    dbc.Row([

        dbc.Col([
            # Gráfico de linha para mostrar a distribuição de ocorrências por ano
            dcc.Graph(id='occurrences-over-time')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            # Gráfico de pizza para mostrar a distribuição dos reinos
            dcc.Graph(id='kingdom-distribution')
        ]),
        dbc.Col([
            # Gráfico de pizza para mostrar a distribuição dos filos
            dcc.Graph(id='phylum-distribution')
        ]),
        dbc.Col([
            # Gráfico de pizza para mostrar a distribuição das classes
            dcc.Graph(id='class-distribution')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            # Gráfico de pizza para mostrar a distribuição das ordens
            dcc.Graph(id='order-distribution')
        ]),
        dbc.Col([
            # Gráfico de pizza para mostrar a distribuição das famílias
            dcc.Graph(id='family-distribution')
        ])
    ])
])

# Defina o callback para atualizar o gráfico de linha da distribuição de ocorrências ao longo do tempo
@app.callback(
    Output('occurrences-over-time', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_occurrences_over_time(toggle):
    template = template_theme1 if toggle else template_theme2

    # Criar um gráfico de linha para mostrar a distribuição de ocorrências ao longo do tempo
    fig = px.line(df_grouped, x='year', y='count', title='Distribuição de Ocorrências ao Longo do Tempo', template=template)

    return fig

# Defina o callback para atualizar o gráfico de pizza da distribuição dos reinos
@app.callback(
    Output('kingdom-distribution', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_kingdom_distribution(toggle):
    template = template_theme1 if toggle else template_theme2

    # Criar um gráfico de pizza para mostrar a distribuição dos reinos
    kingdom_counts = df['kingdom'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=kingdom_counts.index, values=kingdom_counts.values)])

    fig.update_layout(title='Distribuição dos Reinos', template=template)

    return fig

# Defina o callback para atualizar o gráfico de pizza da distribuição dos filos
@app.callback(
    Output('phylum-distribution', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_phylum_distribution(toggle):
    template = template_theme1 if toggle else template_theme2

    # Criar um gráfico de pizza para mostrar a distribuição dos filos
    phylum_counts = df['phylum'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=phylum_counts.index, values=phylum_counts.values)])

    fig.update_layout(title='Distribuição dos Filos', template=template)

    return fig

# Defina o callback para atualizar o gráfico de pizza da distribuição das classes
@app.callback(
    Output('class-distribution', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_class_distribution(toggle):
    template = template_theme1 if toggle else template_theme2

    # Criar um gráfico de pizza para mostrar a distribuição das classes
    class_counts = df['class'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=class_counts.index, values=class_counts.values)])

    fig.update_layout(title='Distribuição das Classes', template=template)

    return fig

# Defina o callback para atualizar o gráfico de pizza da distribuição das ordens
@app.callback(
    Output('order-distribution', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_order_distribution(toggle):
    template = template_theme1 if toggle else template_theme2

    # Criar um gráfico de pizza para mostrar a distribuição das ordens
    order_counts = df['order'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=order_counts.index, values=order_counts.values)])

    fig.update_layout(title='Distribuição das Ordens', template=template)

    return fig

# Defina o callback para atualizar o gráfico de pizza da distribuição das famílias
@app.callback(
    Output('family-distribution', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_family_distribution(toggle):
    template = template_theme1 if toggle else template_theme2

    # Criar um gráfico de pizza para mostrar a distribuição das famílias
    family_counts = df['family'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=family_counts.index, values=family_counts.values)])

    fig.update_layout(title='Distribuição das Famílias', template=template)

    return fig


# Iniciando o servidor da aplicação
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)