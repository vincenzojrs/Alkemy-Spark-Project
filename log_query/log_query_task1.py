# !!!!!!TO BE DONE!!!!!!; DELETE THIS COMMENT WHEN DONE AND UPDATE THE QUERY BELOW
# FILTERING FOR OBSERVATION IN 2021...AND DO WE NEED SOME OTHER FILTERS? CAN'T REMEMBER
# PLEASE ADD ALSO A .TO_CSV TO OUTPUT THE FINAL CSV AND UPLOAD TO "data" FOLDER "final_csv_task1.csv"

query = pd.read_sql("""
WITH d AS (
  SELECT comp_date, product_id, MIN(price) AS min, MAX(price) AS max
  FROM prices
   GROUP BY comp_date, product_id
), 
c AS (
  SELECT DATE(date) as date, type, position, seller, product_id
  FROM concatenato
)

SELECT p.comp_date, p.product_id, p.seller_id, d.min, p.price, d.max, c.type, c.position
FROM prices as p
LEFT JOIN d ON p.comp_date = d.comp_date AND p.product_id = d.product_id
LEFT JOIN c ON p.comp_date = c.date AND p.seller_id = c.seller AND p.product_id = c.product_id
""",
                    conn)
print(query)

# Ragioni per non tenere colonne concatenato

# SELECT * FROM CONCAT WHERE DATE(date) = '2021-07-07' AND product_id = '128776' AND seller = 23
# >>> Vuoto

print(query.type.value_counts())
print(query.position.value_counts())

# Verifica consistency prezzi

query['difference'] = np.where((query['max'] - query['min'] >= 0), 1, 0)
print(query['difference'].value_counts())

query['difference'] = np.where((query['price'] <= query['max']) & (query['price'] >= query['min']), 1, 0)
print(query['difference'].value_counts())
