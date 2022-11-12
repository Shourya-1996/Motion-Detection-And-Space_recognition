from bokeh.plotting import figure, output_file, show
from main import df
from bokeh.models import HoverTool, ColumnDataSource

p = figure(x_axis_type='datetime', height=100, width=500,
           title='Motion Graph')
p.yaxis.minor_tick_line_color = None

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

hover = HoverTool(
    tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

q = p.quad(left='Start', right='End', top=1,
           bottom=0, color='green', source=cds)

output_file('graph.html')
show(p)
