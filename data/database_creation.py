import sqlite3
import pandas as pd

regular = pd.read_csv('dataset/clicks_regular_all.csv')
bidding = pd.read_csv('dataset/clicks_bidding_all.csv')
concatenato = pd.concat([regular, bidding], axis = 0).to_csv('dataset/clicks_concatenato.csv')

# Crea o sovrascrivi un database e connettiti
conn= sqlite3.connect("database.db")

# Tutti i file devono avere questi nomi ed essere inseriti nella stessa cartella di questo script
files = {'bidding':'dataset/clicks_bidding_all.csv',
         'regular': 'dataset/clicks_regular_all.csv',
         'prices': 'dataset/prices_competitor_all.csv',
         'catalog': 'dataset/product_catalog_all.csv',
         'sales': 'dataset/sales_data_all.csv',
         'sellers': 'dataset/sellers_list_all.csv',
         'stock': 'dataset/stock_all.csv',
         'concatenato': 'dataset/clicks_concatenato.csv'}

# Aggiungi i .csv al database
for file in files:
  data = pd.read_csv(files[file])
  data.to_sql(file, conn, if_exists='replace')

# Query di modifica sul database
conn.execute("DELETE FROM concatenato WHERE position = 0.0 AND type = 'Regular'")
conn.execute("UPDATE concatenato SET type = 0 WHERE type = 'Regular'")
conn.execute("UPDATE concatenato SET type = 1 WHERE type = 'Bidding'")
conn.execute("UPDATE concatenato SET position = position + 3 WHERE type = 'Regular'")
