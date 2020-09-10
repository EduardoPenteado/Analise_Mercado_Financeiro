#!/usr/bin/env python
# coding: utf-8

# In[1]:


## """Análise utilizando a biblioteca plotly"""
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline as iplot
import requests
from urllib.request import Request, urlopen

"""
Como usar? 
1. É necessário uma interface de visualização de dados e gráficos como o Jupyter Notebook;
2. O código é bem intuitivo, possui uma espécie de interface que facilita a navegação do usuário;
3. Na primeira vez que o código funcionar, pode-ser que demora um pouco, porém, será somente na primeira vez;
4. Escolha a análise e siga as intruções corretamente, digite corretamente a ação ou correspondente que será analisado.
"""

class All_bonds():
    """
    Classe que obtém todas as ações listadas no IBOV e o seu respectivo setor de atuação.
    Os dados são salvos em um arquivo excel para otimizar a leitura do algoritmo
    """
    def Setores(self):
        try:
            # Se o programa já rodou alguma, ele inicializa pelo arquivo em excel criado.
            self.df_setor = pd.read_excel('Setores.xlsx')
            print("Loading ...")
        except FileNotFoundError:
            # Criação do arquivo em excel com as ações e seus respectivos setores.
            url = "http://www.fundamentus.com.br/detalhes.php"
            req = Request(url, headers={'User-Agent': 'Chrome/84.0.4147.105'})
            webpage = urlopen(req).read()
            # Forma mais simples de remover os pontos separando os milhares.
            df = pd.read_html(webpage)
            df = df[0]
            # Criando um dicionário mostrando o setor de cada empresa
            ano_atual = int(datetime.today().strftime('%Y'))
            mes_atual = int(datetime.today().strftime('%m'))
            dia_atual = int(datetime.today().strftime('%d'))
            cot_atual = datetime(year=ano_atual,month=mes_atual,day=dia_atual-1)
            cot_atual = cot_atual.strftime('%d/%m/%Y')
            setor = []
            print("Loading ...")
            for i in range(0,len(df)):
                url1 = "http://www.fundamentus.com.br/detalhes.php?papel="+df.loc[i]['Papel']
                req = Request(url1, headers={'User-Agent': 'Chrome/84.0.4147.105'})
                webpage = urlopen(req).read()
                self.df_setor = pd.read_html(webpage)
                self.df_setor = self.df_setor[0]
                try:
                    if self.df_setor.loc[1][3] == str(cot_atual) :
                        # Algumas empresas estão com setor vazio, sendo necessário o código abaixo para correção
                        nan_rows = self.df_setor[self.df_setor.isnull().any(1)]
                        try: 
                            nan_rows[1][3]
                            self.df_setor[1][3] = 'Undefined'
                            setor.append((df.loc[i]['Papel'],self.df_setor.loc[3][1]))
                        except Exception:
                            setor.append((df.loc[i]['Papel'],self.df_setor.loc[3][1]))
                    else:
                        None
                except Exception:
                    None
            print('Loading Complete!')
            self.df_setor = pd.DataFrame(setor)
            self.df_setor.to_excel('Setores.xlsx')
            
        self.df_setor.drop(self.df_setor.columns[0],axis=1,inplace=True)
        self.df_setor.rename(columns={0: "Papel", 1: "Setor"}, inplace = True)
        return self.df_setor

