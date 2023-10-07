select 100+row_number() over () as prod_id ,
product_id, 
product_name, 
category, 
subcategory as sub_category, 
segment 
from (select distinct product_id, product_name, category, subcategory, segment from {{ source('orders', 'orders') }} ) a