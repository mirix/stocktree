import flag
import pandas as pd
import numpy as np
from countryinfo import CountryInfo
from stocksymbol import StockSymbol
import yfinance as yf
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

api_key = '724b3358-1685-4659-92ea-1e445f283e30'
ss = StockSymbol(api_key)

market_list = ss.market_list

df = pd.DataFrame.from_dict(market_list)

df = pd.DataFrame.from_dict(market_list)
df = df[['abbreviation', 'market']].copy()

df['country'] = df['abbreviation'].apply(lambda x: CountryInfo(x).name().title() if x != 'eu' else 'Europe')
df['iso3'] = df['abbreviation'].apply(lambda x: CountryInfo(x).iso(3) if x != 'eu' else 'EUR')
df['iso2'] = df['abbreviation'].apply(lambda x: CountryInfo(x).iso(2) if x != 'eu' else 'EU')
df['flags'] = df['iso2'].apply(lambda x: flag.flag(x))
df['lat'] = df['abbreviation'].apply(lambda x: CountryInfo(x).capital_latlng()[0] if x != 'eu' else 49.845556)
df['long'] = df['abbreviation'].apply(lambda x:CountryInfo(x).capital_latlng()[1] if x != 'eu' else 9.906111)

df.loc[df['iso3'] == 'HKG', 'lat'] = 22.278333
df.loc[df['iso3'] == 'HKG', 'long'] = 114.174444

customdata = [df['country'], df['flags']]
hovertemplate = ('<br>' + customdata[0] + '  ' + customdata[1] + '<br>' + '<extra></extra>')

fig = go.Figure(data=go.Scattergeo(
        lon = df['long'],
        lat = df['lat'],
        text = df['flags'] + '<br>' + '<b>' + df['iso3'] + '</b>',
        mode = 'text+markers',
        marker = dict(size=40, color='darkorange', opacity=0.8)
        ))

fig.update_traces(textfont_size=13, customdata=customdata, hovertemplate=hovertemplate)
fig.update_geos(projection=dict(type = 'orthographic'), visible=False, resolution=110, showcountries=True, countrycolor='darkorange')
fig.update_layout(title=dict(text='EXPLORE LISTED COMPANIES BY EXCHANGE', font=dict(color='darkorange')), title_x=0.5, font=dict(color='White'), clickmode='event+select', height=900)

country = 'ch'
symbol_list = ss.get_symbol_list(market=country)
df2 = pd.DataFrame.from_dict(symbol_list)
df3 = pd.DataFrame(df2['exchange'].value_counts().reset_index().values, columns=['exchange', 'number_of_companies'])
df3['country'] =  df.loc[df['abbreviation'] == country]['iso3'].values[0] + ' ' + df.loc[df['abbreviation'] == country]['flags'].values[0]
df3 = df3[['country', 'exchange' , 'number_of_companies']]
df3 = df3.sort_values(['exchange'], ascending = [True])

ticker = 'SQN.SW'
index = 'EBS'
comp = yf.Ticker(ticker)
hist = comp.history(period='1y')
df_inx = df2.loc[df2['exchange'] == index].copy()
df_inx.drop(['shortName', 'market'], axis=1, inplace=True, errors='ignore')
df_inx = df_inx.sort_values(['longName', 'symbol'], ascending = [True, True])
df_inx = df_inx.reset_index(drop=True)
df_inx['id'] = df_inx.index

@callback([Output(component_id='table-index-exchange', component_property='data'), 
				Output(component_id='table-index-exchange', component_property='columns')],
				[Output('table-company-exchange', 'data'), Output('table-company-exchange', 'columns')], [Output('company-evolution-exchange', 'figure')],
				[Input('map-flags', 'selectedData')], [Input('table-index-exchange', 'selected_rows')], [Input('table-company-exchange', 'selected_row_ids')])
