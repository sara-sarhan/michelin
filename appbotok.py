import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import time
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

# Define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

import warnings

warnings.filterwarnings('ignore')
import os
import controller

Ct = controller.Controller()

Ct.domanda = ["Salve! Puoi dirmi chi sei?"]
Ct.risposta = "hai selezionato l'operatore"
Ct.risposta = []


def textbox(text, box="other", value=''):
    style = {
        "max-width": "75%",
        "width": "max-content",
        "padding": "10px 15px",

        "border-radius": "25px",
        "margin-bottom": "2px",
        "width": "50%",
    }

    if box == "self":
        style["margin-right"] = 0
        style["margin-left"] = "auto"
        color = "primary"
        inverse = True

        thumbnail = html.Img(
            src="https://w7.pngwing.com/pngs/312/283/png-transparent-man-s-face-avatar-computer-icons-user-profile-business-user-avatar-blue-face-heroes-thumbnail.png",
            style={
                "border-radius": 50,
                "height": 36,

                "margin-left": 5,
                "float": "right",
            },
        )

        textbox = dbc.Card(html.Div([

            html.H5(" Seleziona  ", className="card-title"),
            dcc.Dropdown(Ct.listaparametri, id='demo-dropdown',
                         style={'background-color': color, 'border-color': '#808080', 'color': '#ffab00'}),
            html.Div(id='dd-output-container'),
        ]), style=style, body=True, color=color, inverse=inverse
        )



    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "75%"
        color = "danger"
        inverse = True

        style = {
            "max-width": "75%",
            "width": "max-content",
            "padding": "10px 15px",

            "border-radius": "25px",
            "margin-bottom": "2px",
        }

        thumbnail = html.Img(
            src="https://w7.pngwing.com/pngs/1001/63/png-transparent-internet-bot-computer-icons-chatbot-sticker-electronics-face-careobot-thumbnail.png",
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )

        if Ct.user in Ct.Prodotto:

            # r = list(set(Ct.df1['VISUALIZZAZIONE ProtezioneCliente '].tolist()))
            r = Ct.visualizza[-1]
            textbox = dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(" Protezione Cliente ", className="card-title"),
                        html.P(
                            r
                        ),
                        html.Div([
                            Ct.domanda[-1],
                            dcc.Dropdown(Ct.listaparametri, id='demo-dropdown',
                                         style={'background-color': color, 'border-color': '#808080',
                                                'color': '#ffab00'}),
                            html.Div(id='dd-output-container'),
                        ]),

                    ]
                ),
                style=style, body=True, color=color, inverse=inverse
            )


        elif Ct.user in Ct.Parametro:
            from PIL import Image  # new import
            import base64

            images_files = [f for f in os.listdir(PATH.joinpath("data/foto")) if f.endswith('.jpg')]
            text = Ct.visualizza[-1]

            norma = text[text.find('NORMA'):text.find('AZIONI')].strip().capitalize()
            azioni = text[text.find('AZIONI'):].strip().capitalize()

            textbox1 = [dbc.Card(
                dbc.CardBody(
                    [html.H4("Informazioni sul parametro scelto", className="card-title"),
                     html.H3("Visualizzazione Norme/Verifiche", className="card-title"),
                     # html.H6("Card subtitle", className="card-subtitle"),
                     html.P(
                         norma,
                         className="card-text",
                     ),
                     html.P(
                         azioni,
                         className="card-text",
                     ),

                     ],
                ),
                style=style, body=True, color=color, inverse=inverse
            )]

            if Ct.risposta[3] in images_files[0]:
                for i in images_files:
                    pil_image = Image.open(os.path.join(os.getcwd(), 'data/foto', i))

                    textbox1.append(
                        html.Img(src=pil_image,

                                 style=style
                                 ))
            textbox = html.Div(textbox1)

        else:
            textbox = dbc.Card(Ct.domanda[-1], style=style, body=True, color=color, inverse=inverse)

    else:
        raise ValueError("Incorrect option for `box`.")

    return [thumbnail, textbox]  # html.Div([thumbnail, textbox,''])


refreshpage = html.Div(
    [dcc.Location(id='url', refresh=True),
     dbc.Button(
         "Refresh Data",

         id="cleanbtn",

         color="primary",
     ),
     ]
)

conversation = html.Div(

    id="display-conversation",
)
listchat = html.Div([
    dcc.Dropdown(['NYC', 'MTL', 'SF'], id='demo-dropdown'),
    html.Div(id='dd-output-container')
], style={'display': 'none'})

