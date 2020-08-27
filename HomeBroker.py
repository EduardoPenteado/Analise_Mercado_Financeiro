#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

class All_bonds():
    """
    Classe que obtém todas as ações listadas no IBOV e o seu respectivo setor de atuação
    """
    def Setores(self):
        try:
            # Se o programa já rodou alguma, ele inicializa pelo arquivo em excel criado.
            self.df_setor = pd.read_excel('Setores.xlsx')
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
            for i in range(0,len(df)):
                url1 = "http://www.fundamentus.com.br/detalhes.php?papel="+df.loc[i]['Papel']
                req = Request(url1, headers={'User-Agent': 'Chrome/84.0.4147.105'})
                webpage = urlopen(req).read()
                self.df_setor = pd.read_html(webpage)
                self.df_setor = self.df_setor[0]
                try:
                    if self.df_setor.loc[1][3] == str(cot_atual) :
                        setor.append((df.loc[i]['Papel'],self.df_setor.loc[3][1]))
                    else:
                        pass
                except:
                    df = df.drop(i)
                print('Loading... ',end='')
                print(str(round(i/len(df)*100,0))+' %')
                if i == len(df):
                    print('Loading Complete!')
            self.df_setor = pd.DataFrame(setor)
            self.df_setor.to_excel('Setores.xlsx')
            
        self.df_setor.drop(self.df_setor.columns[0],axis=1,inplace=True)
        self.df_setor.rename(columns={0: "Papel", 1: "Setor"}, inplace = True)
        return self.df_setor

