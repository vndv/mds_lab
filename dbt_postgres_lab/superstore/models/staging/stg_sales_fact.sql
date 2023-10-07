select
    cust_id,
    to_char(order_date, 'yyyymmdd')::int as order_date_id,
    to_char(ship_date, 'yyyymmdd')::int as ship_date_id,
    p.prod_id,
    s.ship_id,
    geo_id,
    o.order_id,
    sales,
    profit,
    quantity,
    discount,
    100 + row_number() over () as sales_id
from {{ source('orders', 'orders') }} as o
inner join {{ ref('stg_shipping_dim') }} as s on o.ship_mode = s.shipping_mode
inner join
    {{ ref('stg_geo_dim') }} as g
    on
        o.postal_code = g.postal_code
        and o.country = g.country
        and o.city = g.city
        and o.state = g.state
inner join
    {{ ref('stg_product_dim') }} as p
    on
        o.product_name = p.product_name
        and o.segment = p.segment
        and o.subcategory = p.sub_category
        and o.category = p.category
        and o.product_id = p.product_id
inner join
    {{ ref('stg_customer_dim') }} as cd
    on o.customer_id = cd.customer_id and o.customer_name = cd.customer_name
