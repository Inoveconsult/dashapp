from dash import html, dcc, Input, Output
from dashapp import app
import plotly.express as px
import plotly.graph_objects as go
from dashapp.df_tratados import df_long, df_proteses_sexo
from dashapp.utils import opcoes_meses

df = df_long.sort_values(['Mes'])
df_sexo = df_proteses_sexo

# listar_meses = list(df['Mes Extenso'].unique())
# listar_meses.append('Todos')
listar_anos = sorted(list(df['Ano'].unique()))

layout_homepage = html.Div(className='homepage', children=[])

layout_desenvolvimento = html.Div(className='development', children=[])

layout_dash = html.Div([ 
    html.Div([ html.Img(src='/assets/imagens/brasil-sorridente.png', alt='Logo'),
             html.H1(children='PROGRAMA BRASIL SORRIDENTE')], className='titulo'),

    html.Div(children='''
        Laboratório de Próteses Dentárias - LRPD
    ''', className="subtitulo"),
    
    html.Div(children=[
        html.Div(children=[html.Label('Selecione o Ano'), dcc.RadioItems(listar_anos, value='2024', id='selecao_ano')], className='container-radio'),
     
        html.Div(children=[ html.Label('Selecione o Mês'), dcc.Dropdown(value='Todos', id='selecao_meses')], style={'text-transform':'uppercase'})      
    ], className='topo'),    
    
    html.Div(children=[dcc.Graph(id='grafico_metas', className='item-grafico'),
                       dcc.Graph(id='grafico_mensal', className='item-grafico')], className='container-grafico'),
   
    html.Div(children=[dcc.Graph(id='grafico_procedimentos', className='item-grafico'),
                       dcc.Graph(id='grafico_sexo', className='item-grafico')], className='container-grafico'),      
   
], className='page-container'),

    #  html.Div(children=[
    #   dcc.Graph(id='grafico_mensal')]),
    
 
   

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
   html.Div([
        # Botão para toggle do menu
        html.Div([
            html.Button("Toggle Menu", id="toggle-button", n_clicks=0),  
    
    # Menu lateral que será ocultado ou mostrado
            html.Div(id="sidebar", children=[
                html.H2("AMBULATÓRIO", style={'textAlign': 'center'}),
                html.Hr(),
                dcc.Link("Brasil Sorridente", "/dashboard", style={'padding': '10px', 'display': 'block'}, className='opcoes-menu'),
                dcc.Link("Urgência / Emergência", "/development", style={'padding': '10px', 'display': 'block'}, className='opcoes-menu'),
                dcc.Link("Exames Laboratóriais", "/development", style={'padding': '10px', 'display': 'block'}, className='opcoes-menu'),
                dcc.Link("Radiologia", "/development", style={'padding': '10px', 'display': 'block'}, className='opcoes-menu'),
                dcc.Link("Citologia","/development", style={'padding': '10px', 'display': 'block'}, className='opcoes-menu'),
                
                html.H2("HOSPITALAR", style={'textAlign': 'center'}),
                html.Hr(),
                dcc.Link("Internações /Leito", "/development", style={'padding': '10px', 'display': 'block'}, className='opcoes-menu'),
            ], style={'width': '200px', 'position': 'absolute', 'background-color': '#f8f9fa', 'padding': '10px', 'display': 'none'})        
            ], className='botao-container'),
            dcc.Link(html.Img(src='/assets/imagens/home.png', alt='Logo', className='logo-home'), "/"),
            html.Div(html.H1('VERSÃO DE DESENVOLVIMENTO'), className='barra'),
       
    ], className='top-container'),
    
    html.Div(id='conteudo_pagina'),
    
    html.Footer(        
        children=[
            html.Div([
                html.Div([html.P("© 2024 - Inove Consultoria. Todos os direitos reservados.")], className='grid-itens'),          
                # html.Div([html.P("© 2024 Minha Aplicação. Todos os direitos reservados.")], className='grid-itens'),          
                # html.Div([html.P("© 2024 Minha Aplicação. Todos os direitos reservados.")], className='grid-itens'),          
            ], className='grid-container'),
                    
        ], className='footer')                  
],)


