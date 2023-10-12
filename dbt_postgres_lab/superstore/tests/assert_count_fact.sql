select 
count(*) 
FROM {{ ref('stg_sales_fact') }} sf
inner join {{ ref('stg_shipping_dim') }} s on sf.ship_id=s.ship_id
inner join {{ ref('stg_geo_dim') }} g on sf.geo_id=g.geo_id
inner join {{ ref('stg_product_dim') }} p on sf.prod_id=p.prod_id
inner join {{ ref('stg_customer_dim') }} cd on sf.cust_id=cd.cust_id
HAVING not(count(*) = 9994)

