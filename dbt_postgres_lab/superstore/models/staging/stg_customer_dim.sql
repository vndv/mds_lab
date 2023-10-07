select
    customer_id,
    customer_name,
    100 + row_number() over () as cust_id
from
    (select distinct
        customer_id,
        customer_name
    from {{ source('orders', 'orders') }}) as a
