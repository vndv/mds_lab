select
    ship_mode as shipping_mode,
    100 + row_number() over () as ship_id
from
    (select distinct ship_mode from {{ source('orders', 'orders') }}) as a
