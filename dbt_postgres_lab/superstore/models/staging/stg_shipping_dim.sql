select 100+row_number() over() as ship_id,
ship_mode as shipping_mode
from 
(select distinct ship_mode from {{ source('orders', 'orders') }} ) a