from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('crimedata.csv')

app = Dash(__name__)

app.layout = html.Div(children=[

    html.Div([
        html.Div([
            dcc.Dropdown(
                ["murders", "rapes", "robberies", "assaults", "burglaries", "larcenies", "autoTheft", "arsons"],
                "murders", id="feature")],
            style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='graphic')
    ]),
    html.Div([
        dcc.Graph(id='full-graphic'),
        html.Div("Choose maximum percent of retirements"),
        dcc.Slider(id="pctWRetire",
                   min=df["pctWRetire"].min(),
                   max=df["pctWRetire"].max(),
                   step=10),

        html.Div("Choose maximum percent of population under povetry"),
        dcc.Slider(id="PctPopUnderPov",
                   min=df["PctPopUnderPov"].min(),
                   max=df["PctPopUnderPov"].max(),
                   step=10
                   ),

        html.Div("Choose maximum percent of unemployed population"),
        dcc.Slider(id="PctUnemployed",
                   min=df["PctUnemployed"].min(),
                   max=df["PctUnemployed"].max(),
                   step=10
                   ),
        html.Div("Choose maximum perceent of working moms"),
        dcc.Slider(id="PctWorkMom",
                   min=df["PctWorkMom"].min(),
                   max=df["PctWorkMom"].max(),
                   step=10
                   ),

        html.Div("Choose maximum percent of people not speaking English well"),
        dcc.Slider(id="PctNotSpeakEnglWell",
                   min=df["PctNotSpeakEnglWell"].min(),
                   max=df["PctNotSpeakEnglWell"].max(),
                   step=10
                   ),
    ])
])


@app.callback(
    Output('graphic', 'figure'),
    Input('feature', 'value'))
def update_graph(feature_value):
    df_filtered = df.groupby('state').agg(
        {"murders": 'mean', "rapes": 'mean', "robberies": 'mean', "assaults": 'mean', "burglaries": 'mean',
         "larcenies": 'mean',
         "autoTheft": 'mean', "arsons": 'mean'}).reset_index()

    fig = px.histogram(
        df_filtered,
        y=df_filtered[feature_value],
        x='state',
        nbins=50)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 30, 'r': 40},
                      hovermode='closest',
                      xaxis_title='states',
                      yaxis_title="Featured crime count",
                      title="Crimes Count by Different Features")

    return fig


@app.callback(
    Output('full-graphic', 'figure'),
    Input('feature', 'value'),
    Input('pctWRetire', 'value'),
    Input('PctPopUnderPov', 'value'),
    Input('PctUnemployed', 'value'),
    Input('PctWorkMom', 'value'),
    Input('PctNotSpeakEnglWell', 'value'))
def update_full_graph(feature, pctWRetire, PctPopUnderPov, PctUnemployed, PctWorkMom, PctNotSpeakEnglWell):
    local_df = df[df["pctWRetire"] <= pctWRetire]
    local_df = local_df[local_df["PctPopUnderPov"] <= PctPopUnderPov]
    local_df = local_df[local_df["PctUnemployed"] <= PctUnemployed]
    local_df = local_df[local_df["PctWorkMom"] <= PctWorkMom]
    local_df = local_df[local_df["PctNotSpeakEnglWell"] <= PctNotSpeakEnglWell]

    fig = px.histogram(local_df,
                       x="population",
                       y=[feature])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 30, 'r': 40}, hovermode='closest',
                      xaxis_title="Population",
                      yaxis_title="Crimes Count")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
