from os.path import dirname, join

import json
import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.transform import factor_cmap
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource, Div

# parties = pd.read_csv("D:/UnFound/Task - Bokeh Visualization/data/parliament_members_data.csv")

axis_map = {
    "Debates Participated": "Debates Participated",
    "Private Member Bills": "Private Member Bills",
    "Questions Raised": "Questions Raised",
    "Attendance": "Attendance",
}

average_scores = {
    "Debates Participated": 67.1,
    "Private Member Bills": 2.3,
    "Questions Raised": 293,
    "Attendance": 80,
}

end_range = {
    "Debates Participated": 500,
    "Private Member Bills": 50,
    "Questions Raised": 500,
    "Attendance": 100,
}

with open("movies/party_scores.json", "r") as file:
    party_scores = json.load(file)

"""
desc = Div(text=open(
    "D:/UnFound/git_repositories/interactive_visualizations/interactive_visualization/app/movies/description.html").read(),
           width=800)"""

desc = Div(text=open(join(dirname(__file__), 'description.html')).read(),
           width=800)

# Input Controls
party = Select(title="Party", value="Bharatiya Janata Party",
               options=open(join(dirname(__file__), 'parties.txt')).read().split("\n"))
parameter = Select(title="Parameter", options=sorted(axis_map.keys()), value="Attendance")

party_score = party_scores[party.value][parameter.value]
average_score = average_scores[parameter.value]

x_data = ["Party Score", "Overall Average"]
y_data = [party_score, average_score]

source = ColumnDataSource(data=dict(x_data=x_data, y_data=y_data))

p = figure(x_range=x_data, plot_height=450, toolbar_location=None, title="")
p.vbar(x='x_data', top='y_data', width=0.6, source=source,
       line_color='white', fill_color=factor_cmap('x_data', palette=['#DD4968', '#277E8E'], factors=x_data))

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 300


def update():
    party_name = party.value
    parameter_name = parameter.value
    if party_name != "Bharatiya Janata Party" or parameter.value != "Attendance":
        party_score = party_scores[party_name][parameter_name]
        parameter_score = average_scores[parameter_name]

        p.xaxis.axis_label = party_name
        p.yaxis.axis_label = parameter_name
        p.title.text = "Showing parliament stats for: %s " % party.value
        source.data = dict(
            x_data=["Party Score", "Overall Average"],
            y_data=[party_score, parameter_score],
        )
        # print(source.data)


controls = [party, parameter]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = column(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Indian Political Parties"