# Define Layout
app.layout = dbc.Container(
    fluid=True,
    children=[

        html.Div([
            html.Div(html.Img(
                src="https://logos-download.com/wp-content/uploads/2016/03/Michelin_Logo_1997.png",
                style={
                    "margin-top": 5,
                    "margin-bottom": 2,
                    "height": 150,
                    "margin-right": 10,
                }
            ), style={'display': 'flex', 'height': 'auto', 'justify-content': 'center'}),
            # html.Div(html.H1("Bot"),style={'display': 'inline-block', 'height': 'auto', 'color': 'orange'}),
            dcc.Location(id='url', refresh=True),
            dbc.Button(
                "Refresh Data",

                id="cleanbtn",

                color="primary", style={
                    "margin-left": "25%",

                    "width": "50%",
                    "height": "80%",
                    "fontSize": "1em",
                    "background-color": "#fde903",
                    "color": " #2972b3",
                    "border-radius": "6px",
                    "border": "2px solid #2972b3",
                    "margin-top": "2px",
                    # "margin-right":"30%"
                },
            ),
        ]),

        html.Hr(),

        dcc.Store(id="store-conversation", data=""),
        conversation,
        listchat,
        html.Br(),

        # controls,

    ],
)


@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data"), ]
)
def update_display(chat_history):
    # print("update_display",chat_history)

    style = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px 15px",

        "border-radius": "25px",
        "margin-bottom": "2px",
    }
    styleuser = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px 15px",

        "border-radius": "25px",
        "margin-bottom": "2px",
    }

    time.sleep(2)
    value = Ct.user

    if value is not None:
        print(f"Risposta utente ---> {value}")
        time.sleep(1)
        Ct.risposta.append(value)

    print(f"Riempio la variabile del controller? ---> {Ct.risposta}")


    if value in Ct.userlist:
        df = Ct.df
        df2 = df[(df['User'] == Ct.risposta[0])]
        Ct.name = list(set(df2['Operatore (utente)'].tolist()))[0]
        df1 = df[(df['Operatore (utente)'] == Ct.name)]
        Ct.listaparametri = list(set(df1['Tipi Schede'].tolist()))  # Ct.TipiSchede
        Ct.df1 = df1

        Ct.listaparametri = list(set(df1['Tipo Macchinario'].tolist()))

        Ct.domanda.append("Ciao " + Ct.name.capitalize() + ' ' + value + '! Scegli il tipo di macchinario')

    elif value in Ct.TipoMacchinario:
        df = Ct.df1
        df1 = df[(df['Operatore (utente)'] == Ct.name) & (df['Tipo Macchinario'] == Ct.risposta[1])]
        Ct.df1 = df1
        Ct.listaparametri = list(set(df1['Modello Scheda'].tolist()))

        Ct.domanda.append('Scegli il tipo di Modello Scheda')
    elif value in Ct.ModelloScheda:
        df = Ct.df1

        df1 = df[(df['Operatore (utente)'] == Ct.name) & (df['Tipo Macchinario'] == Ct.risposta[1]) & (
                df['Modello Scheda'] == Ct.risposta[2])]
        Ct.listaparametri = list(set(df1['Tipi Schede'].tolist()))  # Ct.TipiSchede
        Ct.domanda.append('Scegli Tipi Schede')

        Ct.df1 = df1
    elif value in Ct.TipiSchede:
        df = Ct.df1
        df1 = df[(df['Operatore (utente)'] == Ct.name) & (df['Tipo Macchinario'] == Ct.risposta[1]) & (
                df['Modello Scheda'] == Ct.risposta[2]) & (df['Tipi Schede'] == Ct.risposta[3])]
        Ct.listaparametri = list(set(df1['Prodotto'].tolist()))
        Ct.domanda.append('Scegli il tipo di Prodotto da visualizzare')
        Ct.df1 = df1
    elif value in Ct.Prodotto:
        df = Ct.df1
        df1 = df[(df['Operatore (utente)'] == Ct.name) & (df['Tipo Macchinario'] == Ct.risposta[1]) & (
                df['Modello Scheda'] == Ct.risposta[2]) & (df['Tipi Schede'] == Ct.risposta[3]) & (
                         df['Prodotto'] == Ct.risposta[4])]
        Ct.df1 = df1
        r = list(set(df1['VISUALIZZAZIONE ProtezioneCliente '].tolist()))
        Ct.visualizza.append(r[-1])

        Ct.domanda.append('Scegli il tipo di Parametro da visualizzare')
        Ct.listaparametri = list(set(df1['Parametro'].tolist()))

    elif value in Ct.Parametro:
        df = Ct.df1
        df1 = df[(df['Operatore (utente)'] == Ct.name) & (df['Tipo Macchinario'] == Ct.risposta[1]) & (

                df['Modello Scheda'] == Ct.risposta[2]) & (df['Tipi Schede'] == Ct.risposta[3]) & (
                         df['Prodotto'] == Ct.risposta[4]) & (df['Parametro'] == Ct.risposta[5])]

        r = list(set(df1['VISUALIZZAZIONE Norme/Verifiche'].tolist()))
        Ct.visualizza.append(r[-1])


    history = [i for i in chat_history.split("<split>")[:-1] if str(i) != 'None']



    l = [
        textbox(x, box="AI") if i % 2 == 0 else textbox(x, box="self", value=value)
        for i, x in enumerate(history
                              # .split(tokenizer.eos_token)[:-1]
                              )
    ]

    counter = 0
    cd = 0

    # print('update_display history', history)
    for i in range(len(history) - 1):

        # print(i, i % 2 != 0)
        if (i % 2 != 0 and len(Ct.risposta) > 0) or (
                i % 2 != 0 and len(Ct.risposta) and Ct.risposta[-1] in Ct.Parametro):

            styleuser["margin-right"] = 0
            styleuser["margin-left"] = "auto"
            color = "primary"
            inverse = True

            # else:
            text = Ct.risposta[
                counter]  # + f'Hai selezionato il valore:  {Ct.risposta[c]}'  # qua in una variabile nel control magari metto la domanda,
            l[i][-1] = dbc.Card(text, style=styleuser, body=True, color=color, inverse=inverse)
            counter += 1
            # print("user  len(Ct.risposta)", len(Ct.risposta), l[i][-1])

        elif i % 2 == 0 and cd <= len(Ct.domanda) - 1:
            style["margin-left"] = 0
            style["margin-right"] = "75%"
            color = "danger"
            inverse = True
            if Ct.domanda[cd] == 'Scegli il tipo di Parametro da visualizzare':
                # print("Parametro.....", )
                text = Ct.visualizza[0]
                quando = text[text.find('QUANDO'):text.find('ProtezioneCliente')].strip().capitalize()
                nomra = text[text.find('ProtezioneCliente') + len('ProtezioneCliente'):text.find(
                    'AZIONI')].strip().capitalize()
                azioni = text[text.find('AZIONI'):].strip().capitalize()
                # + f'Hai selezionato il valore:  {Ct.risposta[c]}'  # qua in una variabile nel control magari metto la domanda,
                l[i][-1] = dbc.Card(
                    dbc.CardBody(
                        [html.H5("Informazioni sul prodotto scelto.", className="card-title"),

                         html.P(quando),

                         html.H5("Protezione Cliente"),
                         # html.H6("Card subtitle", className="card-subtitle"),
                         html.P(
                             nomra,
                             className="card-text"
                         ),
                         html.P(
                             azioni,
                             className="card-text"
                         ),
                         html.Br(),
                         html.H5(Ct.domanda[cd], className="card-title"),
                         ]
                    ),
                    style=style, body=True, color=color, inverse=inverse
                )


            else:
                text = Ct.domanda[
                    cd]  # + f'Hai selezionato il valore:  {Ct.risposta[c]}'  # qua in una variabile nel control magari metto la domanda,
                l[i][-1] = dbc.Card(text, style=style, body=True, color=color, inverse=inverse)

            cd += 1

    tex = [html.Div([i[0], i[1], '']) for i in l]
    if len(Ct.risposta) > 5:
        tex = tex[0:-1]

    return tex


@app.callback(

    Output("url", "href"),
    Input("cleanbtn", "n_clicks"),
)
def reload_data(n):
    if n:
        Ct.user = ''

        Ct.domanda = ["Salve! Puoi dirmi chi sei?"]
        Ct.risposta = []
        Ct.visualizza = []
        Ct.df1 = ''
        Ct.listaparametri = Ct.userlist
        return '/', ''


@app.callback(
    [Output("store-conversation", "data"), Output('dd-output-container', 'children'), ],
    [Input('demo-dropdown', 'value')],
    [State("store-conversation", "data")],
)
def run_chatbot(value, chat_history):
    Ct.user = value

    if len(Ct.risposta) <= 5:
        chat_history += f"{Ct.domanda[-1]}<split> {value}<split>"

    return chat_history, ""


# if __name__ == "__main__":
    # app.run_server(debug=True)
    # app.run_server()
    # app.run_server(port=8051)
