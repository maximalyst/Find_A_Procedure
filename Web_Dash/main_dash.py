import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sqlite3

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# SQLite Database Connection
conn = sqlite3.connect('../CIFP_parse.sqlite')
cursor = conn.cursor()

app.layout = html.Div([
    dbc.Container([
        html.H1("SQLite Database Search", className="display-4"),
        dbc.Input(id='search-input', type='text', placeholder='Enter text to search...'),
        dbc.Button("Search", id='search-button', color="primary", className="mt-2"),
        html.Div(id='search-results', className='mt-3')
    ])
])


@app.callback(
    Output('search-results', 'children'),
    [Input('search-button', 'n_clicks')],
    [dash.dependencies.State('search-input', 'value')]
)
def search_database(n_clicks, search_term):
    if n_clicks is not None and search_term:
        # Execute a search query in your SQLite database
        cursor.execute("SELECT * FROM PF WHERE airHeli_portIdent_id LIKE ?", (f"%{search_term}%",))
        results = cursor.fetchall()

        if results:
            result_html = html.Ul([html.Li(result[0]) for result in results])
        else:
            result_html = html.P("No results found.")

        return result_html
    else:
        return html.P("Enter a search term and click the 'Search' button.")


if __name__ == '__main__':
    app.run_server(debug=True)