# Callback para links
@app.callback(Output('conteudo_pagina', 'children'), Input('url','pathname'))
def carregar_pagina(pathname):
    if pathname == '/':
        return layout_homepage
    elif pathname =='/dashboard':
        return layout_dash
    elif pathname == '/development':
        return layout_desenvolvimento

# Callback para alternar a visibilidade do menu lateral
@app.callback(
    Output("sidebar", "style"),
    Output("toggle-button", "children"),
    Output("toggle-button", "style"),
    Input("toggle-button", "n_clicks"),
)
def toggle_sidebar(n_clicks):
    if n_clicks % 2 == 1:  # Se for ímpar, mostra o menu
        img = html.Img(src="assets/imagens/cardapio.png", style={"height": "25px", "width": "25px"})
        return {'width': '200px', 'height': '83vh', 'position': 'absolute', 'background-color': '#240d8f', 'padding': '10px','color':'white'}, [img, "Menu Close"], {"width": "220px", "height": "40px"}
    else:  # Se for par, oculta o menu
        img = html.Img(src="assets/imagens/cardapio.png", style={"height": "25px", "width":"25px"})
        return {'display': 'none'}, [img, "Menu"], {"width": "100px", "height": "40px"}

@app.callback(
    Output('selecao_meses', 'value'),
    Output('selecao_meses', 'options'), 
    Input('selecao_ano', 'value'))   
def listar_meses(ano_atual): 
    if ano_atual is None or ano_atual not in df['Ano'].unique():
        return [], None  # Retorna lista vazia se o ano não for válido       
    df_meses = df.loc[df['Ano'] == ano_atual, :]
    df_meses = df_meses.sort_values(['Mes'])
    listagem = list(df_meses['Mes Extenso'].unique())
    listagem.append('Todos')    
    lista_inicial = 'Todos'
    return lista_inicial, listagem
        
