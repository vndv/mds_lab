 SELECT 
    g.region, COUNT(distinct s.ship_id) AS no_of_shipments, SUM(m.profit) AS profit_in_each_region
	FROM
    {{ ref('stg_sales_fact') }} m
	INNER JOIN
    {{ ref('stg_customer_dim') }} c ON m.cust_id = c.cust_id
	INNER JOIN
    {{ ref('stg_shipping_dim') }} s ON m.ship_id = s.ship_id
	INNER JOIN
    {{ ref('stg_product_dim') }} p ON m.prod_id = p.prod_id
    inner join {{ ref('stg_geo_dim') }} g on  m.geo_id = g.geo_id
	WHERE
    p.sub_category IN (	SELECT 	p.sub_category FROM {{ ref('stg_sales_fact') }} m INNER JOIN {{ ref('stg_product_dim') }} p ON m.prod_id = p.prod_id GROUP BY p.sub_category HAVING SUM(m.profit) <= ALL
	(	SELECT 
		SUM(m.profit) AS profits
		FROM
		{{ ref('stg_sales_fact') }} m
		INNER JOIN
		{{ ref('stg_product_dim') }} p ON m.prod_id = p.prod_id
		GROUP BY p.sub_category
	)
	)
	GROUP BY g.region
	ORDER BY profit_in_each_region DESC