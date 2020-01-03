from os.path import dirname, join

import json
import pandas as pd

from bokeh.io import curdoc
from bokeh.models.widgets import Select
from bokeh.transform import factor_cmap
from bokeh.layouts import layout, column
from bokeh.models import Div, HoverTool
from bokeh.models import SingleIntervalTicker, LinearAxis


from math import pi
from bokeh.palettes import Category20c
Category20c[1] = ['#3182bd']
Category20c[2] = ['#3182bd', '#6baed6']

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

# Bar Chart ---------------------------------------------------------------------------------------------------

axis_map_1 = {
    "Debates Participated": "Debates Participated",
    "Private Member's Bills": "Private Member's Bills",
    "Questions Raised": "Questions Raised",
    "Attendance": "Attendance",
}

average_scores_1 = {
    "Debates Participated": 67.1,
    "Private Member's Bills": 2.3,
    "Questions Raised": 293,
    "Attendance": 80,
}

max_scores_1 = {
    "Debates Participated": 300,
    "Private Member's Bills": 10.5,
    "Questions Raised": 737,
    "Attendance": 90.5,
}

min_scores_1 = {
    "Debates Participated": 3,
    "Private Member's Bills": 0,
    "Questions Raised": 4,
    "Attendance": 26.67,
}

max_party_1 = {
    "Debates Participated": "Revolutionary Socialist Party",
    "Private Member's Bills": "INLD",
    "Questions Raised": "AIMIM",
    "Attendance": "Apna Dal",
}

min_party_1 = {
    "Debates Participated": "JKNC",
    "Private Member's Bills": "AIADMK",
    "Questions Raised": "NDPP",
    "Attendance": "PDP",
}

max_party_1_members = {
    "Debates Participated": "Revolutionary Socialist Party",
    "Private Member's Bills": "Indian National Lok Dal",
    "Questions Raised": "All India Majlis-E-Ittehadul Muslimeen",
    "Attendance": "Apna Dal",
}

min_party_1_members = {
    "Debates Participated": "Jammu and Kashmir National Conference",
    "Private Member's Bills": "All India Anna Dravida Munnetra Kazhagam",
    "Questions Raised": "Nationalist Democratic Progressive Party",
    "Attendance": "Jammu and Kashmir Peoples Democratic Party",
}



# Load Input Data
with open("parliament/party_scores.json", "r") as file:
    party_scores = json.load(file)

with open("parliament/party_members.json", "r") as file:
    party_members = json.load(file)


hover_1 = HoverTool()
hover_1.tooltips = [
    ("Party", "@z_data_1"),
    ("No. of MPs", "@members_1"),
    ("Average per MP", "@y_data_1")
]


desc = Div(text=open(join(dirname(__file__), 'description_stats.html')).read(),
           width=1200)

desc2 = Div(text=open(join(dirname(__file__), 'description_education.html')).read(),
            width=1200)

desc3 = Div(text=open(join(dirname(__file__), 'description_questions.html')).read(),
            width=1200)

desc4 = Div(text=open(join(dirname(__file__), 'disclaimer.html')).read(),
            width=1200)

# Input Controls
parties_list = open(join(dirname(__file__), 'parties.txt')).read().split("\n")
parties_list.sort()

with open("parliament/short_parties_map.json", "r") as file:
    short_parties_map = json.load(file)

parameter_1 = Select(title="Parameter", options=sorted(axis_map_1.keys()), value="Attendance")

party_1 = Select(title="Party 1", value="None",
               options=parties_list)
party_2 = Select(title="Compare against Party 2", value="None",
               options=parties_list)

# party_score = party_scores[party.value][parameter.value]
average_score_1 = average_scores_1[parameter_1.value]
max_score_1 = max_scores_1[parameter_1.value]
min_score_1 = min_scores_1[parameter_1.value]

x_data_1 = ["Overall Average", "Overall Maximum", "Overall Minimum"]
y_data_1 = [average_score_1, max_score_1, min_score_1]
z_data_1 = ["Overall Average", max_party_1[parameter_1.value], min_party_1[parameter_1.value]]
members_1 = [""]*len(x_data_1)
palette_1 = ['#D24742', '#F57C15', '#FABF25']

source_1 = ColumnDataSource(data=dict(x_data_1=x_data_1, y_data_1=y_data_1, z_data_1=z_data_1,
                                      members_1=members_1))

p = figure(x_range=x_data_1, plot_height=350, toolbar_location=None, title="", active_drag=None, active_scroll=None)
p.vbar(x='x_data_1', top='y_data_1', width=0.5, source=source_1,
       line_color='white', fill_color=factor_cmap('x_data_1', palette=palette_1, factors=x_data_1, nan_color="#9E2963"))

p.xgrid.grid_line_color = None
p.tools.append(hover_1)


