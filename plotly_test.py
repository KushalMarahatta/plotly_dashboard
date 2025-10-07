import plotly.express as px

# Load sample dataset (comes with Plotly)
df = px.data.iris()

# Creating an interactive scatter plot
fig = px.scatter(df,
                 x='sepal_width',
                 y='sepal_length',
                 color='species',
                 size='petal_length',
                 title='Iris Scatter (Interactive)')

# Displaying the plot 
fig.write_image("iris_plot.png")
fig.show()