class Bond_Analisys(All_bonds):    
    
    """
    Algoritmo que analisa as ações e correlatos.
    """
    
    def __init__(self):
        # Obtém o dataframe com as ações e os setores correspondentes.
        self.Setores()
    
    def initialize(self):
        # Interface para facilitar o uso do algoritmo.
        resp = ''
        while resp != 'quit':
            print('-----Bem Vindo ao HomeBroker!-----\n'+
                   'Digite uma das opções de análises\n'+
                   '[1] Ação Brasileira\n'+
                   '[2] Ação Americana\n'+
                   '[3] Índice\n'+
                   '[4] Moeda\n'+
                   '[5] Criptomoeda\n'+
                 '* Digite "quit" para sair a qualquer momento')
            resp = input('').lower()
            resp2 = ''
            if resp == str(1):
                while resp2 != 'BACK':
                    print('Digite uma das opções de análises\n'+
                       '[1] Candlestick\n'+
                       '[2] Análise Médias\n'+
                       '[3] Médias de High & Low\n'+
                       '[4] Fundamentalista\n'+
                       '[5] Volume\n'+
                       '[6] Oscilações\n'+
                       '[7] TreeMap Variação Diária\n'+
                       '[8] Comparação\n'+
                       '[9] Dividendos\n'+
                       '[10] Setor\n'+
                       '[11] Todas\n'+
                       '* Digite "back" para voltar')
                    resp2 = input('').upper()
                    if resp2 != 'BACK':
                        if resp2 != str(7):
                            if resp2 != str(10):
                                ação = []
                                self.ação = input("Ação a ser analisada: \nExemplo(MGLU3, VALE3, PETR4 ...)").upper()
                                self.bond = yf.download(self.ação +'.SA', end=datetime.today())
                                self.bond['Date'] = self.bond.index
                                ação.append(self.ação)
                    if resp2 == str(1):
                        self.Candlestick(resp)
                    elif resp2 == str(2):
                        self.Análise_Media(resp)
                    elif resp2 == str(3):
                        self.Traces()
                    elif resp2 == str(4):
                        self.Analise_Fundamentalista(ação)
                    elif resp2 == str(5):
                        self.Volume_Analisys()
                    elif resp2 == str(6):
                        self.Oscilações()
                    elif resp2 == str(7):
                        print('Digite o período desejado para a análise:\n'+
                             '[1] Dia\n'+
                             '[2] Mês\n'+
                             '[3] YTD\n')
                        resp3 = input('')
                        self.Variações_Diária(resp3)
                    elif resp2 == str(8):
                        self.Comparação(resp)
                    elif resp2 == str(9):
                        self.Dividends()
                    elif resp2 == str(10):
                        self.Setor()
                    elif resp2 == str(11):
                        self.Candlestick(resp)
                        self.Análise_Media(resp)
                        self.Traces()
                        self.Analise_Fundamentalista()
                        self.Volume_Analisys()
                        self.Oscilações()
                        self.Comparação(resp)
                    else:
                        None
            elif resp == str(2):
                while resp2 != "BACK":
                    print('Digite uma das opções de análises\n'+
                           '[1] Candlestick\n'+
                           '[2] Análise Médias\n'+
                           '[3] Médias de High & Low\n'+
                           '[4] Oscilações\n'+
                           '[5] Comparação\n'+
                           '[6] Todas\n'+
                           '* Digite "back" para voltar')
                    resp2 = input('').upper()
                    if resp2 != 'BACK':
                        self.ação = input("Ação a ser analisada: \n"+'Exemplo (AAPL, TSLA, GOOG ...)').upper()
                        self.bond = yf.download(self.ação, end=datetime.today())
                        self.bond['Date'] = self.bond.index
                    if resp2 == str(1):
                        self.Candlestick(resp)
                    elif resp2 == str(2):
                        self.Análise_Media(resp)
                    elif resp2 == str(3):
                        self.Traces()
                    elif resp2 == str(4):
                        self.Oscilações()
                    elif resp2 == str(5):
                        self.Comparação(resp)
                    elif resp2 == str(6):
                        self.Candlestick(resp)
                        self.Análise_Media(resp)
                        self.Traces()
                        self.Oscilações()
                        self.Comparação(resp)
                    else:
                        None
            elif resp == str(3):
                while resp2 != "BACK":
                    print('Digite uma das opções de análises\n'+
                           '[1] Candlestick\n'+
                           '[2] Análise Médias\n'+
                           '[3] Médias de High & Low\n'+
                           '[4] Oscilações\n'+
                           '[5] Todas\n'+
                           '* Digite "back" para voltar')
                    resp2 = input('').upper()
                    if resp2 != 'BACK':
                        self.ação = input("Ação a ser analisada: \n"+'Exemplo (BVSP, GSPC, VIX  ...)')
                        self.bond = yf.download('^'+self.ação, end=datetime.today())
                        self.bond['Date'] = self.bond.index
                    if resp2 == str(1):
                        self.Candlestick(resp)
                    elif resp2 == str(2):
                        self.Análise_Media(resp)
                    elif resp2 == str(3):
                        self.Traces()
                    elif resp2 == str(4):
                        self.Oscilações()
                    elif resp2 == str(5):
                        self.Candlestick(resp)
                        self.Análise_Media(resp)
                        self.Traces()
                        self.Oscilações()
                    else:
                        None
            elif resp == str(4):
                while resp2 != "BACK":
                    print('Digite uma das opções de análises\n'+
                           '[1] Candlestick\n'+
                           '[2] Análise Médias\n'+
                           '[3] Médias de High & Low\n'+
                           '[4] Oscilações\n'+
                           '[5] Todas\n'+
                           '* Digite "back" para voltar')
                    resp2 = input('').upper()
                    if resp2 != 'BACK':
                        self.ação = input("Ação a ser analisada: \n"+'Exemplo (BRL, BRLEUR, BRLUSD ...)')
                        self.bond = yf.download(self.ação+"=X", end=datetime.today())
                        self.bond['Date'] = self.bond.index
                    if resp2 == str(1):
                        self.Candlestick(resp)
                    elif resp2 == str(2):
                        self.Análise_Media(resp)
                    elif resp2 == str(3):
                        self.Traces()
                    elif resp2 == str(4):
                        self.Oscilações()
                    elif resp2 == str(5):
                        self.Candlestick(resp)
                        self.Análise_Media(resp)
                        self.Traces()
                        self.Oscilações()
                    else:
                        None
            elif resp == str(5):
                while resp2 != "BACK":
                    print('Digite uma das opções de análises\n'+
                           '[1] Candlestick\n'+
                           '[2] Análise Médias\n'+
                           '[3] Médias de High & Low\n'+
                           '[4] Oscilações\n'+
                           '[5] Todas\n'+
                           '* Digite "back" para voltar')
                    resp2 = input('').upper()
                    if resp2 != 'BACK':
                        self.ação = input("Ação a ser analisada: \n"+'Exemplo (BTC, ETH ...)')
                        self.bond = yf.download(self.ação+"-USD", end=datetime.today())
                        self.bond['Date'] = self.bond.index
                    if resp2 == str(1):
                        self.Candlestick(resp)
                    elif resp2 == str(2):
                        self.Análise_Media(resp)
                    elif resp2 == str(3):
                        self.Traces()
                    elif resp2 == str(4):
                        self.Oscilações()
                    elif resp2 == str(5):
                        self.Candlestick(resp)
                        self.Análise_Media(resp)
                        self.Traces()
                        self.Oscilações()
                    else:
                        None
            
    def Bond_SelectorButton(self, fig):
        # Adiciona nos gráficos botôes para periodos específicos ('1 Dia, 1 Mês, Year to Date ...)
        fig.update_xaxes(
                    rangeslider_visible = True,
                    rangeselector = dict(
                        buttons=list([
                            dict(count=1, label='1D', step='day', stepmode='backward'),
                            dict(count=5, label='5D', step='day', stepmode='backward'),
                            dict(count=1, label='1M', step='month', stepmode='backward'),
                            dict(count=3, label='3M', step='month', stepmode='backward'),
                            dict(count=6, label='6M', step='month', stepmode='backward'),
                            dict(count=1, label='1Y', step='year', stepmode='backward'),
                            dict(count=5, label='5Y', step='year', stepmode='backward'),
                            dict(count=11, label='Todos', step='year', stepmode='backward'),
                            dict(count=1, label='YTD', step='year', stepmode='todate') ]))
                        )
        
    def Fig_Update(self, fig, resp):
        #Arruma os eixos do gráfico, de acordo  com a ação ser brasileira ou americana
        self.resp = resp
        if self.resp == str(2) or self.resp == str(5):
            fig.update_yaxes(tickprefix="$")
            fig.update_layout(yaxis = dict(title_text = "Price",
                                           title_standoff = 25))
        else:
            fig.update_yaxes(tickprefix="R$")
            fig.update_layout(yaxis = dict(title_text = "Preço",
                                           title_standoff = 25))
        
    def Covid_Notation(self, fig):
        # Adicionado um marcador no gráfico no inicio do impacto da COVID-19 no Brasil.
        fig.update_layout(
                            shapes = [dict(x0='2020-03-04', x1='2020-03-04', y0=0, y1=1, xref='x', yref='paper', 
                                           line_width=1.5)],    
                            annotations=[dict(x='2020-03-04', y=0.15, xref='x', yref='paper', xanchor='left', 
                                              text='Covid-19',showarrow=False)])
            
    def Candlestick(self, resp):
        #Plota um gráfico candlestick da ação escolhida, característico do mercado financeiro
        self.resp = resp
        fig = go.Figure(data=[go.Candlestick
                        (
                            x=self.bond['Date'],
                            open=self.bond['Open'],
                            high=self.bond['High'],
                            low=self.bond['Low'],
                            close=self.bond['Close'],
                        )])
        
        fig.update_layout(title_text=self.ação.upper()+' Candlestick')
        self.Bond_SelectorButton(fig)
        self.Fig_Update(fig,self.resp)
        fig.show()
    
    def Análise_Media(self, resp):
        #Plota um gráfico com botôes selecionáveis das análises médias desejadas(5,10,20,50,100 ou 200 dias)
        self.bond['MA5'] = self.bond['Close'].rolling(5).mean()
        self.bond['MA10'] = self.bond['Close'].rolling(10).mean()
        self.bond['MA20'] = self.bond['Close'].rolling(20).mean()
        self.bond['MA50'] = self.bond['Close'].rolling(50).mean()
        self.bond['MA100'] = self.bond['Close'].rolling(100).mean()
        self.bond['MA200'] = self.bond['Close'].rolling(200).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter
              (x=self.bond.index,
               y=self.bond['Close'],
               name="Close",
               line=dict(color="#33CFA5")))
        fig.add_trace(go.Scatter
               (x=self.bond.index,
               y=self.bond['MA5'],
               name="MA5",
               visible=False,
               line=dict(color="Orange")))
        fig.add_trace(go.Scatter
               (x=self.bond.index,
               y=self.bond['MA10'],
               name="MA10",
               visible=False,
               line=dict(color="Black")))
        fig.add_trace(go.Scatter
               (x=self.bond.index,
               y=self.bond['MA20'],
               name="MA20",
               visible=False,
               line=dict(color="Green")))
        fig.add_trace(go.Scatter
               (x=self.bond.index,
               y=self.bond['MA50'],
               name="MA50",
               visible=False,
               line=dict(color="Blue")))
        fig.add_trace(go.Scatter
               (x=self.bond.index,
               y=self.bond['MA100'],
               name="MA100",
               visible=False,
               line=dict(color="Yellow")))
        fig.add_trace(go.Scatter
               (x=self.bond.index,
               y=self.bond['MA200'],
               name="MA200",
               visible=False,
               line=dict(color="RED")))
        fig.update_layout(
            updatemenus=[dict(active=0,
                buttons=list([
                    dict(label="Close",
                         method="update",
                         args=[{"visible": [True, False, False, False, False, False, False]},
                               {"title": self.ação.upper()+" Close",
                                "annotations": []}]),
                    dict(label="MA5",
                         method="update",
                         args=[{"visible": [True, True, False, False, False, False, False]},
                               {"title": self.ação.upper()+' MA5',
                                "annotations": []}]),
                    dict(label="MA10",
                         method="update",
                         args=[{"visible": [True, False, True, False, False, False, False]},
                               {"title": self.ação.upper()+' MA10',
                                "annotations": []}]),
                    dict(label="MA20",
                         method="update",
                         args=[{"visible": [True, False, False, True, False, False, False]},
                               {"title": self.ação.upper()+' MA20'}]),
                    dict(label="MA50",
                         method="update",
                         args=[{"visible": [True, False, False, False, True, False, False]},
                               {"title": self.ação.upper()+' MA50'}]),
                    dict(label="MA100",
                         method="update",
                         args=[{"visible": [True, False, False, False, False, True, False]},
                               {"title": self.ação.upper()+' MA100'}]),
                    dict(label="MA200",
                         method="update",
                         args=[{"visible": [True, False, False, False, False, False, True]},
                               {"title": self.ação.upper()+' MA200'}]),
                    dict(label="All",
                         method="update",
                         args=[{"visible": [True, True, True, True, True, True, True]},
                               {"title": self.ação.upper()+' Médias'}]),
                ]),
            )
        ])
        fig.update_layout(title_text=self.ação.upper()+' Média Móvel')
        self.Bond_SelectorButton(fig)
        self.Fig_Update(fig, resp)
        fig.show()
    
    def Traces(self):
        #Dois Gráficos de High e Low da ação e as médias do período, desde que a ação começou a operar na bolsa e no YTD
        fig = go.Figure()
        fig.add_trace(go.Scatter
              (x=list(self.bond.index),
               y=list(self.bond['High']),
               name="High",
               line=dict(color="#33CFA5")))
        fig.add_trace(go.Scatter
               (x=list(self.bond.index),
               y=[self.bond['High'].mean()] * len(self.bond.index),
               name="High Average",
               visible=False,
               line=dict(color="#33CFA5", dash="dash")))
        fig.add_trace(go.Scatter
               (x=list(self.bond.index),
               y=list(self.bond['Low']),
               name="Low",
               line=dict(color="#F06A6A")))

        fig.add_trace(go.Scatter
               (x=list(self.bond.index),
               y=[self.bond['Low'].mean()] * len(self.bond.index),
               name="Low Average",
               visible=False,
               line=dict(color="#F06A6A", dash="dash")))
        
        high_annotations = [dict(x="2016-03-01",
                         y=self.bond['High'].mean(),
                         xref="x", yref="y",
                         text="High Average:<br> %.3f" % self.bond['High'].mean(),
                         ax=0, ay=-40),
                    dict(x=self.bond['High'].idxmax(),
                         y=self.bond['High'].max(),
                         xref="x", yref="y",
                         text="High Max:<br> %.3f" % self.bond['High'].max(),
                         ax=0, ay=-40)]
        low_annotations = [dict(x="2014-05-01",
                        y=self.bond['Low'].mean(),
                        xref="x", yref="y",
                        text="Low Average:<br> %.3f" % self.bond['Low'].mean(),
                        ax=0, ay=40),
                   dict(x=self.bond['High'].idxmin(),
                        y=self.bond['Low'].min(),
                        xref="x", yref="y",
                        text="Low Min:<br> %.3f" % self.bond['Low'].min(),
                        ax=0, ay=40)]
        
        fig.update_layout(
            updatemenus=[dict(active=0,
                buttons=list([
                    dict(label="None",
                         method="update",
                         args=[{"visible": [True, False, True, False]},
                               {"title": self.ação.upper()+" Low / High",
                                "annotations": []}]),
                    dict(label="High",
                         method="update",
                         args=[{"visible": [True, True, False, False]},
                               {"title": self.ação.upper()+' High',
                                "annotations": high_annotations}]),
                    dict(label="Low",
                         method="update",
                         args=[{"visible": [False, False, True, True]},
                               {"title": self.ação.upper()+' Low',
                                "annotations": low_annotations}]),
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True, True, True]},
                               {"title": self.ação.upper()+' LOW / HIGH',
                                "annotations": high_annotations + low_annotations}]),
                ]),
            )
        ])
        fig.update_layout(title_text=self.ação.upper()+' LOW / HIGH')
        fig.show()
        
        """
        Gráfico da ação com as médias para o ano atual
        """
        # Coletando os dados do ano atual
        year = datetime.today()
        year = year.strftime('%Y')
        df_year = pd.DataFrame()
        x = 0
        for i in range(0,len(self.bond)):
            if self.bond.iloc[i]['Date'].strftime('%Y') == str(year):
                df_year[x] = self.bond.iloc[i]
                x += 1
        
        df_year = df_year.T
        df_year.index = df_year['Date']
        
        #Plotando o gráfico de Open e Close.
        fig = go.Figure()
        
        fig.add_trace(go.Scatter
              (x=list(df_year.index),
               y=(list(df_year['Open'])),
               name='Open',
               line=dict(color='blue')))
        fig.add_trace(go.Scatter
              (x=list(df_year.index),
               y=list(df_year['Close']),
               name='Close',
               line=dict(color='Yellow')))
        fig.add_trace(go.Scatter
              (x=list(df_year.index),
               y=list(df_year['High']),
               name="High",
               line=dict(color="#33CFA5")))
        fig.add_trace(go.Scatter
               (x=list(df_year.index),
               y=[df_year['High'].mean()] * len(df_year.index),
               name="High Average",
               visible=False,
               line=dict(color="#33CFA5", dash="dash")))
        fig.add_trace(go.Scatter
               (x=list(df_year.index),
               y=list(df_year['Low']),
               name="Low",
               line=dict(color="#F06A6A")))
        fig.add_trace(go.Scatter
               (x=list(df_year.index),
               y=[df_year['Low'].mean()] * len(df_year.index),
               name="Low Average",
               visible=False,
               line=dict(color="#F06A6A", dash="dash")))
        
        #Problema para coletar o index do higher value, resolvido da seguinte forma:
        maximo = df_year['High'].max()
        minimo = df_year['High'].min()
        for i in range(0,len(df_year)):
            if df_year['High'][i] == maximo:
                max_index = df_year['Date'][i]
            elif df_year['High'][i] == minimo:
                min_index = df_year['Date'][i]
            
        high_annotations = [dict(x="2020-03-03",
                         y=df_year['High'].mean(),
                         xref="x", yref="y",
                         text="High Average:<br> %.3f" % df_year['High'].mean(),
                         ax=0, ay=-40),
                    dict(x=max_index,
                         y=df_year['High'].max(),
                         xref="x", yref="y",
                         text="High Max:<br> %.3f" % df_year['High'].max(),
                         ax=0, ay=-40)]
        low_annotations = [dict(x="2020-02-02",
                        y=df_year['Low'].mean(),
                        xref="x", yref="y",
                        text="Low Average:<br> %.3f" % df_year['Low'].mean(),
                        ax=0, ay=40),
                   dict(x=min_index,
                        y=df_year['Low'].min(),
                        xref="x", yref="y",
                        text="Low Min:<br> %.3f" % df_year['Low'].min(),
                        ax=0, ay=40)]
        
        fig.update_layout(
            updatemenus=[dict(active=0,
                buttons=list([
                    dict(label="All",
                         method="update",
                         args=[{"visible": [True, True, True, False, True, False]},
                               {"title": self.ação.upper()+' '+year,
                                "annotations": []}]),
                    dict(label="High",
                         method="update",
                         args=[{"visible": [True, True, True, True, False, False]},
                               {"title": self.ação.upper()+' '+year+' High',
                                "annotations": high_annotations}]),
                    dict(label="Low",
                         method="update",
                         args=[{"visible": [True, True, False, False, True, True]},
                               {"title": self.ação.upper()+' '+year+' Low',
                                "annotations": low_annotations}]),
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True, True, True, True, True]},
                               {"title": self.ação.upper()+' '+year+' LOW / HIGH',
                                "annotations": high_annotations + low_annotations}]),
                ]),
            )
        ])

        fig.update_layout(title_text=self.ação.upper()+' '+year)
        fig.show()
        
    def Volume_Analisys(self):
        #Gráfico da análise de volume
        fig = make_subplots(rows = 2, cols = 1, shared_xaxes=True,
                           row_heights=[1.5, 0.3])
        
        fig.add_trace(go.Scatter(x=self.bond['Date'], y = self.bond['Open'], name="Open"),
                            row = 1, col = 1)
        fig.add_trace(go.Scatter(x=self.bond['Date'], y = self.bond['Close'], name="Close"),
                            row = 1, col = 1)
        fig.add_trace(go.Scatter(x=self.bond['Date'], y = self.bond['High'], name="High"),
                            row = 1, col = 1)
        fig.add_trace(go.Scatter(x=self.bond['Date'], y = self.bond['Low'], name="Low"),
                            row = 1, col = 1)
        fig.add_trace(go.Bar(x=self.bond['Date'], y = self.bond['Volume'], name='Volume'),
                            row = 2, col = 1)
        
        fig.update_yaxes(showgrid=False, row=2, col=1)
        ' Falta ainda efetuar alguns ajustes no volume'
        return fig.show()
    
    def anos(self, lista_anos):
        #Função que seleciona os anos desejados para a análise fundamentalista e retorna em forma de lista os anos digitados
        anos_validos = ['2019','2018','2017','2016','2015']
        self.lista_anos = lista_anos
        while self.anos != 'quit':
            print("Os seguintes anos " + '-'.join(map(str,anos_validos)) + " possuem dados")
            self.anos = input(str("Digite o ano desejado para a análise e quit para sair:")).lower()
            if self.anos in anos_validos:
                lista_anos.append(self.anos)
                for i in enumerate(anos_validos):
                    if self.anos in anos_validos:
                        del anos_validos[i[0]]
            elif self.anos != 'quit':
                print('Valor inválido, digite um desses anos: '+'-'.join(map(str,anos_validos)))
            else:
                print("\nAnos a serem analisados:"+'-'.join(map(str,lista_anos)))
        return lista_anos 
    
    def Balanço_Patrimonial(self, ação):
        # DataFrame do Balanço Patrimonial da ação (Somente Brasileira)
        self.ação = ação
        try:
            url = "https://statusinvest.com.br/acoes/"+ self.ação
            análise_fundamentalista = requests.get(url)
            self.df_BP = pd.read_html(análise_fundamentalista.text)
            self.df_BP = self.df_BP[4]
            anos = ['2019','2018','2017','2016','2015']
            colunas= []
            for i in self.df_BP.columns:
                colunas.append(i)
                for i in colunas:
                    for j in anos:
                        if j == i:
                            colunas.remove(j)
            for i in colunas:
                if i != '#':
                    self.df_BP.drop(columns=i,axis=1,inplace=True)
            self.df_BP.rename(columns={"#": "Balanço Patrimonial (Milhões)"}, inplace = True)
            self.df_BP.index = self.df_BP["Balanço Patrimonial (Milhões)"]
            self.df_BP.drop("Balanço Patrimonial (Milhões)", axis = 1, inplace = True)
            for i in self.df_BP.columns:
                for j in range(0, len(self.df_BP)):
                    try:
                        if self.df_BP.iloc[j][i] == '-':
                            self.df_BP.iloc[j][i] = float(self.df_BP.iloc[j][i].replace("-","0"))
                        else:
                            self.df_BP.iloc[j][i] = float(self.df_BP.iloc[j][i][:-1].replace(".","").replace(",","."))
                    except:
                        self.df_BP.iloc[j][i] = float(0)
            return self.df_BP
        except:
            return print('Dados para a ação '+self.ação+' não foram encontrados.')
    
    def Fluxo_de_Caixa(self, ação):
        # DataFrame do Fluxo de Caixa da ação (Somente Brasileira)
        self.ação = ação
        try:
            url = "https://statusinvest.com.br/acoes/"+ self.ação
            análise_fundamentalista = requests.get(url)
            self.df_FC = pd.read_html(análise_fundamentalista.text)
            self.df_FC = self.df_FC[3]
            anos = ['2019','2018','2017','2016','2015']
            colunas= []
            for i in self.df_FC.columns:
                colunas.append(i)
                for i in colunas:
                    for j in anos:
                        if j == i:
                            colunas.remove(j)
            for i in colunas:
                if i != '#':
                    self.df_FC.drop(columns=i,axis=1,inplace=True)
            self.df_FC.rename(columns={"#": "Fluxo de Caixa (Milhões)"}, inplace = True)
            self.df_FC.index = self.df_FC["Fluxo de Caixa (Milhões)"]
            self.df_FC.drop("Fluxo de Caixa (Milhões)", axis = 1, inplace = True)
            for r in self.df_FC.columns:
                for i in range(0, len(self.df_FC)):
                    try:
                        if self.df_FC.iloc[i][r] == "-":
                            self.df_FC.iloc[i][r] = float(self.df_FC.iloc[i][r].replace("-","0"))
                        else:
                            self.df_FC.iloc[i][r] = float(self.df_FC.iloc[i][r][:-1].replace(".","").replace(",","."))
                    except:
                        self.df_FC.iloc[i][r] = float(0)
            return self.df_FC
        except:
            return print('Dados para a ação '+self.ação+' não foram encontrados.')
    
    def DRE(self, ação):
        # DataFrame do Demonstrativo do Resultado de Exercício da ação (Somente Brasileira)
        self.ação = ação
        try:
            url = "https://statusinvest.com.br/acoes/"+ self.ação
            análise_fundamentalista = requests.get(url)
            self.df_DRE = pd.read_html(análise_fundamentalista.text)
            self.df_DRE = self.df_DRE[2]
            anos = ['Últ. 12M 3T2019 - 2T2020','2019','2018','2017','2016','2015']
            colunas= []
            for i in self.df_DRE.columns:
                colunas.append(i)
                for i in colunas:
                    for j in anos:
                        if j == i:
                            colunas.remove(j)
            for i in colunas:
                if i != '#':
                    self.df_DRE.drop(columns=i,axis=1,inplace=True)
            self.df_DRE.drop(index=[12,13,16,17,18,19,20,21],axis=0,inplace=True)
            self.df_DRE.rename(columns={"#": "DRE (Milhões)"}, inplace = True)
            self.df_DRE.index = self.df_DRE["DRE (Milhões)"]
            self.df_DRE.drop("DRE (Milhões)", axis = 1, inplace = True)

            for r in self.df_DRE.columns:
                for i in range(0,len(self.df_DRE)):
                    try:
                        if self.df_DRE.iloc[i][r] == "-":
                            self.df_DRE.iloc[i][r] = float(self.df_DRE.iloc[i][r].replace("-","0"))
                        else:
                            self.df_DRE.iloc[i][r] = float(self.df_DRE.iloc[i][r][:-1].replace(".","").replace(",","."))
                    except:
                        self.df_DRE.iloc[i][r] = float(0)
            return self.df_DRE
        except:
            print('Dados para a ação '+self.ação+' não foram encontrados.')
        
    def Analise_Fundamentalista(self, ação):
       
        """
        Análise Fundamentalista da ação, de acordo com o comando digitado, no caso de Comparação ou Setor, é comparado
        o último ano obtido nos balanços. São plotados gráficos para faciliar a visualização dos dados. Também são calculadas
        as margens e outro parâmetros de investimento como por exemplo ROE, P/L, LPA ...
        
        """
        # Análise do Balanço Patrimonial
        self.ação = ação
        df_BP = pd.DataFrame()
        if len(self.ação) != 1:
            for i in self.ação:
                self.Balanço_Patrimonial(i)
                name = self.df_BP.columns[0]
                df_BP[i+' '+name] = self.df_BP[name]
        else:
            self.Balanço_Patrimonial(self.ação[0])
            df_BP = self.df_BP.copy()
        self.ação = ação
        pd.options.display.float_format = '{:.2f}'.format
        display(df_BP)
        
        #Análise Vertical e Horizontal
        if len(self.ação) == 1:
            df_BP_VH = pd.DataFrame()
            lista_anos = []
            self.anos(lista_anos)
            for i in lista_anos:
                df_BP_VH[i] = df_BP[i].copy()
                df_BP_VH["AV % "+ i] = (df_BP[i] / df_BP[i][0]) * 100
                for j in range(1,len(lista_anos)):
                    if "AV % "+lista_anos[j] in df_BP_VH.columns:
                        df_BP_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]] = float(0)
                        for k in range(len(df_BP_VH)):
                            try:
                                df_BP_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]][k] = ((df_BP[lista_anos[0]][k] - df_BP[lista_anos[j]][k])/df_BP[lista_anos[j]][k]) *100
                            except:
                                None
            display(df_BP_VH)   
            
        df_bal_graph = pd.DataFrame()
        lista_graph = ["Ativo Total - (R$)","Ativo Circulante - (R$)","Ativo Não Circulante - (R$)",
                      "Passivo Circulante - (R$)","Passivo Não Circulante - (R$)","Patrimônio Líquido Consolidado - (R$)"]   
        fig1 = go.Figure() 
        for i in range(0,len(df_BP)):
            if df_BP.iloc[i].name in lista_graph:
                df_bal_graph[i] = df_BP.iloc[i]
                df_bal_graph.rename(columns={i: df_BP.iloc[i].name}, inplace = True)
                fig1.add_trace(go.Bar(
                    x=df_bal_graph.index,
                    y=df_bal_graph[df_BP.iloc[i].name],
                    name=df_BP.iloc[i].name,
                    marker_color= 0
                    ))
        df_bal_graph['Passivos'] = df_bal_graph["Passivo Circulante - (R$)"] + df_bal_graph ["Passivo Não Circulante - (R$)"] 
        
        fig1.add_trace(go.Scatter(x=df_bal_graph.index, y=df_bal_graph[lista_graph[0]],name='Ativo',
                                line=dict(color='black',width = 2)))  
        
        fig1.add_trace(go.Scatter(x=df_bal_graph.index, y=df_bal_graph["Passivos"],name='Passivo',
                                line=dict(color='red', width = 2)))
        fig1.update_layout(title='<b>Balanço Patrimonial</b> ('+' '.join(map(str,self.ação))+')')
        fig1.show()
        
        #Índices de solvência de curto e longo prazo
        # Algumas empresas não possuem alguns dados de liquidez, por exemplo: Bancos, sendo necessário utilizar um try/except
        df_solvencia = pd.DataFrame()
        fig2 = go.Figure()
        for i in df_BP.columns:
            try:
                df_solvencia['Liquidez Corrente'] = df_BP.loc['Ativo Circulante - (R$)'] / df_BP.loc['Passivo Circulante - (R$)']
                df_solvencia['Liquidez Seca'] = (df_BP.loc['Ativo Circulante - (R$)'] - df_BP.loc['Estoque - (R$)']) / df_BP.loc['Passivo Circulante - (R$)']
                df_solvencia['Endividamento Total'] = ((df_BP.loc['Ativo Total - (R$)'] - df_BP.loc['Patrimônio Líquido Consolidado - (R$)']) / df_BP.loc['Ativo Total - (R$)'] )* 100
                df_solvencia['Dívida/Capital Própio'] = (df_BP.loc['Passivo Não Circulante - (R$)'] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)']) * 100
                df_solvencia['Grau Alavancagem Financeira'] = df_BP.loc['Ativo Total - (R$)'] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)']
                
            except ZeroDivisionError:
                df_solvencia['Endividamento Total'] = ((df_BP.loc['Ativo Total - (R$)'] - df_BP.loc['Patrimônio Líquido Consolidado - (R$)']) / df_BP.loc['Ativo Total - (R$)'] )* 100
                df_solvencia['Dívida/Capital Própio'] = (df_BP.loc['Passivo Não Circulante - (R$)'] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)']) * 100
                df_solvencia['Grau Alavancagem Financeira'] = df_BP.loc['Ativo Total - (R$)'] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)']
        try:
            df_solvencia['Liquidez Corrente']
            fig2 = make_subplots(rows=2, cols=2,
                    subplot_titles=("Liquidez Corrente e Seca", 
                                "Endividamento Total", 
                                "Dívida/Capital Próprio", 
                                "Grau Alavancagem Financeira"
                                 ))
        
            for i in range(0,len(df_solvencia.columns)-3):
                        fig2.add_trace(go.Bar(
                            x=df_solvencia.index,
                            y=df_solvencia[df_solvencia.columns[i]],
                            name=df_solvencia.columns[i],
                            marker_color=0),
                            row=1, col=1)         
                
            fig2.add_trace(go.Scatter(x=df_solvencia.index, y=df_solvencia[df_solvencia.columns[2]],name=df_solvencia.columns[2]),
                                  row=1, col=2)

            fig2.add_trace(go.Scatter(x=df_solvencia.index, y=df_solvencia[df_solvencia.columns[3]],name=df_solvencia.columns[3]),
                                  row=2, col=1)

            fig2.add_trace(go.Scatter(x=df_solvencia.index, y=df_solvencia[df_solvencia.columns[4]],name=df_solvencia.columns[4]),
                                  row=2, col=2)
        except KeyError:
            fig2 = make_subplots(rows=1, cols=3,
                    subplot_titles=("Endividamento Total", 
                                "Dívida/Capital Próprio", 
                                "Grau Alavancagem Financeira"
                                 ))
            fig2.add_trace(go.Scatter(x=df_solvencia.index, y=df_solvencia[df_solvencia.columns[0]],name=df_solvencia.columns[0]),
                                  row=1, col=1)

            fig2.add_trace(go.Scatter(x=df_solvencia.index, y=df_solvencia[df_solvencia.columns[1]],name=df_solvencia.columns[1]),
                                  row=1, col=2)

            fig2.add_trace(go.Scatter(x=df_solvencia.index, y=df_solvencia[df_solvencia.columns[2]],name=df_solvencia.columns[2]),
                                  row=1, col=3)
        fig2.update_layout(title='<b>Índices de Solvência</b> ('+' '.join(map(str,self.ação))+')')
        fig2.show()
        
        #Análise do Demonstrativo de Resultado de Exercício
        
        df_DRE = pd.DataFrame()
        if len(self.ação) != 1:
            for i in self.ação:
                self.DRE(i)
                
                name = self.df_DRE.columns[0]
                df_DRE[i+' '+name] = self.df_DRE[name]
        else:
            self.DRE(self.ação[0])
            df_DRE = self.df_DRE
        pd.options.display.float_format = '{:.2f}'.format
        display(df_DRE)
        self.ação = ação
        
        lista_graph = ("Receita Líquida - (R$)","Custos - (R$)")
        df_DRE = df_DRE.T
        fig3 = go.Figure()
        for i in range(0,len(df_DRE)):
            if df_DRE.columns[i] in lista_graph:
                fig3.add_trace(go.Bar(
                    x=df_DRE.index,
                    y=df_DRE[df_DRE.columns[i]],
                    name=df_DRE.columns[i],
                    marker_color= 0
                ))
        fig3.update_layout(barmode='relative', title_text='Receita Líquida $ (mil)')
        fig3.add_trace(go.Scatter(x=df_DRE.index, y=df_DRE["Lucro Líquido - (R$)"],name='Lucro Líquido',
                                line=dict(color='black',width = 2)))      
        fig3.update_layout(title='<b>Demonstrativo do Resultado do Exercício</b> ('+' '.join(map(str,self.ação))+')')
        fig3.show()
        df_DRE = df_DRE.T

        #Análise Vertical e Horizontal
        
        if len(self.ação) == 1:
            df_DRE_VH = pd.DataFrame()
            for i in lista_anos:
                df_DRE_VH[i] = df_DRE[i]
                df_DRE_VH["AV % "+ i] = (df_DRE[i] / df_DRE[i][0]) * 100
                for j in range(1,len(lista_anos)):
                    if "AV % "+lista_anos[j] in df_DRE_VH.columns:
                        df_DRE_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]] = float(0)
                        for k in range(len(df_DRE_VH)):
                            try:
                                df_DRE_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]][k] = ((df_DRE[lista_anos[0]][k] - df_DRE[lista_anos[j]][k])/df_DRE[lista_anos[j]][k]) *100
                            except:
                                None
            pd.options.display.float_format = '{:.2f}'.format
            display(df_DRE_VH)   
            
        #Cálculo dos indicadores de lucratividade (Margem Bruta, Margem Operacional e Margem Líquida)
        df_margens = pd.DataFrame()
        df_margens['Margem Bruta - (%)'] = df_DRE.loc['Lucro Bruto - (R$)'] / df_DRE.loc['Receita Líquida - (R$)'] * 100
        df_margens['Margem Operacional - (%)'] = df_DRE.loc['EBITDA - (R$)'] / df_DRE.loc['Receita Líquida - (R$)'] * 100
        df_margens['Margem Líquida - (%)'] = df_DRE.loc['Lucro Líquido - (R$)'] / df_DRE.loc['Receita Líquida - (R$)'] * 100
        media_b = 0
        media_o = 0
        media_l = 0
        for i in range(0,len(df_margens)):
            media_b =  media_b + df_margens['Margem Bruta - (%)'][i]
            media_o =  media_o + df_margens['Margem Operacional - (%)'][i]
            media_l =  media_l + df_margens['Margem Líquida - (%)'][i]         
        df_margens['Média 5y Bruta'] = round(media_b / (len(df_margens)),2)
        df_margens['Média 5y Operacional'] = round(media_o / (len(df_margens)),2)
        df_margens['Média 5y Líquida'] = round(media_l / (len(df_margens)),2)
        
        fig4 = go.Figure()
        for i in range(0, len(df_margens.columns)-3):
            fig4.add_trace(go.Bar(
                x=df_margens.index,
                y=df_margens[df_margens.columns[i]],
                name=df_margens.columns[i],
                marker_color= 0
                ))
        for j in range(3, len(df_margens.columns)):
            fig4.add_trace(go.Scatter(
                x=df_margens.index,
                y=df_margens[df_margens.columns[j]],
                name=df_margens.columns[j],
                line=dict(color='black',width=2)
                ))
        fig4.update_layout(title_text='<b>Margens Líquida, Operacional e Bruta</b> ('+' '.join(map(str,self.ação))+')')
        fig4.show()
        
        #Análise do Fluxo de Caixa
        df_FC = pd.DataFrame()
        if len(self.ação) != 1:
            for i in self.ação:
                self.Fluxo_de_Caixa(i)
                name = self.df_FC.columns[0]
                df_FC[i +' '+name] = self.df_FC[name]
        else:
            self.Fluxo_de_Caixa(self.ação[0])
            df_FC = self.df_FC
        pd.options.display.float_format = '{:.2f}'.format
        display(df_FC)
        self.ação = ação
    
        fig5 = go.Figure()
        colunas =['Caixa Líquido Atividades Operacionais - (R$)','Caixa Líquido Atividades de Investimento - (R$)',
                  'Caixa Líquido Atividades de Financiamento - (R$)','Aumento de Caixa e Equivalentes - (R$)']
        
        df_FC = df_FC.T
        for i in colunas:
            fig5.add_trace(go.Bar(
                    x=df_FC.index,
                    y=df_FC[i],
                    name=i,
                    marker_color=0))
        fig5.add_trace(go.Scatter(x=df_FC.index,y=df_FC['Lucro Líquido - (R$)'],name='Lucro Líquido - (R$)'))
        fig5.update_layout(title='<b>Demonstrativo de Fluxo de Caixa</b> ('+' '.join(map(str,self.ação))+')')
        fig5.show()
        
        fig6 = go.Figure()
        colunas = ['Lucro Líquido - (R$)','Aumento de Caixa e Equivalentes - (R$)',
                   'Saldo Inicial de Caixa e Equivalentes - (R$)','Saldo Final de Caixa e Equivalentes - (R$)']
        for i in colunas:
            fig6.add_trace(go.Bar(
                x=df_FC.index,
                y=df_FC[i],
                name=i,
                marker_color=0))
        fig6.update_layout(title='<b>Composição Final do Caixa</b> ('+' '.join(map(str,self.ação))+')')
        fig6.show()
        
        #Análise Vertical e Horizontal
        if len(self.ação) == 1:
            df_FC = df_FC.T
            df_FC_VH = pd.DataFrame()
            for i in lista_anos:
                df_FC_VH[i] = df_FC[i]
                df_FC_VH["AV % "+ i] = (df_FC[i] / df_FC[i][0]) * 100
                for j in range(1,len(lista_anos)):
                    if "AV % "+lista_anos[j] in df_FC_VH.columns:
                        df_FC_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]] = float(0)
                        for k in range(len(df_FC_VH)):
                            try:
                                df_FC_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]][k] = ((df_FC[lista_anos[0]][k] - df_FC[lista_anos[j]][k])/df_FC[lista_anos[j]][k]) *100
                            except:
                                None
            pd.options.display.float_format = '{:.2f}'.format
            display(df_FC_VH)
        
        """Indicadores de Mercado
        O método de webscrapping utilizado até então não funcionou para esse site, sendo necessário mudar o método.
        Utilizando a biblioteca Request e especificando alguns parâmetros, fazendo com que o site permita o acesso.
        """
        retorno_anual = []
        bond_f_list = []
        bond_a_list = []
        LPA = []
        valor_mercado = []
        ROE = []
        ROIC = []
        ROA = []
        Giro_ativo = []
        column = 0
        self.ação = ação
        if len(self.ação) > 1:
            for i in self.ação:
                url3 = "http://www.fundamentus.com.br/detalhes.php?papel="+ i
                req = Request(url3, headers={'User-Agent': 'Chrome/84.0.4147.105'})
                webpage = urlopen(req).read()
                # Forma mais simples de remover os pontos separando os milhares.
                df1 = pd.read_html(webpage, decimal=',', thousands='.')
                df1 = df1[1]
                # Coleta do número de ações da empresa alvo.
                n_ações = float(df1[3][1])
                # O Site fundamentus já fornece todos os dados que queremos, porém irei calcular a fim de treino e aprendizado.
                LPA.append(df_DRE.loc["Lucro Líquido - (R$)"][column]*1000000 / n_ações)
                ROE.append(df_DRE.loc['Lucro Líquido - (R$)'][column] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)'][column] * 100)
                ROIC.append((df_DRE.loc['EBIT - (R$)'][column] - df_DRE.loc['Impostos - (R$)'][column]) / (df_BP.loc['Patrimônio Líquido Consolidado - (R$)'][column] + df_DRE.loc['Dívida Bruta - (R$)'][column]) *100)
                ROA.append(df_DRE.loc['Lucro Líquido - (R$)'][column] / df_BP.loc['Ativo Total - (R$)'][column] * 100)
                Giro_ativo.append(df_DRE.loc['Receita Líquida - (R$)'][column] / df_BP.loc['Ativo Total - (R$)'][column])
                bond = yf.download(i+'.SA',period='ytd')
                bond_f_list.append(bond['Close'].iloc[0])
                bond_a_list.append(bond['Close'].iloc[-1])
                retorno_anual.append((bond['Close'].iloc[-1]-bond['Close'].iloc[0])/bond['Close'].iloc[0]*100)
                valor_mercado.append(bond['Close'].iloc[-1]*n_ações)
                column += 1
        else:
            for i in df_BP.columns:
                url3 = "http://www.fundamentus.com.br/detalhes.php?papel="+ self.ação[0]
                req = Request(url3, headers={'User-Agent': 'Chrome/84.0.4147.105'})
                webpage = urlopen(req).read()
                # Forma mais simples de remover os pontos separando os milhares.
                df1 = pd.read_html(webpage, decimal=',', thousands='.')
                df1 = df1[1]
                n_ações = float(df1[3][1])
                LPA.append(df_DRE.loc["Lucro Líquido - (R$)"][i]*1000000 / n_ações)
                ROE.append(df_DRE.loc['Lucro Líquido - (R$)'][i] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)'][i] * 100)
                ROIC.append((df_DRE.loc['EBIT - (R$)'][i] - df_DRE.loc['Impostos - (R$)'][i]) / (df_BP.loc['Patrimônio Líquido Consolidado - (R$)'][i] + df_DRE.loc['Dívida Bruta - (R$)'][i]) *100)
                ROA.append(df_DRE.loc['Lucro Líquido - (R$)'][i] / df_BP.loc['Ativo Total - (R$)'][i] * 100)
                Giro_ativo.append(df_DRE.loc['Receita Líquida - (R$)'][i] / df_BP.loc['Ativo Total - (R$)'][i])
                bond = yf.download(self.ação[0]+'.SA',start=datetime(year=int(i),month=1,day=1), end=datetime(year=int(i),month=12,day=31))
                bond_f_list.append(bond['Close'].iloc[0])
                bond_a_list.append(bond['Close'].iloc[-1])
                retorno_anual.append((bond['Close'].iloc[-1]-bond['Close'].iloc[0])/bond['Close'].iloc[0]*100)
                valor_mercado.append(bond['Close'].iloc[-1]*n_ações)
        if len(ação) == 1:
            df_DRE.drop(columns='Últ. 12M 3T2019 - 2T2020', axis=1, inplace=True)
        # Adicionando os valores no DataFrame
        df_m = pd.DataFrame()
        df_m = df_m.append(pd.Series(data=LPA, index = df_DRE.columns, name ="Lucro por Ação (LPA)"))
        df_m = df_m.append(pd.Series(data=bond_f_list, index=df_DRE.columns, name = "Preço Ação R$ (Início do ano)"))
        df_m = df_m.append(pd.Series(data=bond_a_list, index=df_DRE.columns, name = "Preço Ação R$ (Atual)"))
        P = df_m.loc['Preço Ação R$ (Atual)'] / df_m.loc['Lucro por Ação (LPA)']
        df_m = df_m.append(pd.Series(data=P, index=df_DRE.columns, name = "P/L"))
        df_m = df_m.append(pd.Series(data=ROA, index=df_DRE.columns, name= "ROA (%)"))
        df_m = df_m.append(pd.Series(data=ROE, index=df_DRE.columns, name = "ROE (%)"))
        df_m = df_m.append(pd.Series(data=ROIC, index=df_DRE.columns, name = "ROIC (%)"))
        df_m = df_m.append(pd.Series(data=Giro_ativo, index=df_DRE.columns, name='Giro Ativo'))
        df_m = df_m.append(pd.Series(data=retorno_anual, index=df_DRE.columns, name = "Retorno Atual (%)"))
        df_m = df_m.append(pd.Series(data=valor_mercado, index=df_DRE.columns, name = "Valor de Mercado (Bilhões)"))
        pd.options.display.float_format = '{:.2f}'.format
        if len(ação) > 1:
            for i in range (0, len(self.ação)):
                df_m.rename(columns={self.ação[i]+ " Últ. 12M 3T2019 - 2T2020": self.ação[i]+' Ult.12M'}, inplace=True)
            

        fig7 = make_subplots(rows=2, cols=3,
                    subplot_titles=("LPA", "P/L", 'Giro Ativo', "ROA", "ROE", "ROIC"))
        
        fig7.add_trace(go.Bar(
                            x=df_m.columns,
                            y=df_m.loc["Lucro por Ação (LPA)"],
                            name='LPA',
                            marker_color=0),
                            row=1, col=1)
        fig7.add_trace(go.Bar(
                            x=df_m.columns,
                            y=df_m.loc["P/L"],
                            name='P/L',
                            marker_color=0),
                            row=1, col=2)
        fig7.add_trace(go.Bar(
                            x=df_m.columns,
                            y=df_m.loc["Giro Ativo"],
                            name='Giro Ativo',
                            marker_color=0),
                            row=1, col=3)
        fig7.add_trace(go.Bar(
                            x=df_m.columns,
                            y=df_m.loc["ROA (%)"],
                            name='ROA',
                            marker_color=0),
                            row=2, col=1)
        fig7.add_trace(go.Bar(
                            x=df_m.columns,
                            y=df_m.loc["ROE (%)"],
                            name='ROE',
                            marker_color=0),
                            row=2, col=2)
        fig7.add_trace(go.Bar(
                            x=df_m.columns,
                            y=df_m.loc["ROIC (%)"],
                            name='ROIC',
                            marker_color=0),
                            row=2, col=3) 
        fig7.show()
        display(df_m)
        sav_table = input(str('Deseja salvar alguma das tabelas em Excel? [S/N]')).upper()
        if sav_table == 'S' or sav_table == 'SIM':
            sav = ''
            while sav != 'QUIT':
                if len(ação) == 1:
                    print('Digite a Tabela Desejada\n'+
                          '[1] BP\n'+
                          '[2] BP (Análise Vertical e Horizontal)\n'+
                          '[3] DRE\n'+
                          '[4] DRE (Análise Vertical e Horizontal)\n'+
                          '[5] FC\n'+
                          '[6] FC (Análise Vertical e Horizontal)')
                    print('Digite "QUIT" para sair.')
                    sav = input('').upper()
                    if sav == str(1):
                        self.Save_to_Excel(df_BP)
                    elif sav == str(2):
                        self.Save_to_Excel(df_BP_VH)
                    elif sav == str(3):
                        self.Save_to_Excel(df_DRE)
                    elif sav == str(4):
                        self.Save_to_Excel(df_DRE_VH)
                    elif sav == str(5):
                        self.Save_to_Excel(df_FC)
                    elif sav == str(6):
                        self.Save_to_Excel(df_FC_VH)
                else:
                    print('Digite a Tabela Desejada\n'+
                          '[1] BP\n'+
                          '[2] DRE\n'+
                          '[3] FC')
                    print('Digite "QUIT" para sair.')
                    sav = input('').upper()
                    if sav == str(1):
                        self.Save_to_Excel(df_BP)
                    elif sav == str(2):
                        self.Save_to_Excel(df_DRE)
                    elif sav == str(3):
                        self.Save_to_Excel(df_FC)
                        
    def Save_to_Excel(self, df):
        self.df = df
        name = input(str('Digite o nome do arquivo sem espaços:'))
        self.df.to_excel(name+'.xlsx')
        print('Arquivo salvo com sucesso!\n Está salvo na mesma pasta do algoritmo')
        
    def Oscilações(self):
        # Cálculo das oscilações da ação no dia, mês, ano, YTD
        df_osc = pd.DataFrame()
        # Calculando a oscilação mensal
        # A biblioteca yfinance só retorna o valor após o fechamento do mercado
        ano_atual = int(datetime.today().strftime('%Y'))
        mes_atual = int(datetime.today().strftime('%m'))
        dia_atual = int(datetime.today().strftime('%d'))
        cot_atual = datetime(year=ano_atual,month=mes_atual,day=dia_atual)
        self.Data(cot_atual)
        cot_atual = self.data
        osc_dia = ((self.bond.loc[cot_atual]['Close'] - self.bond.loc[cot_atual]['Open'])/self.bond.loc[cot_atual]['Open'])*100
        
        """Oscilação em 30 dias"""
        dia_atual = int(cot_atual.strftime('%d'))
        cot_30 = datetime(year=ano_atual,month=mes_atual-1,day=dia_atual)
        self.Data(cot_30)
        cot_30 = self.data
        osc_30 = ((self.bond.loc[cot_atual]['Close'] - self.bond.loc[cot_30]['Close']) /self.bond.loc[cot_30]['Close'])*100

        """Oscilação no mês"""
        while dia_atual != 1:
            dia_atual -= 1
            dia_mes = datetime(year=ano_atual,month=mes_atual,day=dia_atual)
            if dia_atual == 1:
                if dia_mes.weekday() == 5:
                    dia_atual = dia_atual + 2
                    dia_mes = datetime(year=ano_atual,month=mes_atual,day=dia_atual)
                    break
                elif dia_mes.weekday() == 6:
                    dia_atual = dia_atual + 1
                    dia_mes = datetime(year=ano_atual,month=mes_atual,day=dia_atual)
                    break
                else:
                    dia_mes = datetime(year=ano_atual,month=mes_atual,day=dia_atual)
                    break            
        osc_mes = ((self.bond.loc[cot_atual]['Close'] - self.bond.loc[dia_mes]['Close'])/self.bond.loc[dia_mes]['Close'])*100
        
        
        """Oscilação YTD"""
        cot_ano = []
        for i in range(0,len(self.bond)):
            if self.bond.iloc[i]['Date'].strftime('%Y') == str(ano_atual):
                cot_ano.append(self.bond.iloc[i]['Close'])    
        osc_YTD = ((self.bond.loc[cot_atual]['Close'] - cot_ano[0])/cot_ano[0] *100)
        
        """Oscilação 12 meses"""
        #Resetando o dia_atual
        dia_atual = int(datetime.today().strftime('%d'))
        cot_12 = datetime(year=ano_atual-1,month=mes_atual,day=dia_atual)                                       
        self.Data(cot_12)
        cot_12 = self.data
        osc_12 = ((self.bond.loc[cot_atual]['Close'] - self.bond.loc[cot_12]['Close'])/self.bond.loc[cot_12]['Close'])*100
        
        """Max e Min 52 Semanas"""
        cot_52 = []
        for i in range(0,len(self.bond)):
            if self.bond.iloc[i]['Date'] > datetime(year=ano_atual-1,month=mes_atual-1,day=dia_atual):
                cot_52.append(self.bond.iloc[i]['Close'])
        
        """Tabela"""
        osc_index = ['Dia',"Mês","30 Dias","YTD","12 Meses","52 Max","52 Min"]
        dados = [round(osc_dia,2),round(osc_mes,2),round(osc_30,2),round(osc_YTD,2),round(osc_12,2),max(cot_52),min(cot_52)]
        df_osc['Oscilações (%) '+self.ação.upper()] = pd.Series(data=dados,index=osc_index)
        display(df_osc) 
    
    def Data(self, data):
        #Função que corrige a data digitada, por exemplo se for um sábado ou domingo.
        self.data = data
        # 5 = Saturday and 6 = Sunday
        ano = int(self.data.strftime('%Y'))
        mes = int(self.data.strftime('%m'))
        dia = int(self.data.strftime('%d'))
        if self.data.weekday() != 5 and self.data.weekday() != 6:
            pass
        else:
            if self.data.weekday() == 5:
                try:
                    self.data = datetime(year=ano,month=mes,day=dia - 1)
                except ValueError:
                    try:
                        self.data = datetime(year=ano,month=mes-1,day=31)
                        self.bond.loc[self.data]
                    except ValueError:
                        self.data = datetime(year=ano,month=mes-1,day=30)
            else:
                try:
                    self.data = datetime(year=ano,month=mes,day=dia - 2)
                except ValueError:
                    try:
                        self.data = datetime(year=ano,month=mes-1,day= 31)
                        self.bond.loc[self.data]
                    except ValueError:
                        self.data = datetime(year=ano,month=mes-1,day=30)
        return self.data
        
    def Variações_Diária(self, resp):
        # Função que monta dois TreeMap das 20 maiores variações positivas e negativs do setor no dia, mês ou ano
        df_setor = self.df_setor
        day_period = str('2d')
        month_period = str('1m')
        year_period = str('ytd')
        def Analise(self):
            bonds = []
            bonds_err = []
            var = []
            setor = []
            close_dia = []
            close_pre = []
            for i in range(0, len(df_setor)):
                if self != '1m':
                    bond = yf.download(df_setor['Papel'][i]+'.SA',period=self,rounding=True)
                else:
                    bond = yf.download(df_setor['Papel'][i]+'.SA',start=datetime(
                                    year=int(datetime.today().strftime('%Y')),month=int(datetime.today().strftime('%m')),day=1),
                                rounding=True)
                try:
                    bond['Close'][0]
                    bonds.append(df_setor['Papel'][i])
                    setor.append(df_setor['Setor'][i])
                    close_dia.append(bond['Close'][-1])
                    close_pre.append(bond['Close'][0])
                    try:
                        var.append((bond['Close'][-1]-bond['Close'][0])/ bond['Close'][0] *100)
                    except Exception:
                        var.append(0)
                except Exception:
                    bonds_err.append(df_setor['Papel'][i])        
            #Transformando os dados em DF
            data_inicial = bond.index[0]
            data_final = bond.index[-1]
            data = data_inicial.strftime("%d/%m/%Y")+' - '+data_final.strftime("%d/%m/%Y")
            df_vard = pd.DataFrame()
            df_vard = df_vard.append(pd.Series(data=close_pre, index=bonds, name='Pré Fechamento'))
            df_vard = df_vard.append(pd.Series(data=close_dia, index=bonds, name='Fechamento'))
            df_vard = df_vard.append(pd.Series(data=var,index=bonds, name='Var Diária (%)'))
            df_vard = df_vard.append(pd.Series(data=setor,index=bonds, name='Setor'))
            df_vard = df_vard.T
            df_vard['Papel'] = df_vard.index
            df_vard['Status'] = 'a'
            df_neg = pd.DataFrame()
            df_pos = pd.DataFrame()
            x = 0
            y = 0
            for i in range(0, len(df_vard)):
                if df_vard['Var Diária (%)'][i] > 0:
                    df_vard['Status'][i] = ' Var Postive'
                    df_pos[x] = df_vard.iloc[i]
                    x += 1
                else:
                    df_vard['Status'][i] = 'Var Negative'
                    df_vard['Var Diária (%)'][i] = df_vard['Var Diária (%)'][i] * -1
                    df_neg[y] = df_vard.iloc[i]
                    y += 1

            df_pos = df_pos.T
            df_pos.index = df_pos['Papel']
            df_pos['Var Diária (%)'] = df_pos['Var Diária (%)'].apply(lambda x: round(x, 2))
            while len(df_pos) > 20:
                arg_min = df_pos['Var Diária (%)'].argmin()
                df_pos.drop(index=df_pos['Papel'].iloc[arg_min], inplace=True)
            df_neg = df_neg.T
            df_neg.index = df_neg['Papel']
            df_neg['Var Diária (%)'] = df_neg['Var Diária (%)'].apply(lambda x: round(x, 2))
            while len(df_neg) > 20:
                arg_min = df_neg['Var Diária (%)'].argmin()
                df_neg.drop(index=df_neg['Papel'].iloc[arg_min], inplace=True)


            #Treemap
            fig1 = px.treemap(df_pos, path=['Setor','Papel','Var Diária (%)'], values='Var Diária (%)', hover_data = ['Setor'],
                                color ='Var Diária (%)',
                                color_continuous_scale='greens',
                                color_continuous_midpoint=np.average(df_pos['Var Diária (%)'], weights=df_pos['Var Diária (%)']),
                                title='As 20 maiores variações <b>Positivas</b> entre '+data)
            fig2 = px.treemap(df_neg, path=['Setor','Papel','Var Diária (%)'], values='Var Diária (%)', hover_data=['Setor'],
                            color ='Var Diária (%)',
                            color_continuous_scale='reds',
                            color_continuous_midpoint=np.average(df_neg['Var Diária (%)'], weights=df_neg['Var Diária (%)']),
                            title='As 20 maiores variações <b>Negativas</b> entre '+data)
            
            print(str(x)+' Variações Positivas no IBOV em '+data)
            print(str(y)+' Variações Negativas no IBOV em '+data)
            display(pd.concat([df_pos,df_neg]))
            fig1.show()
            fig2.show()
            
        if resp == str(1):
            Analise(day_period)
        elif resp == str(2):
            Analise(month_period)
        else:
            Analise(year_period)
   
    def Comparação(self, resp):
        # Função que retorna os dados fundamentalista e gráficos de análise das ações digitadas com intuito de comparação
        lista = []
        lista.append(self.ação)
        ação = ''
        if resp != str(2):
            while ação != 'QUIT':
                test = 0
                ação = input('Digite a(s) ação(s) que deseja \033[1m comparar \033[0m com '+' '.join(map(str,lista))+'\n *Para sair digite \033[1m"quit"\033[0m').upper()
                if ação != 'QUIT':
                    for i in range(0,len(self.df_setor)):
                        if ação == self.df_setor['Papel'][i]:
                            test += 1
                if test == 1:
                    lista.append(ação)
                elif ação == 'QUIT':
                    None
                else:
                     print('Ocorreu um erro, digite um valor válido!')
            print(lista)
            print('Digite a data para efetuar uma análise cumulativa das ações')
            start = datetime(year=int(input('Digite o ano: ')),month=int(input('Digite o mês: ')),day=int(input('Digite o dia: ')))
            fig = go.Figure()
            fig2 = go.Figure()
            fig3 = go.Figure()
            fig4 = go.Figure()
            for i in lista:
                # Ação até o dia atual
                bond = yf.download(i+'.SA', end=datetime.today())
                fig.add_trace(go.Scatter
                            (x=bond.index,
                            y=bond['Close'],
                            name=i))
                # Ação na data estipulada até o dia atual
                bond = yf.download(i+'.SA',start=start, end=datetime.today())
                fig2.add_trace(go.Scatter
                             (x=bond.index,
                             y=(bond['Close']/bond['Close'].iloc[0]),
                             name= i))
                # Análise do volume na data estipulada
                fig3.add_trace(go.Scatter
                              (x=bond.index,
                               y=bond['Volume'],
                               name=i))
                # Análise da variação diária da ação
                fig4.add_trace(go.Histogram
                              (x=bond['Close'].pct_change(1),
                              name=i,
                              histnorm='',
                              opacity=0.75))
                
            # Gráfico cumulativo comparativo com o ibovespa
            ibov = yf.download('^BVSP', start=start, end=datetime.today())
            fig2.add_trace(go.Scatter
                             (x=ibov.index,
                             y=(ibov['Close']/ibov['Close'].iloc[0]),
                             name='IBOVESPA',
                             line=dict(color='Black')))
            
            self.Fig_Update(fig, resp)
            fig.update_layout(title_text=' '.join(map(str,lista))+' <b>Close</b>')
            fig.update_layout(hovermode='x')
            fig2.update_layout(title_text=' '.join(map(str,lista))+' IBOV'+' <b>Cumulative</b> a partir de '+start.strftime('%d')+
                             '/'+start.strftime('%m')+'/'+start.strftime('%Y'))
            fig2.update_layout(hovermode='x')
            fig3.update_layout(title_text=' '.join(map(str,lista))+' <b>Volume</b> a partir de '+start.strftime('%d')+
                             '/'+start.strftime('%m')+'/'+start.strftime('%Y'))
            fig3.update_layout(hovermode='x')
            fig4.update_layout(title_text=' '.join(map(str,lista))+' <b>Variação diária</b> a partir de '+start.strftime('%d')+
                             '/'+start.strftime('%m')+'/'+start.strftime('%Y'),
                              barmode='overlay',
                              xaxis_title_text='Variação',
                              yaxis_title_text='Count')

            fig.show()
            fig2.show()
            fig3.show()
            fig4.show()
            
            # Comparação entre os balanços (Apenas ações brasileiras)
            self.Analise_Fundamentalista(lista)
            
        # Para as ações americanas
        else:
            while ação != 'QUIT':
                test = 0
                ação = input('Digite a(s) ação(s) que deseja \033[1mcomparar\033[0m com '+' '.join(map(str,lista))+'\n *Para sair digite \033[1m"quit"\033[0m').upper()
                if ação != 'QUIT':
                    lista.append(ação)
            print(lista)
            start = datetime(year=int(input('Digite o ano: ')),month=int(input('Digite o mês: ')),day=int(input('Digite o dia: ')))
            fig = go.Figure()
            fig2 = go.Figure()
            fig3 = go.Figure()
            fig4 = go.Figure()
            for i in lista:
                bond = yf.download(i, end=datetime.today())
                fig.add_trace(go.Scatter
                            (x=bond.index,
                            y=bond['Close'],
                            name=i))
                bond = yf.download(i, start=start, end=datetime.today())
                fig2.add_trace(go.Scatter
                              (x=bond.index,
                               y=(bond['Close']/bond['Close'].iloc[0]),
                              name=i))
                # Análise do volume na data estipulada
                fig3.add_trace(go.Scatter
                              (x=bond.index,
                               y=bond['Volume'],
                               name=i))
                
                fig4.add_trace(go.Histogram
                              (x=bond['Close'].pct_change(1),
                              name=i,
                              histnorm='',
                              opacity=0.75))                  
            # Comparação com o S&P 500
            syp = yf.download('^GSPC', start=start, end=datetime.today())
            fig2.add_trace(go.Scatter
                             (x=syp.index,
                             y=(syp['Close']/syp['Close'].iloc[0]),
                             name='S&P500',
                             line=dict(color='Black')))
            
            self.Fig_Update(fig, resp)
            fig.update_layout(title_text=' '.join(map(str,lista))+' Close')
            fig2.update_layout(title_text=' '.join(map(str,lista))+' S&P500'+' Cumulative in '+start.strftime('%d')+
                             '/'+start.strftime('%m')+'/'+start.strftime('%Y'))
            fig3.update_layout(title_text=' '.join(map(str,lista))+' Volume a partir de '+start.strftime('%d')+
                             '/'+start.strftime('%m')+'/'+start.strftime('%Y'))
            fig4.update_layout(title_text=' '.join(map(str,lista))+' Variação diária a partir de '+start.strftime('%d')+
                             '/'+start.strftime('%m')+'/'+start.strftime('%Y'),
                              barmode='overlay',
                              xaxis_title_text='Variação',
                              yaxis_title_text='Count')
            fig.show()
            fig2.show()
            fig3.show()
            fig4.show()
            
    def Dividends(self):
        # Dividendos pagos pela empresa desde que começou a sua operação na bolsa.
        bond = yf.download(self.ação +'.SA', end=datetime.today(),actions = True)
        bond['Date'] = bond.index
        df_DIV = pd.DataFrame()
        x = 0
        for i in range(0,len(bond)):
            if bond['Dividends'][i] != 0:
                df_DIV[x] = bond.iloc[i]
                x += 1
        df_DIV = df_DIV.T
        df_DIV.index = df_DIV['Date'] 
        fig = go.Figure()
        fig = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.03,
            specs=[[{"type": "table"}],
                   [{"type": "Scatter"}]]
        )
        fig.add_trace(go.Table(
                header=dict(
                    values=["Date", "Dividends"],
                    font=dict(size=20),
                    align="center"
                ),
                cells=dict(
                    values=[df_DIV.index.strftime('%d'+'/'+'%m'+'/'+'%Y'),df_DIV['Dividends']],
                    align = "center")
            ),row = 1, col = 1)
        fig.add_trace(go.Scatter(
                            x=df_DIV.index, y=df_DIV['Dividends'],
                            mode="markers+lines", 
                            hovertemplate=None,                   
                            hoverlabel=dict(
                                    bgcolor="white", 
                                    font_size=16, 
                                    font_family="Rockwell"
                                            ),
                                ),row=2, col=1
                     )
        fig.update_layout(
            xaxis_tickformat = '%d %B<br>%Y',
            height=800,
            showlegend=False,
            title_text=self.ação+" <b>Dividends<b/>",
        )
        fig.show()
        
    def Setor(self):
        # Análise de ações por Setor, retorna a análise fundamentalista e gráfica, similar ao método comparação, porém somente 
        # para as ações do mesmo setor.
        print('Loading ...\n')
        setores = []
        for i in range(0,len(self.df_setor)):
            if self.df_setor['Setor'].iloc[i] in setores:
                None
            else:
                setores.append(self.df_setor['Setor'].iloc[i])
        print('\033[1mSetores das empresas brasileiras listadas na Bolsa:\033[0m\n'+'\n'.join(map(str,setores)))
        a = 0
        while a == 0:
            setor = input(str('\nDigite o \033[1msetor\033[0m desejado para análise:'))
            if setor in setores:
                a = 1
            else:
                print('Valor inválido, insira um setor válido!')
        empresas = self.df_setor[self.df_setor['Setor'] == setor]
        lista = empresas.Papel.tolist()
        df_BP_Setor = pd.DataFrame()
        df_DRE_Setor = pd.DataFrame()
        df_FC_Setor = pd.DataFrame()
        print('\nEmpresas do setor '+setor+': \n'+'\n'.join(map(str,lista)))
        analise = []
        print('\nDigite quais empresas do setor '+setor+' deseja analisar ou digite \033[1m"Todas"\033[0m para analisar todas as empresas do setor.\n'+
             'OBS. Digite \033[1m"QUIT"\033[0m para sair.')
        resp = ''
        while resp != 'QUIT':
            resp = input('').upper()
            if resp == 'TODAS':
                analise = lista
                resp = 'QUIT'
            elif resp != 'QUIT':
                analise.append(resp)
        analise_1 = []
        for i in analise:
            try:
                url = "https://statusinvest.com.br/acoes/"+i
                análise_fundamentalista = requests.get(url)
                test = pd.read_html(análise_fundamentalista.text)
                analise_1.append(i)
            except:
                pass
        analise = analise_1
        self.Analise_Fundamentalista(analise)
        
        fig7 = go.Figure()
        fig8 = go.Figure()
        fig9 = go.Figure()
        for i in analise:
            bond = yf.download(i+'.SA',period='5y')
            fig7.add_trace(go.Scatter(
                            x=bond.index,
                            y=bond['Close'],
                            name=i))
            
            bond = yf.download(i+'.SA',period='ytd')
            fig8.add_trace(go.Scatter(
                            x=bond.index,
                            y=bond['Close'],
                            name=i))
            fig9.add_trace(go.Scatter(
                            x=bond.index,
                            y=bond['Close'] / bond['Close'].iloc[0],
                            name=i))
        
        ibov = yf.download('^BVSP', period='ytd')
        fig9.add_trace(go.Scatter(
                            x=ibov.index,
                            y=(ibov['Close']/ibov['Close'].iloc[0]),
                            name='IBOVESPA',
                            line=dict(color='Black')))
        
        self.Bond_SelectorButton(fig7)
        fig7.update_layout(title='<b>Fechamento das ações em 5 anos</b> ('+setor+')')
        fig8.update_layout(hovermode='x', title='<b>Fechamento YTD</b> ('+setor+')')
        fig9.update_layout(hovermode='x',title='<b>Acúmulo diário YTD comparado com IBOV</b> ('+setor+')')
        fig7.show()
        fig8.show()
        fig9.show()
            
analise = Bond_Analisys()
Bond_Analisys.initialize(analise)

