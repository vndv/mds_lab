select
    region,
    country,
    city,
    state,
    postal_code,
    100 + row_number() over () as geo_id
from
    (select distinct
        region,
        country,
        city,
        state,
        postal_code
    from {{ source('orders', 'orders') }}) as a