#Secao de Callbacks
@app.callback(Output('grafico_mensal', 'figure'), Input('selecao_ano', 'value'))
def selecionar_ano(ano):
    if ano == '2024': 
        df_filtrado = df_long.sort_values(['Mes'])
        df_filtrado = df.loc[df_filtrado['Ano']== ano, : ]
        df_agrupado = df_filtrado.groupby(['Mes','Mes Extenso'], as_index=False)['Quantidade'].sum()
        cores_alternadas = [
            '#e335ee',  # Vermelho Alaranjado
            '#00a382',  # Verde
            '#3357FF',  # Azul
            '#FF33A1',  # Rosa
            '#FFBD33',  # Laranja
            '#ff4024',  # Verde Limão
            '#33FFF6',  # Ciano
            '#9933FF',  # Roxo
            '#FF3380',  # Rosa Choque
            '#33FFBD',  # Verde Água
            '#FFD433',  # Amarelo
            '#3375FF'   # Azul Celeste
        ]
        cores = [cores_alternadas[i % len(cores_alternadas)] for i in range(len(df_agrupado))]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_agrupado['Mes Extenso'],  # Rótulos dos meses por extenso
            y=df_agrupado['Quantidade'],   # Valores da quantidade
            marker=dict(color=cores),  # Cor das barras
            text=df_agrupado['Quantidade'],  # Mostrar o valor sobre as barras
            textposition='auto'  # Posição automática do texto (dentro das barras)
        ))
        # Ajustar o layout do gráfico
        fig.update_layout(
            title={'text': f"Quantidade por Mês - Ano {ano}".upper()},  # Título dinâmico com base no ano
            title_x=0.5,
            title_font=dict(size=20),
            xaxis_title='Mês Extenso',
            yaxis_title='Quantidade',
            width=700,   # Largura do gráfico (em pixels)
            height=340,  # Altura do gráfico (em pixels)
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo geral transparente
            plot_bgcolor='rgba(0,0,0,0)',    # Fundo da área de plotagem transparente
            bargap=0.2,  # Ajustar o espaçamento entre as barras
            font=dict(family='Arial', size=15),  # Tamanho da fonte
            template="plotly_white"  # Tema do gráfico
        )
        labels = df_filtrado['Procedimentos realizados']
        values = df_filtrado['Quantidade']

        # Puxar algumas fatias
        pull = [0.1, 0.3, 0.1, 0.2]  # Aumenta a aparência das fatias 'Frogs' e 'Hogs'

        # Criando o gráfico
        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull)])

            # Título
        fig1.update_layout(title='Proporção de Procedimentos Realizados') 
                       
    else:        
        df_filtrado = df_long.sort_values(['Mes'])
        df_filtrado = df[df['Ano']== ano]
        df_agrupado = df_filtrado.groupby(['Mes','Mes Extenso'], as_index=False)['Quantidade'].sum()
        cores_alternadas = [
            '#e335ee',  # Vermelho Alaranjado
            '#00a382',  # Verde
            '#3357FF',  # Azul
            '#FF33A1',  # Rosa
            '#FFBD33',  # Laranja
            '#ff4024',  # Verde Limão
            '#33FFF6',  # Ciano
            '#9933FF',  # Roxo
            '#FF3380',  # Rosa Choque
            '#33FFBD',  # Verde Água
            '#FFD433',  # Amarelo
            '#3375FF'   # Azul Celeste
        ]
        cores = [cores_alternadas[i % len(cores_alternadas)] for i in range(len(df_agrupado))]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_agrupado['Mes Extenso'],  # Rótulos dos meses por extenso
            y=df_agrupado['Quantidade'],   # Valores da quantidade
            marker=dict(color=cores),  # Cor das barras
            text=df_agrupado['Quantidade'],  # Mostrar o valor sobre as barras
            textposition='auto'  # Posição automática do texto (dentro das barras)
        ))
        # Ajustar o layout do gráfico
        fig.update_layout(
            title={'text':f"Quantidade por Mês - Ano {ano}".upper()},  # Título dinâmico com base no ano
            title_x=0.5,
            title_font=dict(size=20),
            xaxis_title='Mês Extenso',
            yaxis_title='Quantidade',
            width=700,   # Largura do gráfico (em pixels)
            height=340,  # Altura do gráfico (em pixels)
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo geral transparente
            plot_bgcolor='rgba(0,0,0,0)',    # Fundo da área de plotagem transparente
            bargap=0.2,  # Ajustar o espaçamento entre as barras
            font=dict(family='Arial',size=15),  # Tamanho da fonte
            template="plotly_white"  # Tema do gráfico            
        )         
    return fig
    