def display_selected_data(selectedData, selected_rows, selected_row_ids):
	global df
	global df3
	global df_inx
	if selectedData:
		index = selectedData['points'][0]['pointIndex']
		country = df.iloc[index]['abbreviation']
	else:
		country = 'ch'
	symbol_list = ss.get_symbol_list(market=country)
	df2 = pd.DataFrame.from_dict(symbol_list)
	df3 = pd.DataFrame(df2['exchange'].value_counts().reset_index().values, columns=['exchange', 'number_of_companies'])
	df3['country'] =  df.loc[df['abbreviation'] == country]['iso3'].values[0] + ' ' + df.loc[df['abbreviation'] == country]['flags'].values[0]
	df3 = df3[['country', 'exchange' , 'number_of_companies']]
	df3 = df3.sort_values(['exchange'], ascending = [True])
	columns = [{'name': col, 'id': col} for col in df3.columns]
	data = df3.to_dict(orient='records')
	
	if selected_rows:
		#index = selected_rows
		if selected_rows[0] > len(df3)-1:
			selected_rows = [0]
		index = df3['exchange'].iloc[selected_rows[0]]
		
	else:
		index = 'EBS'
	df_inx = df2.loc[df2['exchange'] == index].copy()

	df_inx.drop(['shortName', 'market'], axis=1, inplace=True, errors='ignore')
	df_inx = df_inx.sort_values(['longName', 'symbol'], ascending = [False, False])
	df_inx = df_inx.reset_index(drop=True)
	df_inx['id'] = df_inx.index
	columns2 = [{'name': col, 'id': col} for col in df_inx.columns[:-1]]
	data2 = df_inx.to_dict(orient='records')

	if selected_row_ids:
		if selected_row_ids[0] > len(df_inx)-1:
			selected_row_ids = [0]
		ticker = df_inx['symbol'].iloc[selected_row_ids[0]]
		comp_name = df_inx['longName'].iloc[selected_row_ids[0]]	
	else:
		ticker = 'SQN.SW'
		comp_name = 'Swissquote Group Holding Ltd'
	comp = yf.Ticker(ticker)
	hist = comp.history(period='1y')
	fig2 = go.Figure(data=go.Scatter(
			x = hist.index,
			y = hist['Close'],
			mode = 'lines',
			line = dict(color='firebrick', width=3)
			))
	        
	fig2.update_layout(
		xaxis=dict(
			showline=False,
			showgrid=True,
			showticklabels=True,
			gridcolor='WhiteSmoke',
			tickfont=dict(
				size=12,
				color='darkorange',
			),
		),
		yaxis=dict(
			showline=False,
			showgrid=True,
			showticklabels=True,
			gridcolor='WhiteSmoke',
			tickfont=dict(
				size=12,
				color='darkorange',
			),
		),
		showlegend=False,
		plot_bgcolor='white',
		title=comp_name,
		font=dict(
			size=12,
			color='darkorange'
    )
	)

	return data, columns, data2, columns2, fig2
  
layout = html.Div([
	html.Div([
	dcc.Graph(id='map-flags',
		figure=fig, style={'width': '900px', 'height': '900px'})], style={'display': 'inline-block'}),
	html.Div([
	dcc.Graph(id='company-evolution-exchange',
		figure=fig, style={'width': '900px', 'height': '600px'})], style={'display': 'inline-block'}),
	html.Div([
	html.Label('EXCHANGES', style={'fontWeight': 'bold', 'color': 'darkorange', 'fontSize': 12, 'fontFamily': 'Arial, Helvetica, sans-serif'}),
	dash_table.DataTable(id='table-index-exchange',
				style_header={'backgroundColor': 'darkorange',
					'color': 'white',
					'fontWeight': 'bold', 'fontFamily': 'Arial, Helvetica, sans-serif', 'fontSize': 12
				},
				style_data={'backgroundColor': 'white',
					'color': 'grey'
				},
				fill_width=False,
				editable=True,
				filter_action='native',
				filter_options={'case': 'insensitive'},
				sort_action='native',
				sort_mode='multi',
				#column_selectable='single',
				row_selectable='single',
				#selected_columns=[],
				selected_rows=[],
				#selected_row_ids=[],
				#fixed_rows={'headers':True, 'data':1},
				page_action='none',
				style_table={'height': '900px', 'width': '700px', 'overflowY': 'auto'}
				#page_current=0,
				#page_size=10
	)], style={'display': 'inline-block'}),
	html.Div([
	html.Label('COMPANIES', style={'fontWeight': 'bold', 'color': 'darkorange', 'fontSize': 12, 'fontFamily': 'Arial, Helvetica, sans-serif'}),
	dash_table.DataTable(id='table-company-exchange',
				style_header={'backgroundColor': 'darkorange',
					'color': 'white',
					'fontWeight': 'bold', 'fontFamily': 'Arial, Helvetica, sans-serif', 'fontSize': 12
				},
				style_data={'backgroundColor': 'white',
					'color': 'grey'
				},
				fill_width=False,
				editable=True,
				filter_action='native',
				filter_options={'case': 'insensitive'},
				sort_action='native',
				sort_mode='multi',
				#column_selectable='single',
				row_selectable='single',
				#selected_columns=[],
				selected_rows=[],
				selected_row_ids=[],
				#fixed_rows={'headers': True},
				page_action='none',
				style_table={'height': '900px', 'width': '1200px', 'overflowY': 'auto'}
				#page_current=0,
				#page_size=10
	)], style={'display': 'inline-block'}),
])


