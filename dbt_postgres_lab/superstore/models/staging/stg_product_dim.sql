select
    product_id,
    product_name,
    category,
    subcategory as sub_category,
    segment,
    100 + row_number() over () as prod_id
from
    (select distinct
        product_id,
        product_name,
        category,
        subcategory,
        segment
    from {{ source('orders', 'orders') }}) as a