def update():
    party_1_name = party_1.value
    party_2_name = party_2.value
    parameter_name = parameter_1.value
    average_score = average_scores_1[parameter_1.value]
    max_score = max_scores_1[parameter_1.value]
    min_score = min_scores_1[parameter_1.value]
    if party_1_name == "None" and party_2_name == "None":
        p.yaxis.axis_label = parameter_name
        p.title.text = "Average %s per member in 16th Lok Sabha" % (parameter_1.value)
        p.title.align = 'center'

        p.x_range.factors = []
        p.x_range.factors = ["Overall Average", "Overall Maximum", "Overall Minimum"]

        source_1.data = dict(
            x_data_1=["Overall Average", "Overall Maximum", "Overall Minimum"],
            y_data_1=[average_score, max_score, min_score],
            z_data_1=["Overall Average", max_party_1[parameter_1.value], min_party_1[parameter_1.value]],
            members_1=[571, party_members[max_party_1_members[parameter_1.value]], party_members[min_party_1_members[parameter_1.value]]]
        )
    elif party_1_name != "None" and party_2_name == "None":
        party_1_score = party_scores[party_1_name][parameter_name]
        p.yaxis.axis_label = parameter_name
        p.title.text = "Average %s per member, of %s" % (parameter_1.value, short_parties_map[party_1_name])
        p.title.align = 'center'
        p.x_range.factors = []
        p.x_range.factors = [short_parties_map[party_1_name], "Overall Average", "Overall Maximum", "Overall Minimum"]

        source_1.data = dict(
            x_data_1=[short_parties_map[party_1_name],"Overall Average", "Overall Maximum", "Overall Minimum"],
            y_data_1=[party_1_score, average_score, max_score, min_score],
            z_data_1=[short_parties_map[party_1_name], "Overall Average", max_party_1[parameter_1.value], min_party_1[parameter_1.value]],
            members_1=[party_members[party_1_name], 571, party_members[max_party_1_members[parameter_1.value]], party_members[min_party_1_members[parameter_1.value]]]
        )

    elif party_1_name == "None" and party_2_name != "None":
        party_2_score = party_scores[party_2_name][parameter_name]
        p.yaxis.axis_label = parameter_name
        p.title.text = "Average %s per member, of %s" % (parameter_1.value, short_parties_map[party_2_name])
        p.title.align = 'center'

        p.x_range.factors = []
        p.x_range.factors = [short_parties_map[party_2_name], "Overall Average", "Overall Maximum", "Overall Minimum"]

        source_1.data = dict(
            x_data_1=[party_2_name, "Overall Average", "Overall Maximum", "Overall Minimum"],
            y_data_1=[party_2_score, average_score, max_score, min_score],
            z_data_1=[party_2_name, "Overall Average", max_party_1[parameter_1.value], min_party_1[parameter_1.value]],
            members_1=[party_members[party_2_name], 571, party_members[max_party_1_members[parameter_1.value]], party_members[min_party_1_members[parameter_1.value]]]
        )
    else:
        party_1_score = party_scores[party_1_name][parameter_name]
        party_2_score = party_scores[party_2_name][parameter_name]

        p.yaxis.axis_label = parameter_name
        p.title.text = "Comparison of Average %s per member, of %s & %s" % (parameter_name, short_parties_map[party_1_name], short_parties_map[party_2_name])
        p.title.align = 'center'

        p.x_range.factors = []
        p.x_range.factors = [short_parties_map[party_1_name], short_parties_map[party_2_name], "Overall Average", "Overall Maximum", "Overall Minimum"]

        source_1.data = dict(
            x_data_1=[short_parties_map[party_1_name], short_parties_map[party_2_name], "Overall Average", "Overall Maximum", "Overall Minimum"],
            y_data_1=[party_1_score, party_2_score, average_score, max_score, min_score],
            z_data_1=[short_parties_map[party_1_name], short_parties_map[party_2_name], "Overall Average", max_party_1[parameter_1.value], min_party_1[parameter_1.value]],
            members_1=[party_members[party_1_name], party_members[party_2_name], 571, party_members[max_party_1_members[parameter_1.value]], party_members[min_party_1_members[parameter_1.value]]]
        )


# Pie Chart ---------------------------------------------------------------------------------------------------

axis_map_2 = {
    "Have Information unavailable": "Have Information unavailable",
    "Have Others": "Have Others",
    "Went to college": "Went to college",
    "Have Advanced degree": "Have Advanced degree",
    "Studied till school": "Studied till school"
}

average_scores_2 = {
    "Have Information unavailable": 1.22,
    "Have Others": 0.7,
    "Went to college": 67.25,
    "Have Advanced degree": 12.43,
    "Studied till school": 18.38
}

