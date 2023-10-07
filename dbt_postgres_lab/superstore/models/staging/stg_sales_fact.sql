select
	 100+row_number() over() as sales_id
	 ,cust_id
	 ,to_char(order_date,'yyyymmdd')::int as  order_date_id
	 ,to_char(ship_date,'yyyymmdd')::int as  ship_date_id
	 ,p.prod_id
	 ,s.ship_id
	 ,geo_id
	 ,o.order_id
	 ,sales
	 ,profit
     ,quantity
	 ,discount
from {{ source('orders', 'orders') }} o 
inner join {{ ref('stg_shipping_dim') }} s on o.ship_mode = s.shipping_mode
inner join {{ ref('stg_geo_dim') }} g on o.postal_code = g.postal_code and g.country=o.country and g.city = o.city and o.state = g.state 
inner join {{ ref('stg_product_dim') }} p on o.product_name = p.product_name and o.segment=p.segment and o.subcategory=p.sub_category and o.category=p.category and o.product_id=p.product_id 
inner join {{ ref('stg_customer_dim')}} cd on cd.customer_id=o.customer_id and cd.customer_name=o.customer_name 