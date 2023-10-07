select 100+row_number() over() as cust_id,
customer_id, 
customer_name 
from (select distinct customer_id, customer_name from {{ source('orders', 'orders') }} ) a