max_scores_2 = {
    "Have Information unavailable": 3,
    "Have Others": 2,
    "Went to college": 185,
    "Have Advanced degree": 35,
    "Studied till school": 64,
}

min_scores_2 = {
    "Have Information unavailable": 0,
    "Have Others": 0,
    "Went to college": 0,
    "Have Advanced degree": 0,
    "Studied till school": 0}

max_party_2 = {
    "Have Information unavailable": "BJP",
    "Have Others": "BJP",
    "Went to college": "BJP",
    "Have Advanced degree": "BJP",
    "Studied till school": "BJP"
}

min_party_2 = {
    "Have Information unavailable": "NDPP",
    "Have Others": "RLD",
    "Went to college": "RLD",
    "Have Advanced degree": "PMK",
    "Studied till school": "TRS"
}


# Load Input Data
with open("parliament/party_education.json", "r") as file:
    party_education = json.load(file)

with open("parliament/party_education_percent.json", "r") as file:
    party_education_percent = json.load(file)


hover_2 = HoverTool()
hover_2.tooltips = [
    ("Party", "@z_data_2"),
    ("Total MPs of this party", "@members_2"),
    ("% who have this qualification", "@y_data_2")
]

# Input Controls
parties_list = open(join(dirname(__file__), 'parties.txt')).read().split("\n")
parties_list.sort()

parameter_2 = Select(title="Parameter", options=sorted(axis_map_2.keys()), value="Went to college")

party_3 = Select(title="Party 1", value="None",
               options=parties_list)
party_4 = Select(title="Compare against Party 2", value="None",
               options=parties_list)


# party_score = party_scores[party.value][parameter.value]
average_score_2 = average_scores_2[parameter_2.value]
max_score_2 = max_scores_2[parameter_2.value]
min_score_2 = min_scores_2[parameter_2.value]

x_data_2 = ["Overall Average"]
y_data_2 = [average_score_2]
z_data_2 = ["Overall Average"]
members_2 = [571]
palette_2 = ['#B2DD2C']

source_2 = ColumnDataSource(data=dict(x_data_2=x_data_2, y_data_2=y_data_2, z_data_2=z_data_2,
                                      members_2=members_2))

p2 = figure(x_range=x_data_2, plot_height=350, toolbar_location=None, title="", active_drag=None, active_scroll=None)
p2.vbar(x='x_data_2', top='y_data_2', width=0.2, source=source_2,
       line_color='white', fill_color=factor_cmap('x_data_2', palette=palette_2, factors=x_data_2, nan_color='#1E9C89'))


p2.xgrid.grid_line_color = None
p2.tools.append(hover_2)


def update_2():
    party_3_name = party_3.value
    party_4_name = party_4.value
    parameter_name = parameter_2.value
    average_score = average_scores_2[parameter_2.value]
    max_score = max_scores_2[parameter_2.value]
    min_score = min_scores_2[parameter_2.value]
    if party_3_name == "None" and party_4_name == "None":
        p2.yaxis.axis_label = parameter_name
        p2.title.text = "% of MPs who {}".format(parameter_name)
        p2.title.align = 'center'

        p2.x_range.factors = []
        p2.x_range.factors = ["Overall Average"]

        source_2.data = dict(
            x_data_2=["Overall Average"],
            y_data_2=[average_score],
            z_data_2=["Overall Average"],
            members_2=[571]
        )
    elif party_3_name != "None" and party_4_name == "None":
        party_3_score = party_education_percent[party_3_name][parameter_name]
        p2.yaxis.axis_label = parameter_name
        p2.title.text = "% of {} MPs who {}".format(short_parties_map[party_3_name], parameter_2.value)
        p2.title.align = 'center'
        p2.x_range.factors = []
        p2.x_range.factors = [short_parties_map[party_3_name], "Overall Average"]

        source_2.data = dict(
            x_data_2=[short_parties_map[party_3_name], "Overall Average"],
            y_data_2=[party_3_score, average_score],
            z_data_2=[short_parties_map[party_3_name], "Overall Average"],
            members_2=[party_members[party_3_name], 571]
        )

    elif party_3_name == "None" and party_4_name != "None":
        party_4_score = party_education_percent[party_4_name][parameter_name]
        p2.yaxis.axis_label = parameter_name
        p2.title.text = "% of {} MPs who {}".format(short_parties_map[party_4_name], parameter_2.value)
        p2.title.align = 'center'

        p2.x_range.factors = []
        p2.x_range.factors = [short_parties_map[party_4_name], "Overall Average"]

        source_2.data = dict(
            x_data_2=[short_parties_map[party_4_name], "Overall Average"],
            y_data_2=[party_4_score, average_score],
            z_data_2=[short_parties_map[party_4_name], "Overall Average"],
            members_2=[party_members[party_4_name], 571]
        )
    else:
        party_3_score = party_education_percent[party_3_name][parameter_name]
        party_4_score = party_education_percent[party_4_name][parameter_name]

        p2.yaxis.axis_label = parameter_name
        p2.title.text = "Compare % of {} & {} MPs who {}".format(short_parties_map[party_3_name], short_parties_map[party_4_name], parameter_name)
        p2.title.align = 'center'

        p2.x_range.factors = []
        p2.x_range.factors = [short_parties_map[party_3_name], short_parties_map[party_4_name], "Overall Average"]

        source_2.data = dict(
            x_data_2=[short_parties_map[party_3_name], short_parties_map[party_4_name], "Overall Average"],
            y_data_2=[party_3_score, party_4_score, average_score],
            z_data_2=[short_parties_map[party_3_name], short_parties_map[party_4_name], "Overall Average"],
            members_2=[party_members[party_3_name], party_members[party_4_name], 571]
        )

