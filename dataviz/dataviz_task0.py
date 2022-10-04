import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import numpy as np

# Import database

stock_distribution = pd.read_sql("""
SELECT *
FROM stock
""",
                         conn)

stock_distribution['binary'] = np.where(stock_distribution['total_stock'] < 0, 0, 1)

fig = px.histogram(stock_distribution,
                   x="total_stock",
                   title = 'Stock log-distribution',
                   labels = {'total_stock':'number of stock'},
                   log_y = True,
                   color = 'binary',
                   color_discrete_sequence =['#fadd4d', '#8f00ff'],
                   nbins= 200)

fig.update_layout({'plot_bgcolor': '#313131',
                   'paper_bgcolor': '#313131'},
                  font=dict(color="#ffffff"),
                  bargap=0.1,
                  showlegend=False)

fig.update_yaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.show()
#%%
sales = pd.read_sql("""
SELECT *
FROM sales
""",
                         conn)

sales['revenue'] = sales['quantity'] * sales['sales_price_tax']

sales['sale_date'] = pd.to_datetime(sales['sale_date'])

sales = sales.groupby(sales.sale_date.dt.strftime('%W')) \
       .agg(quantity_sold=('quantity', 'sum'), cumul_revenues=('revenue', 'sum'), price_median = ('revenue', 'median')) \
       .reset_index()

fig = px.line(sales,
              title="Revenues",
              x="sale_date",
              y="cumul_revenues",
              log_y=True,
              color_discrete_sequence =['#fadd4d'])

fig2 = px.bar(sales,
              x="sale_date",
              y="quantity_sold",
              log_y=True,
              color_discrete_sequence =['#fadd4d'])

fig3 = px.line(sales,
               title = 'Median Price',
              x="sale_date",
              y="price_median",
              log_y=True,
              color_discrete_sequence =['#8f00ff'])

fig.add_trace(fig2.data[0])
fig.add_trace(fig3.data[0])

fig.update_layout({'plot_bgcolor': '#313131',
                   'paper_bgcolor': '#313131'},
                  title="Revenues, Median Price and Aggregated Quantities",
                  xaxis_title="Week",
                  yaxis_title="Quantities, Median Price, Revenues",
                  font=dict(color="#ffffff"))

fig.update_xaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.update_yaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.add_annotation(x=4, y=4,
            text="Median Price",
            showarrow=False,
            yshift=10,
                   font=dict(
            size=13,
            color="#fff"
            ))

fig.add_annotation(x=4, y=7,
            text="Revenues",
            showarrow=False,
            yshift=10,
                   font=dict(
            size=13,
            color="#fff"
            ))

fig.show()
#%%
sales = pd.read_sql("""
SELECT product_id, SUM(quantity)
FROM sales
GROUP BY product_id
ORDER BY quantity DESC
""",
                    conn)
print(sales.sort_values('SUM(quantity)', ascending= False).iloc[:10, 0].unique().tolist())

sales = pd.read_sql("""
SELECT *
FROM sales
WHERE product_id IN (112582, 110853, 157318, 125506, 107645, 136250, 132408 ,157317, 132284, 142254)
""",
                    conn)

sales['revenue'] = sales['quantity'] * sales['sales_price_tax']
sales['sale_date'] = pd.to_datetime(sales['sale_date'])

sales = sales.groupby([sales.sale_date.dt.strftime('%W'), 'product_id']) \
       .agg(quantity_sold=('quantity', 'sum'), cumul_revenues=('revenue', 'sum'), price_median = ('revenue', 'median')) \
       .reset_index()

sales['sale_date'] = sales['sale_date'].astype('int32')
sales = sales.sort_values('sale_date')


fig = px.line(sales,
                 x='sale_date',
                 y='cumul_revenues',
                 color = 'product_id',
                 log_y = True)

fig.update_layout({'plot_bgcolor': '#313131',
                   'paper_bgcolor': '#313131'},
                  title="Revenues of the 10 bestsellers",
                  xaxis_title="Week",
                  yaxis_title="Revenues",
                  font=dict(color="#ffffff"),
                  xaxis = dict(
                      tickmode = 'linear',
                      tick0 = 1,
                      dtick = 1)
                  )

fig.update_xaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.update_yaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.show()
#%%
sales = pd.read_sql("""
SELECT *
FROM sales
""",
                    conn)

sales['net'] = sales['quantity'] * sales['sales_price_tax'] - sales['quantity'] * sales['purchase_price']
sales['sale_date'] = pd.to_datetime(sales['sale_date'])
sales['binary'] = np.where(sales['net'] < 0, 0, 1)

fig = px.histogram(sales,
                   x="net",
                   title = 'Net profits log-distribution',
                   color = 'binary',
                   log_y = True,
                   color_discrete_sequence =['#fadd4d', '#8f00ff'],
                   nbins= 200)

fig.update_layout({'plot_bgcolor': '#313131',
                   'paper_bgcolor': '#313131'},
                  font=dict(color="#ffffff"),
                  bargap=0.1,
                  showlegend=False)

fig.update_yaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.show()
#%%
sales = pd.read_sql("""
SELECT COUNT(position), position
FROM regular
GROUP BY position
""",
                         conn)
higher_bound = ((sales['position'].mean() + 3*sales['position'].std()))
print('Higher bound is {}'.format(higher_bound))

lower_bound = ((sales['position'].mean() - 3*sales['position'].std()))
print('Lower bound is {}'.format(lower_bound))

sales['outlier'] = np.where((sales['position'] >= lower_bound) & (sales['position'] <= higher_bound), 0, 1)

fig = px.bar(sales,
             x="position",
             y='COUNT(position)',
             title = 'Stock log-distribution',
             labels = {'total_stock':'number of stock'},
             log_y = True,
             log_x = True,
             color = 'outlier',
             color_discrete_sequence =['#fadd4d', '#8f00ff'])

fig.update_layout({'plot_bgcolor': '#313131',
                   'paper_bgcolor': '#313131'},
                  font=dict(color="#ffffff"),
                  bargap=0.1,
                  showlegend=False)

fig.update_yaxes(showline=True,
                 linewidth=2,
                 linecolor='white',
                 gridcolor='rgba(255, 255, 255, 0.1)')

fig.show()
