from os.path import dirname, join

import json
import pandas as pd

from bokeh.io import curdoc
from bokeh.models.widgets import Select
from bokeh.layouts import layout, column
from bokeh.models import Div, HoverTool, ColumnDataSource

from bokeh.plotting import figure
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar

# Color Palettets
from bokeh.palettes import Blues9
from bokeh.palettes import Magma10
from bokeh.palettes import Viridis10


parameter_map = {
    "Click-bait": "clickbait",
    "Controversial News": "controversy",
    "Readability": "readability",
    "Spamminess": "spamminess",
    "Vagueness": "vagueness",
}


def get_data(media_scores):
    temp = {}
    temp['sources'] = media_scores['clickbait']['sources']
    temp['click_bait'] = media_scores['clickbait']['scores']
    temp['controversial_news'] = media_scores['controversy']['scores']
    temp['readability'] = media_scores['readability']['scores']
    temp['spamminess'] = media_scores['spamminess']['scores']
    temp['vagueness'] = media_scores['vagueness']['scores']

    data = pd.DataFrame.from_dict(temp)

    data = data.set_index('sources')
    data.columns.name = 'factors'

    sources = list(data.index)
    factors = list(data.columns)
    df = pd.DataFrame(data.stack(), columns=['rating']).reset_index()
    df.head()
    return df, sources, factors


def get_color_palette(color_map):
    colors = list(reversed(color_map))
    mapper = LinearColorMapper(palette=colors, low=df.rating.min(), high=df.rating.max())
    return mapper, colors


with open("D:/UnFound/git_repositories/interactive_visualizations/interactive_visualization/app/mediarank/media_scores.json", "r") as file:
    media_scores = json.load(file)

desc = Div(text=open(
    "D:/UnFound/git_repositories/interactive_visualizations/interactive_visualization/app/parliament/description.html").read(),
           width=800)
"""
desc = Div(text=open(join(dirname(__file__), 'description.html')).read(),
           width=800)"""

df, sources, factors = get_data(media_scores)
mapper, colors = get_color_palette(Blues9)


TOOLS = "save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="Media Credibility Ranking",
           x_range=factors, y_range=list(reversed(sources)),
           x_axis_location="above", plot_width=1000, plot_height=600,
           tools=TOOLS, toolbar_location='below')

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0

# create rectangle for heatmap
p.rect(x="factors", y="sources", width=1, height=1,
       source=df,
       fill_color={'field': 'rating', 'transform': mapper},
       line_color=None)

# create colorbar for label
color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="10pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%0.2f"),
                     label_standoff=12, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

# Add on-hover functionality
hover = HoverTool()
hover.tooltips = [("Source", "@sources"),
                  ("Rating", "@rating")]
p.tools.append(hover)

l = layout([
    [p]], sizing_mode="stretch_both")

curdoc().add_root(l)
curdoc().title = "Indian Media Credibility Rankings"
