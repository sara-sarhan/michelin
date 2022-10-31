
import os

import pandas as pd
class Controller:

    def __init__(self):


        self.countDialog=0
        self.chat_history=''
        self.user =None
        self.altroProdotto=         'Parametro'
        self.domanda=[]
        self.risposta=[]
        self.visualizza = []
        self.df1=''
        self.name=''
        #self.df = pd.read_excel('bot_par.xlsx')
        xls = pd.ExcelFile('ELENCO_DATI_E_RELAZIONI_v2.xlsx')
        self.df = pd.read_excel(xls, 'ESEMPIO REAZIONE')

        self.operatore = list(set(self.df['Operatore (utente)'].tolist()))
        self.TipoMacchinario =list(  set(self.df['Tipo Macchinario'].tolist()))
        self.ModelloScheda = list( set(self.df['Modello Scheda'].tolist()))
        self.TipiSchede = list( set(self.df['Tipi Schede'].tolist()))
        self.Prodotto = list( set(self.df['Prodotto'].tolist()))
        self.VISUALIZZAZIONEProtezioneCliente = list( set(self.df['VISUALIZZAZIONE ProtezioneCliente '].tolist()))
        self.Parametro =list(  set(self.df['Parametro'].tolist()))
        self.VISUALIZZAZIONEVerifiche =list(  set(self.df['VISUALIZZAZIONE Norme/Verifiche'].tolist()))
        self.userlist=list(  set(self.df['User'].tolist()))
        self.listaparametri = self.userlist

    #
    def set_user(self, user):
           self.user.append(user)
    def get_user(self):
            return self.user






