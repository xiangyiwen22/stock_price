from flask import Flask, render_template, request, redirect
import requests
import json as simplejson
import pandas as pd
from bokeh.charts import TimeSeries, show, output_file
from bokeh.embed import components 

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from datetime import datetime
from bokeh.palettes import Spectral4


def showplot(htmlinput, showdata, ticker):
    p = figure(plot_width=800, plot_height=500, x_axis_type="datetime")
    color={'open':Spectral4[0],
           'high':Spectral4[1],
           'low':Spectral4[2],
           'close':Spectral4[3]}
    p.title.text = 'Quandl WIKI %s stock price(click on legend entries to hide the corresponding lines)'%ticker
    #p.legend.location = "bottom"
    p.grid.grid_line_alpha=0
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = .2
    #p.xgrid.band_fill_alpha = 1
    for i in htmlinput:
        p.line(showdata['date'], showdata[i], legend=i, 
                                              alpha=0.8,
                                              line_width=2, 
                                              line_color=color[i])
    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    return p
    

app = Flask(__name__) #root path



@app.route('/')
def index():
  return render_template('index.html')

@app.route('/result', methods=['POST']) # home page
def result():
  #ticker=request.form['dataset_code']
  htmlinput=request.form.getlist('check')
  ticker=request.form['dataset_code']
  r=requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?api_key=tBXpG5nLBevqCdXXFi1U')
  json_object=r.json()
  data=json_object['dataset']['data']
  showdata = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
#showdata = {"date": [], "open": []}
  for arr in data:
      showdata['date'].append(datetime.strptime(arr[0], '%Y-%m-%d'))
      showdata['open'].append(arr[1])
      showdata['high'].append(arr[2])
      showdata['low'].append(arr[3])
      showdata['close'].append(arr[4])
      #showdata['volume'].append(arr[5])
  #htmlinput=['open','close']
  plot=showplot(htmlinput, showdata, ticker)
  script,div=components(plot)
  print htmlinput
  return render_template('result.html', script=script, div=div)

  
if __name__ == '__main__':
  app.run(port=33507, debug=True, use_reloader=False)