@app.callback(  
    Output('grafico_metas', 'figure'),
    Output('grafico_procedimentos', 'figure'),
    Output('grafico_sexo', 'figure'),       
    Input('selecao_ano', 'value'),    
    Input('selecao_meses', 'value')    
)
def ver_procedimentos(ano, mes):    
    if ano == '2024' and mes == 'Todos': 
        df_filtrado = df_long.sort_values(['Mes'])        
        df_filtrado = df_filtrado.loc[df_filtrado['Ano'] == ano, :]
        
        labels = list(df_filtrado['Procedimentos realizados'].unique())
        values = df_filtrado['Quantidade']

        # Puxar algumas fatias
        pull = [0.1, 0.1, 0.1, 0.1]  # Aumenta a aparência das fatias 'Frogs' e 'Hogs'

            # Criando o gráfico
        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull)])

            # Título
        fig1.update_layout(
            title={'text':f"Proporção de Procedimentos Realizados - {ano}".upper()},
            title_x=0.5,
            title_font=dict(size=20),
            width=600,  # Largura do gráfico
            height=390,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)',
            # legend=dict(
            # rientationo='h',  # Colocar a legenda na horizontal
            # yanchor='bottom',  # Ancorar a legenda na parte inferior
            # y=-0.2,           # Posição abaixo do gráfico
            # xanchor='center',  # Centralizar a legenda horizontalmente
            # x=0.5             # Posição no centro horizontalmente
            # )
            ) 
        fig1.update_traces(  # Exibe o rótulo e a porcentagem
                    textfont=dict(size=14))  # Aumenta o tamanho da fonte dentro das fatias
        
        #GRAFICO DE INDICADOR
       # Valor atual, mínimo, máximo e meta
        valor_atual = df_filtrado['Quantidade'].sum()+0 
        valor_minimo = 0
        valor_maximo = 960
        meta = 612

        fig2= go.Figure(go.Indicator(
            mode="gauge+number",
            value=valor_atual,
            title={'text': f"META ANUAL - {ano}"},
            title_font=dict(size=20),            
            # number_font=dict(size=40),
            gauge={
                'axis': {
                    'range': [valor_minimo, valor_maximo],  # Define o intervalo mínimo e máximo
                    'tickvals': [valor_minimo, meta, valor_maximo],  # Coloca as marcações no eixo
                    'ticktext': [f"Min ({valor_minimo})", f"Meta ({meta})", f"Max ({valor_maximo})"],  # Texto das marcações
                    'tickfont': {'size': 13.5},
                },
                'steps': [
                    {'range': [valor_minimo, meta * 0.20], 'color': "red"},  # Até 50% da meta
                    {'range': [meta * 0.21, meta * 0.50], 'color': "orange"},      # Entre 50% e 75% da meta
                    {'range': [meta * 0.51, meta * 0.74], 'color': "yellow"},            # Entre 75% e a meta
                    {'range': [meta * 0.75, meta], 'color': "#008cff"},
                    {'range': [meta, valor_maximo], 'color': "#131a9e"}# Acima da meta                    
                ],
                'threshold': {
                    'line': {'color': "#f9f871", 'width': 5},  # Linha da meta
                    'thickness': 0.99,
                    'value': meta  # Valor da meta
                }
            },
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig2.update_layout(
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        
        #GRAFICO POR SEXO
        df_filtrado_sexo = df_proteses_sexo[df_proteses_sexo['Ano'] == ano]
        df_agrupado = df_filtrado_sexo.groupby('Sexo', as_index=False)['Quantidade'].sum()
        # df_filtrado_sexo = df_proteses_sexo[df_proteses_sexo['Mes Extenso'] == mes]
        sexos = list(df_filtrado_sexo['Sexo'].unique())
        quantidades = df_agrupado['Quantidade'] 
                # Criar o gráfico de barras
        fig3 = go.Figure()

                # Adicionar a barra para cada sexo
        fig3.add_trace(go.Bar(
            x=sexos,
            y=quantidades,
            marker_color=['#ffcbdb', '#007dcc'],  # Cores personalizadas para cada barra
            text=quantidades,  # Exibir os valores das quantidades
            textposition='auto'
            ))

                # Atualizar o layout do gráfico
        fig3.update_layout(
            title={'text': f"Quantidade de Atendimento por Sexo - {ano}".upper()},
            title_x=0.5,
            title_font=dict(size=20),
            xaxis_title="Sexo",
            yaxis_title="Quantidade de Atendimentos",
            bargap=0.2,  # Espaçamento entre as barras
            yaxis=dict(range=[0, max(quantidades) * 1.2]),  # Definir o intervalo do eixo y
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)')
        fig3.update_traces(textfont=dict(
        family='Arial',  # Altere para a fonte desejada
        size=14  # Tamanho da fonte
        
        ))                   
    elif mes != 'Todos':           
        df_filtrado = df_long.sort_values(['Mes'])
        df_filtrado = df_filtrado.loc[df_filtrado['Ano'] == ano, :]        
        df_filtrado = df_filtrado.loc[df_filtrado['Mes Extenso'] == mes, :]
                   
        #Inicia gráfico        
        labels = list(df_filtrado['Procedimentos realizados'].unique())
        values = df_filtrado['Quantidade']

        # Puxar algumas fatias
        pull = [0.1, 0.1, 0.1, 0.1]  # Aumenta a aparência das fatias 'Frogs' e 'Hogs'

        # Criando o gráfico
        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull)])

        # Título
        fig1.update_layout(
            title={'text':f"Proporção de Procedimentos Realizados - {ano}".upper()},
            title_x=0.5,
            title_font=dict(size=20),
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)',
            # legend=dict(
            # orientation='h',  # Colocar a legenda na horizontal
            # yanchor='bottom',  # Ancorar a legenda na parte inferior
            # y=-0.2,           # Posição abaixo do gráfico
            # xanchor='center',  # Centralizar a legenda horizontalmente
            # x=0.5             # Posição no centro horizontalmente
            # )
            ) 
        fig1.update_traces(  # Exibe o rótulo e a porcentagem
                    textfont=dict(size=14))  # Aumenta o tamanho da fonte dentro das fatias      
        
        #GRAFICO DE INDICADOR
        # Valor atual, mínimo, máximo e meta
        valor_atual = df_filtrado['Quantidade'].sum()
        valor_minimo = 0
        valor_maximo = 80
        meta = 51

        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=valor_atual,
            title={'text': f"META MENSAL - {mes} / {ano}"},
            gauge={
                'axis': {
                    'range': [valor_minimo, valor_maximo],  # Define o intervalo mínimo e máximo
                    'tickvals': [valor_minimo, meta, valor_maximo],  # Coloca as marcações no eixo
                    'ticktext': [f"Min ({valor_minimo})", f"Meta ({meta})", f"Max ({valor_maximo})"]  # Texto das marcações
                },
                'steps': [
                    {'range': [valor_minimo, meta * 0.20], 'color': "red"},  # Até 50% da meta
                    {'range': [meta * 0.21, meta * 0.50], 'color': "orange"},      # Entre 50% e 75% da meta
                    {'range': [meta * 0.51, meta * 0.74], 'color': "yellow"},            # Entre 75% e a meta
                    {'range': [meta * 0.75, meta], 'color': "#131a9e    "},
                    {'range': [meta, valor_maximo], 'color': "#ad94c8"}# Acima da meta
                ],
                'threshold': {
                    'line': {'color': "#f9f871", 'width': 5},  # Linha da meta
                    'thickness': 0.75,
                    'value': meta  # Valor da meta
                }
            },
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig2.update_layout(
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        #GRAFICO POR SEXO
        df_filtrado_sexo = df_proteses_sexo.loc[df_proteses_sexo['Ano'] == ano, :]
        df_filtrado_sexo = df_filtrado_sexo.loc[df_proteses_sexo['Mes Extenso'] == mes, :]
        sexos = list(df_filtrado_sexo['Sexo'].unique())
        quantidades = df_filtrado_sexo['Quantidade']  # Quantidade total de procedimentos por sexo
                # Criar o gráfico de barras
        fig3 = go.Figure()

                # Adicionar a barra para cada sexo
        fig3.add_trace(go.Bar(
            x=sexos,
            y=quantidades,
            marker_color=['#ffcbdb', '#007dcc'],  # Cores personalizadas para cada barra
            text=quantidades,  # Exibir os valores das quantidades
            textposition='auto'
            ))

                # Atualizar o layout do gráfico
        fig3.update_layout(
            title={'text': f"Quantidade de Atendimento por Sexo - {ano}".upper()},
            title_x=0.5,
            title_font=dict(size=20),
            xaxis_title="Sexo",
            yaxis_title="Quantidade de Atendimentos",
            bargap=0.2,  # Espaçamento entre as barras
            yaxis=dict(range=[0, max(quantidades) * 1.2]),  # Definir o intervalo do eixo y
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)'            
        )
        fig3.update_traces(textfont=dict(
        family='Arial',  # Altere para a fonte desejada
        size=14  # Tamanho da fonte        
        ))                 
    else:
        df_filtrado = df_long.sort_values(['Mes'])
        df_filtrado = df_filtrado[df_filtrado['Ano'] == ano]                
                   
        #Inicia gráfico        
        labels = df_filtrado['Procedimentos realizados']
        values = df_filtrado['Quantidade']

        # Puxar algumas fatias
        pull = [0.1, 0.3, 0.1, 0.2]  # Aumenta a aparência das fatias 'Frogs' e 'Hogs'

        # Criando o gráfico
        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull)])

        # Título
        fig1.update_layout(
            title={'text':f"Proporção de Procedimentos Realizados - {ano}".upper()},
            title_x=0.5,
            title_font=dict(size=20),
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)',
            # legend=dict(
            # orientation='h',  # Colocar a legenda na horizontal
            # yanchor='bottom',  # Ancorar a legenda na parte inferior
            # y=-0.2,           # Posição abaixo do gráfico
            # xanchor='center',  # Centralizar a legenda horizontalmente
            # x=0.5             # Posição no centro horizontalmente
            # )
            ) 
        fig1.update_traces(  # Exibe o rótulo e a porcentagem
                    textfont=dict(size=14))  # Aumenta o tamanho da fonte dentro das fatias 
        
        #GRAFICO DE INDICADOR
        valor_atual = df_filtrado['Quantidade'].sum() 
        valor_minimo = 0
        valor_maximo = 80
        meta = 51

        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=valor_atual,
            title={'text': f"META ANUAL - {ano}"},
            title_font=dict(size=20),
            gauge={
                'axis': {
                    'range': [valor_minimo, valor_maximo],  # Define o intervalo mínimo e máximo
                    'tickvals': [valor_minimo, meta, valor_maximo],  # Coloca as marcações no eixo
                    'ticktext': [f"Min ({valor_minimo})", f"Meta ({meta})", f"Max ({valor_maximo})"]  # Texto das marcações
                },
                'steps': [
                    {'range': [valor_minimo, meta * 0.20], 'color': "red"},  # Até 50% da meta
                    {'range': [meta * 0.21, meta * 0.50], 'color': "orange"},      # Entre 50% e 75% da meta
                    {'range': [meta * 0.51, meta * 0.74], 'color': "yellow"},            # Entre 75% e a meta
                    {'range': [meta * 0.75, meta], 'color': "#131a9e"},
                    {'range': [meta, valor_maximo], 'color': "#ad94c8"}# Acima da meta
                ],
                'threshold': {
                    'line': {'color': "#f9f871", 'width': 5},  # Linha da meta
                    'thickness': 0.75,
                    'value': meta  # Valor da meta
                }
            },
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig2.update_layout(
            width=600,  # Largura do gráfico
            height=340,  # Altura do gráfico
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        df_filtrado_sexo = df_proteses_sexo[df_proteses_sexo['Ano'] == ano]
        df_filtrado_sexo = df_filtrado_sexo.sort_values(['Sexo'])
        df_agrupado = df_filtrado_sexo.groupby('Sexo', as_index=False)['Quantidade'].sum()
        sexos = list(df_filtrado_sexo['Sexo'].unique())
        quantidades = df_agrupado['Quantidade']  # Quantidade total de procedimentos por sexo
        # Criar o gráfico de barras
        fig3 = go.Figure()

        # Adicionar a barra para cada sexo
        fig3.add_trace(go.Bar(
            x=sexos,
            y=quantidades,
            marker_color=['#ee3599', '#007dcc'],  # Cores personalizadas para cada barra
            text=quantidades,  # Exibir os valores das quantidades
            textposition='auto'
            ))

        # Atualizar o layout do gráfico
        fig3.update_layout(
            title={'text': f"Quantidade de Atendimento por Sexo - {ano}".upper()},
            title_x=0.5,
            title_font=dict(size=20),
            xaxis_title="Sexo",
            yaxis_title="Quantidade de Atendimentos",
            bargap=0.2,  # Espaçamento entre as barras
            yaxis=dict(range=[0, max(quantidades) * 1.2]),  # Definir o intervalo do eixo y
            width=600,   # Largura do gráfico (em pixels)
            height=340,  # Altura do gráfico (em pixels)
            paper_bgcolor='rgba(0,0,0,0)',  # Fundo geral transparente
            plot_bgcolor='rgba(0,0,0,0)'    # Fundo da área de plotagem transparente
          )
        fig3.update_traces(textfont=dict(
        family='Arial',  # Altere para a fonte desejada
        size=14  # Tamanho da fonte        
        ))  
 
    return fig2, fig1, fig3  