from dash import Dash, html, dcc
import dash
import os

os.environ['suppress_callback_exceptions'] = 'True'

app = Dash(__name__, use_pages=True)

button_style = {'background-color': 'darkorange', 'color': 'white', 'fontWeight': 'bold', 'fontFamily': 'sans', 'border': '0px', 'border-radius': '5%', 'padding': '5px', 'margin': '5px'}

pages = {}
for page in dash.page_registry.values():
	pages[page['name']] = page['relative_path']

app.layout = html.Div([
	html.Div([html.Label('HIERARCHICAL STOCK OVERVIEW', style={'fontWeight': 'bold', 'fontFamily': 'sans', 'color': 'darkorange', 'fontSize': 18})], style={'display': 'inline-block'}),
	html.Div([dcc.Link(html.Button(list(pages.keys())[0], style=button_style), href=list(pages.values())[0])], style={'display': 'inline-block', 'margin-left': '1100px'}),
	html.Div([dcc.Link(html.Button(list(pages.keys())[1], style=button_style), href=list(pages.values())[1])], style={'display': 'inline-block', 'margin-left': '20px'}),
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True, host='0.0.0.0', port=8050)
