import dash
import dash_auth
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import math
import pandas as pd


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Mickey': 'Mouse', 'Donald': 'Duck', 'Sudha': 'Akula'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='auth_plus_charts'
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Dictionary with dataframes for each continent
continent_names = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']


# get data from plotly express
df = px.data.gapminder()
df_2007 = df[df['year']==2007]
df_2007 = df_2007.sort_values(['continent', 'country'])

hover_text = []
bubble_size = []

for index, row in df_2007.iterrows():
    hover_text.append(('Country: {country}<br>'+
                      'Life Expectancy: {lifeExp}<br>'+
                      'GDP per capita: {gdp}<br>'+
                      'Population: {pop}<br>'+
                      'Year: {year}').format(country=row['country'],
                                            lifeExp=row['lifeExp'],
                                            gdp=row['gdpPercap'],
                                            pop=row['pop'],
                                            year=row['year']))
    bubble_size.append(math.sqrt(row['pop']))
    

df_2007['text'] = hover_text
df_2007['size'] = bubble_size
sizeref = 2.*max(df_2007['size'])/(100**2)


app.layout = html.Div([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),
    dcc.Dropdown(
        id='dropdown',
        #options=[{'label': i, 'value': i} for i in [1, 2, 3, 4, 5]],
        options=[{'label': i, 'value': i} for i in continent_names],
        value='Africa'
    ),

    html.Div(id='graph-title'),
    dcc.Graph(id='graph'),
    html.A('Auth Code on Github', href='https://github.com/austinlasseter/dash-auth-example'),
    html.Br(),
    html.A('Plotly Code on Github', href='https://plotly.com/python/bubble-charts/'),
    html.Br(),
    html.A("Data Source", href='https://dash.plotly.com/authentication'),
], className='container')

@app.callback(
    Output('graph-title', 'children'),
    Output('graph', 'figure'),
    Input('dropdown', 'value'),
    )


def update_graph(dropdown_value):

#     x_values = [-3,-2,-1,0,1,2,3]
#     y_values = [x**dropdown_value for x in x_values]
#     colors=['black','red','green','blue','orange','purple']
    graph_title='Life Expectancy vs Per Capita GDP 2007 {}'.format(str(dropdown_value))

    #df_2007 = df_2007.query("continent == '%s'" %dropdown_value)
    
    fig = px.scatter(df_2007.query("continent == '%s'" %dropdown_value), x="gdpPercap", y="lifeExp",
	         size="pop", color="country",
                 hover_name="country", log_x=True, size_max=60)
   
    # fig.show()  
    return graph_title, fig

    # trace0 = go.Scatter(
    #     x = x_values,
    #     y = y_values,
    #     mode = 'lines',
    #     marker = {'color': colors[dropdown_value]},
    # )

    # assign traces to data
    # data = [trace0]
    # layout = go.Layout(
    #     title = graph_title
    #)

    # Generate the figure dictionary
#     fig = go.Figure(data=data,layout=layout)

#     return graph_title, fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
