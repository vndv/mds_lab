select 100+row_number() over() as geo_id,
country,
city, 
state, 
postal_code 
from (select distinct country, city, state, postal_code from {{ source('orders', 'orders') }} ) a