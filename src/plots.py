import plotly.express as px

@staticmethod
def plot_line(df, x_axis : str, y_axis : list, **kwargs):
    """
    https://plotly.com/python/line-charts/
    """
    fig = px.line(df, x=x_axis, y=y_axis, **kwargs)
    return fig.show()
