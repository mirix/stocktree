import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
	html.Br(),
	html.Br(),
	html.Br(),
	dcc.Markdown('''
		**ExchangeTree** is an interactive web application that enables one to explore the most relevant stock indexes and exchanges.
		
		The app is still under development and should be considered alpha quality. 
		
		The tool is provided "as is" and we are not to be hold responsible for any inaccuracies. 
		
		The current version represents the very first working prototype and it is glitchy and very minimalistic.
		
		Bugs can be reported and additional functionality requested via [GitHub](https://github.com/mirix/stocktree).
		
		The design is currently non-responsive. It has been developed in Linux and optimised for Firefox with a 1080p desktop display.
		
		Microsoft browsers and operating systems are unable to display unicode emoji flags, whereas Google Chrome can be patched by installing an [extension](https://chrome.google.com/webstore/detail/country-flag-fixer/jhcpefjbhmbkgjgipkhndplfbhdecijh).
		
		**ExchangeTree** is build in Python by leveraging [Plotly/Dash](https://github.com/plotly/dash) technologies.
		
		Finantial information is gathered in real time by using the [StockSymbol](https://github.com/yongghongg/stock-symbol) and [yfinance](https://github.com/ranaroussi/yfinance) APIs.
		
		However, these sources may be replaced in the future.
		
		**ExchangeTree**  has two exploration modes: index mode and exchange mode, respectively. 
		
		Indexes are far from exhaustive as only the main ones are currently considered, whereas exchange mode can be a bit laggy.
		
		This app differs from existing tools in which it aims at providing a hierarchical overview whereas other apps tend to be more targeted.
		
		The current layout is intended to be explored counterclockwise from top to bottom:
		
		First one chooses a country, then a exchange or index and finally a specific stock. 
		
		Graphs are on the top row and tables on the bottom row (you may need to scroll down to see them).
		
		Graphs are somehow interactive and tables can be filtered by entering the first letters of the desired item.
		
	''', link_target="_blank",
	style={'fontFamily': 'Arial, Helvetica, sans-serif', 'color': 'grey', 'fontSize': 14, 'linkColor': 'darkorange'}),

])
