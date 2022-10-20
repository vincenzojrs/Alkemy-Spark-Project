# Run first the code to create the database, available in data/database_creation.py. Use that file, which is the most updated

query = pd.read_sql("""
WITH d AS (
  SELECT comp_date, product_id, MIN(price) AS min, MAX(price) AS max
  FROM prices
  GROUP BY comp_date, product_id
)

SELECT p.comp_date, p.product_id, p.seller_id, d.min, p.price, d.max
FROM prices as p
LEFT JOIN d ON p.comp_date = d.comp_date AND p.product_id = d.product_id
""",
                         conn)

# Ragioni per non tenere colonne concatenato
# SELECT * FROM CONCAT WHERE DATE(date) = '2021-07-07' AND product_id = '128776' AND seller = 23
# >>> Vuoto
# print(query.type.value_counts())
# print(query.position.value_counts())

# Verifica consistency prezzi

query['difference'] = np.where((query['max'] - query['min'] >= 0), 1, 0)
print(query['difference'].value_counts())

query['difference'] = np.where((query['price'] <= query['max']) & (query['price'] >= query['min']), 1, 0)
print(query['difference'].value_counts())

query.drop(columns=['difference'], inplace = True)

query.head()

query.to_csv('final_csv_task1.csv')