# Dot plot ---------------------------------------------------------------------------------------------------

# Load Input Data
with open("parliament/party_questions.json", "r") as file:
    questions_asked = json.load(file)

# Input Controls
parties_list = open(join(dirname(__file__), 'parties.txt')).read().split("\n")
parties_list.sort()
party3 = Select(title="Party", value="Bharatiya Janata Party",
               options=parties_list)

categories = questions_asked[party3.value]["categories"]
questions = questions_asked[party3.value]["questions"]
questions_percent = questions_asked[party3.value]["questions_percentage"]

source3 = ColumnDataSource(data=dict(questions=questions, categories=categories, questions_percent=questions_percent,
                                     parties_3=[short_parties_map["Bharatiya Janata Party"]]*len(questions),
                                     members_3=[party_members["Bharatiya Janata Party"]]*len(questions)))

hover_3 = HoverTool()

hover_3.tooltips = [
    ("Party", "@parties_3"),
    ("Total MPs of this party", "@members_3"),
    ("Questions Asked", "@questions")
]

p3 = figure(title="Percentage of questions asked in the Parliament by %s in various categories" % party3.value,
            toolbar_location=None, y_range=categories,
            x_range=[0, 20], x_axis_type=None, active_drag=None, active_scroll=None)

p3.segment(x0=0, y0="categories", x1="questions_percent", y1="categories", source=source3,
           line_width=10, line_color="#f7ad02")

p3.circle(x="questions_percent", y="categories", source=source3, size=15,
          fill_color="#ffffff", line_color="#f7ad02", line_width=4)

p3.yaxis.axis_label_text_font_size = "12pt"
p3.xaxis.axis_label_text_font_size = "12pt"
ticker = SingleIntervalTicker(interval=5, num_minor_ticks=5)
xaxis = LinearAxis(ticker=ticker)
p3.add_layout(xaxis, 'below')
ticker2 = SingleIntervalTicker(interval=5, num_minor_ticks=5)
xaxis2 = LinearAxis(ticker=ticker)
p3.add_layout(xaxis2, 'above')
p3.tools.append(hover_3)


def update_3():
    p3.title.text = "Percentage of questions asked in the Parliament by %s in various categories" % party3.value
    p3.title.align = 'center'
    p3.yaxis.axis_label = "Categories"

    categories = questions_asked[party3.value]["categories"][::-1]
    questions = questions_asked[party3.value]["questions"][::-1]
    questions_percent = questions_asked[party3.value]["questions_percentage"][::-1]

    p3.y_range.factors = []
    p3.y_range.factors = categories

    source3.data = dict(
        questions=questions,
        categories=categories,
        questions_percent=questions_percent,
        parties_3=[short_parties_map[party3.value]] * len(questions),
        members_3=[party_members[party3.value]] * len(questions)
    )


# Final -----------------------------------------------------------------------------------------------------
sizing_mode = 'scale_width'  # 'scale_width' also looks nice with this example

# Bar Chart
controls = [parameter_1, party_1, party_2]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, sizing_mode=sizing_mode)

# Pie Chart
controls_2 = [parameter_2, party_3, party_4]
for control in controls_2:
    control.on_change('value', lambda attr, old, new: update_2())

inputs2 = column(*controls_2, sizing_mode=sizing_mode)

# Dot Plot
controls_3 = [party3]
for control in controls_3:
    control.on_change('value', lambda attr, old, new: update_3())

inputs3 = column(*controls_3, sizing_mode="fixed")

l = layout([
    [desc],
    [inputs, p],
    [desc2],
    [inputs2, p2],
    [desc3],
    [inputs3],
    [p3],
    [desc4]], sizing_mode=sizing_mode)

update()  # initial load of the data
update_2()  # initial load of the data
update_3()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "UnFound Insights"