"""
Classe que analisa as ações e correlatos.
"""
class Bond_Analisys(All_bonds):    
    
    def __init__(self):
        self.Setores()
    
    def initialize(self):
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
                       '[9] Todas\n'+
                       '* Digite "back" para voltar')
                    resp2 = input('').upper()
                    if resp2 != 'BACK':
                        self.ação = input("Ação a ser analisada: \nExemplo(MGLU3, VALE3, PETR4 ...)").upper()
                        self.bond = yf.download(self.ação +'.SA', end=datetime.today())
                        self.bond['Date'] = self.bond.index
                    if resp2 == str(1):
                        self.Candlestick(resp)
                    elif resp2 == str(2):
                        self.Análise_Media(resp)
                    elif resp2 == str(3):
                        self.Traces()
                    elif resp2 == str(4):
                        self.Analise_Fundamentalista()
                    elif resp2 == str(5):
                        self.Volume_Analisys()
                    elif resp2 == str(6):
                        self.Oscilações()
                    elif resp2 == str(7):
                        self.Variações_Diária()
                    elif resp2 == str(8):
                        self.Comparação(resp)
                    elif resp2 == str(9):
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
    
    def Customization_Button(self):
        self.config = dict({'scrollZoom': True,
                            'displaylogo': False,
                            'responsive': False,
                            'modeBarButtonsToAdd': 
                                        ['drawline',
                                         'drawopenpath',
                                         'eraseshape']})
        
    def Bond_SelectorButton(self, fig):
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
        self.Customization_Button()
        self.Fig_Update(fig,self.resp)
        fig.show()
    
    def Análise_Media(self, resp):
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
        self.Customization_Button()
        self.Fig_Update(fig, resp)
        fig.show()
    
    def Traces(self):
        """Gráfico de High e Low das ações e as médias do período"""
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
        self.ação = ação
        url = "https://statusinvest.com.br/acoes/"+ self.ação
        análise_fundamentalista = requests.get(url)
        self.df_BP = pd.read_html(análise_fundamentalista.text)
        self.df_BP = self.df_BP[4]
        self.df_BP.drop(self.df_BP.columns[[2,4,5,7,8,10,11,13,14]], axis = 1,inplace = True)
        self.df_BP.rename(columns={"#": "Balanço Patrimonial (Milhões)"}, inplace = True)
        self.df_BP.index = self.df_BP["Balanço Patrimonial (Milhões)"]
        self.df_BP.drop("Balanço Patrimonial (Milhões)", axis = 1, inplace = True)
        for r in self.df_BP.columns:
            for i in range(0, len(self.df_BP)):
                try:
                    if self.df_BP.iloc[i][r] == '-':
                        self.df_BP.iloc[i][r] = float(self.df_BP.iloc[i][r].replace("-","0"))
                    else:
                        self.df_BP.iloc[i][r] = float(self.df_BP.iloc[i][r][:-1].replace(".","").replace(",","."))
                except:
                    self.df_BP.iloc[i][r] = float(0)
        return self.df_BP
    
    def Fluxo_de_Caixa(self, ação):
        self.ação = ação
        url = "https://statusinvest.com.br/acoes/"+ self.ação
        análise_fundamentalista = requests.get(url)
        self.df_FC = pd.read_html(análise_fundamentalista.text)
        self.df_FC = self.df_FC[3]
        self.df_FC.drop(self.df_FC.columns[[3,5,7,9]], axis = 1,inplace = True)
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
    
    def DRE(self, ação):
        self.ação = ação
        url = "https://statusinvest.com.br/acoes/"+ self.ação
        análise_fundamentalista = requests.get(url)
        self.df_DRE = pd.read_html(análise_fundamentalista.text)
        self.df_DRE = self.df_DRE[2]
        self.df_DRE.drop(self.df_DRE.columns[[1,2,4,5,7,8,10,11,13,14,16,17]],axis = 1, inplace = True)
        self.df_DRE.drop(self.df_DRE.index[[12,13,15,16,17,18,19,20,21]], axis = 0, inplace = True)
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
    
    def Analise_Fundamentalista(self):    
        """
        Análise do Balanço Patrimonial
        """
        self.Balanço_Patrimonial(self.ação)
        df_BP = self.df_BP
        df_BP_VH = pd.DataFrame()
        lista_anos = []
        self.anos(lista_anos)
        for i in lista_anos:
            df_BP_VH[i] = df_BP[i]
            df_BP_VH["AV % "+ i] = (df_BP[i] / df_BP[i][0]) * 100
            for j in range(1,len(lista_anos)):
                if "AV % "+lista_anos[j] in df_BP_VH.columns:
                    df_BP_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]] = float(0)
                    for k in range(len(df_BP_VH)):
                        try:
                            df_BP_VH["AH % " + lista_anos[0] + '-' + lista_anos[j]][k] = ((df_BP[lista_anos[0]][k] - df_BP[lista_anos[j]][k])/df_BP[lista_anos[j]][k]) *100
                        except:
                            None
                            
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
        fig1.update_layout(title='Balanço Patrimonial '+self.ação.upper())
        
        """Índices de solvência de curto e longo prazo"""
        
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
        fig2.update_layout(title='Índices de Solvência '+self.ação.upper())
        
        """
        Análise do Demonstrativo de REsultado de Exercício
        """
    
        self.DRE(self.ação)
        df_DRE = self.df_DRE
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
        fig3.update_layout(title='Demonstrativo do Resultado do Exercício '+self.ação.upper())
        df_DRE = df_DRE.T

        """Análise Vertical e Horizontal"""
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
                        
        """Cálculo dos indicadores de lucratividade"""
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
        fig4.update_layout(title_text='Margens Líquida, Operacional e Bruta '+ self.ação.upper())
        
        
        """
        Análise do Fluxo de Caixa
        """
        self.Fluxo_de_Caixa(self.ação)
        df_FC = self.df_FC
        
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
        fig5.update_layout(title="Demonstrativo de Fluxo de Caixa da "+self.ação.upper())
        
        fig6 = go.Figure()
        colunas = ['Lucro Líquido - (R$)','Aumento de Caixa e Equivalentes - (R$)',
                   'Saldo Inicial de Caixa e Equivalentes - (R$)','Saldo Final de Caixa e Equivalentes - (R$)']
        for i in colunas:
            fig6.add_trace(go.Bar(
                x=df_FC.index,
                y=df_FC[i],
                name=i,
                marker_color=0))
        fig6.update_layout(title='Composição Final do Caixa da '+self.ação.upper())
        
        """Análise Vertical e Horizontal"""
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
        
        
        """Indicadores de Mercado
        
        O método de webscrapping utilizado até então não funcionou para esse site, sendo necessário mudar o método.
        Utilizando a biblioteca Request e especificando alguns parâmetros, fazendo com que o site permita o acesso.
        """
        
        url3 = "http://www.fundamentus.com.br/detalhes.php?papel="+ self.ação
        req = Request(url3, headers={'User-Agent': 'Chrome/84.0.4147.105'})
        webpage = urlopen(req).read()
        # Forma mais simples de remover os pontos separando os milhares.
        df1 = pd.read_html(webpage, decimal=',', thousands='.')
        df1 = df1[1]
        # Coleta do número de ações da empresa alvo.
        n_ações = float(df1[3][1])
        # O Site fundamentus já fornece todos os dados que queremos, porém irei calcular a fim de treino e aprendizado.
        df_m = pd.DataFrame()
        df_m["Lucro por Ação (LPA)"] = (df_DRE.loc["Lucro Líquido - (R$)"] / n_ações)*1000000
        
        bond_i_list = []
        bond_f_list = []
        for c in df_DRE.columns:
                # 5 = Saturday and 6 = Sunday
                date_i = datetime(year=int(c),month=1,day=2)
                if date_i.weekday() != 5 and date_i.weekday() != 6:
                    pass
                else:
                    if date_i.weekday() == 5:
                        date_i = datetime(year=int(c),month=1,day=2+2)
                    else:
                        date_i = datetime(year=int(c),month=1,day=2+1)
                        
                date_f = datetime(year=int(c),month=12,day=29)
                if date_f.weekday() != 5 and date_f.weekday() != 6:
                    pass
                else:
                    if date_f.weekday() == 5:
                        date_f = datetime(year=int(c),month=12,day=29-1)
                    else:
                        date_f = datetime(year=int(c),month=12,day=29-2)
                        
                for i in range(0,len(self.bond)):
                    if self.bond['Date'][i] == date_i:
                        bond_i = self.bond['Close'][i]
                        bond_i_list.append(bond_i)
                    if self.bond['Date'][i] == date_f:
                        bond_f = self.bond['Close'][i]
                        bond_f_list.append(bond_f)
                        
        retorno_anual = []
        for i in range(0,len(bond_i_list)):
            retorno_anual.append(round(((bond_f_list[i] - bond_i_list[i])/bond_i_list[i])*100,2))
        # Adicionando os valores no DataFrame
        df_m = df_m.T
        df_m = df_m.append(pd.Series(data=bond_f_list, index=df_DRE.columns, name = "Preço Ação R$ (final do ano)"))
        P = df_m.loc['Preço Ação R$ (final do ano)'] / df_m.loc['Lucro por Ação (LPA)']
        ROE = df_DRE.loc['Lucro Líquido - (R$)'] / df_BP.loc['Patrimônio Líquido Consolidado - (R$)'] * 100
        ROIC = (df_DRE.loc['EBIT - (R$)'] + df_DRE.loc['Impostos - (R$)']) / (df_BP.loc['Patrimônio Líquido Consolidado - (R$)'] + df_DRE.loc['Dívida Bruta - (R$)'])*100
        ROA = df_DRE.loc['Lucro Líquido - (R$)'] / df_BP.loc['Ativo Total - (R$)'] * 100
        Giro_ativo = df_DRE.loc['Receita Líquida - (R$)'] / df_BP.loc['Ativo Total - (R$)']
        df_m = df_m.append(pd.Series(data=P, index=df_DRE.columns, name = "P/L"))
        df_m = df_m.append(pd.Series(data=ROA, index=df_DRE.columns, name= "ROA (%)"))
        df_m = df_m.append(pd.Series(data=ROE, index=df_DRE.columns, name = "ROE (%)"))
        df_m = df_m.append(pd.Series(data=ROIC, index=df_DRE.columns, name = "ROIC (%)"))
        df_m = df_m.append(pd.Series(data=Giro_ativo, index=df_DRE.columns, name='Giro Ativo'))
        df_m = df_m.append(pd.Series(data=retorno_anual, index=df_DRE.columns, name = "Retorno Anual (%)"))
        df_m = df_m.append(pd.Series(data=[round(i * n_ações / (1*10**9), 2) for i in bond_f_list], index=df_DRE.columns, name = "Valor de Mercado (Bilhões)"))

        display(df_BP)
        display(df_BP_VH)
        display(df_DRE)
        display(df_DRE_VH)
        display(df_FC)
        display(df_FC_VH)
        display(df_m)
        display(df_solvencia)
        display(fig1)
        display(fig2)
        display(fig3)
        display(fig4)
        display(fig5)
        display(fig6)
    
    def Oscilações(self):
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
        
    def Variações_Diária(self):
        data = datetime.today()
        self.Data(data)
        year = self.data
        dia = int(year.strftime('%d'))
        mes = int(year.strftime('%m'))
        ano = int(year.strftime('%Y'))
        year = datetime(year=ano,month=mes,day=dia)
        df_vard = pd.DataFrame()
        bonds = []
        bonds_err = []
        var = []
        setor = []
        for i in range(0,len(self.df_setor)):
            bond = yf.download(self.df_setor['Papel'][i]+'.SA',start=year)
            try:
                bond['Close'][0]
                bonds.append(self.df_setor['Papel'][i])
                setor.append(self.df_setor['Setor'][i])
                try:
                    var.append((bond['Close'][0]-bond['Open'][0])/ bond['Open'][0] *100)
                except:
                    var.append(0)
            except Exception:
                bonds_err.append(self.df_setor['Papel'][i])
                
        #Transformando os dados em DF
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
        df_neg = df_neg.T
        #Treemap
        fig = go.Figure()
        fig1 = px.treemap(df_pos, path=['Status','Papel'], values='Var Diária (%)', hover_data = ['Setor'],
                        color ='Var Diária (%)',
                        color_continuous_scale='greens',
                        color_continuous_midpoint=np.average(df_pos['Var Diária (%)'], weights=df_pos['Var Diária (%)']),
                        title='Variações Positivas em '+str(dia)+'/'+str(mes)+"/"+str(ano))
        
        fig2 = px.treemap(df_neg, path=['Status','Papel'], values='Var Diária (%)', hover_data=['Setor'],
                        color ='Var Diária (%)',
                        color_continuous_scale='reds',
                        color_continuous_midpoint=np.average(df_neg['Var Diária (%)'], weights=df_neg['Var Diária (%)']),
                        title='Variações Negativas em '+str(dia)+'/'+str(mes)+"/"+str(ano))
        fig1.show()
        fig2.show()
    
    def Comparação(self, resp):
        lista = []
        lista.append(self.ação)
        ação = ''
        if resp != str(2):
            while ação != 'QUIT':
                test = 0
                ação = input('Digite a(s) ação(s) que deseja comparar com '+' '.join(map(str,lista))+'\n *Para sair digite "quit"').upper()
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
            x = 0
            colors = ['Blue','Red','Green','Yellow','Orange','Cian']
            for i in lista:
                # Ação até o dia atual
                bond = yf.download(i+'.SA', end=datetime.today())
                fig.add_trace(go.Scatter
                            (x=bond.index,
                            y=bond['Close'],
                            name=i,
                            line=dict(color=colors[x])))
                # Ação na data estipulada até o dia atual
                bond = yf.download(i+'.SA',start=start, end=datetime.today())
                fig2.add_trace(go.Scatter
                             (x=bond.index,
                             y=(bond['Close']/bond['Close'].iloc[0]),
                             name= i,
                             line=dict(color=colors[x])))
                # Análise do volume na data estipulada
                fig3.add_trace(go.Scatter
                              (x=bond.index,
                               y=bond['Volume'],
                               name=i,
                               line=dict(color=colors[x])))
                # Análise da variação diária da ação
                fig4.add_trace(go.Histogram
                              (x=bond['Close'].pct_change(1),
                              name=i,
                              histnorm='',
                              opacity=0.75))
                x += 1
          
            # Gráfico cumulativo comparativo com o ibovespa
            ibov = yf.download('^BVSP', start=start, end=datetime.today())
            fig2.add_trace(go.Scatter
                             (x=ibov.index,
                             y=(ibov['Close']/ibov['Close'].iloc[0]),
                             name='IBOVESPA',
                             line=dict(color='Black')))
            
            self.Fig_Update(fig, resp)
            fig.update_layout(title_text=' '.join(map(str,lista))+' Close')
            fig2.update_layout(title_text=' '.join(map(str,lista))+' IBOV'+' Cumulative a partir de '+start.strftime('%d')+
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
            
            # Comparação entre os balanços (Apenas ações brasileiras)
            df_BP_COMP = pd.DataFrame()
            df_DRE_COMP = pd.DataFrame()
            df_FC_COMP = pd.DataFrame()
            for i in lista:
                self.Balanço_Patrimonial(i)
                self.DRE(i)
                self.Fluxo_de_Caixa(i)
                df_BP_COMP[i+' 2019'] = self.df_BP['2019']
                df_DRE_COMP[i+' 2019'] = self.df_DRE['2019']
                df_FC_COMP[i+' 2019'] = self.df_FC['2019']
            display(df_BP_COMP)
            display(df_DRE_COMP)
            display(df_FC_COMP)
        
        # Para as ações americanas
        else:
            while ação != 'QUIT':
                test = 0
                ação = input('Digite a(s) ação(s) que deseja comparar com '+' '.join(map(str,lista))+'\n *Para sair digite "quit"').upper()
                if ação != 'QUIT':
                    lista.append(ação)
            print(lista)
            start = datetime(year=int(input('Digite o ano: ')),month=int(input('Digite o mês: ')),day=int(input('Digite o dia: ')))
            fig = go.Figure()
            fig2 = go.Figure()
            fig3 = go.Figure()
            fig4 = go.Figure()
            x = 0
            colors = ['Blue','Red','Green','Yellow','Orange','Black','White']
            for i in lista:
                bond = yf.download(i, end=datetime.today())
                fig.add_trace(go.Scatter
                            (x=bond.index,
                            y=bond['Close'],
                            name=i,
                            line=dict(color=colors[x])))
                bond = yf.download(i, start=start, end=datetime.today())
                fig2.add_trace(go.Scatter
                              (x=bond.index,
                               y=(bond['Close']/bond['Close'].iloc[0]),
                              name=i,
                              line=dict(color=colors[x])))
                # Análise do volume na data estipulada
                fig3.add_trace(go.Scatter
                              (x=bond.index,
                               y=bond['Volume'],
                               name=i,
                               line=dict(color=colors[x])))
                
                fig4.add_trace(go.Histogram
                              (x=bond['Close'].pct_change(1),
                              name=i,
                              histnorm='',
                              opacity=0.75))                  
                x += 1
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

analise = Bond_Analisys()
Bond_Analisys.initialize(analise)

