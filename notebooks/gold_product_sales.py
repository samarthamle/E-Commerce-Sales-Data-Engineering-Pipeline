from pyspark import pipelines as dp
from pyspark.sql.functions import col, sum, count, round, dense_rank
from pyspark.sql.window import Window

@dp.materialized_view(
    name="gold_product_sales",
    comment="Product-wise delivered sales and product performance"
)
def gold_product_sales():
    delivered_df = spark.read.table("gold_delivered_orders")

    # quantity and unit_price are stored as strings in gold_delivered_orders,
    # so cast before computing per-order revenue (quantity x unit_price).
    order_value = col("quantity").cast("decimal(18,2)") * col("unit_price").cast("decimal(18,2)")

    product_sales_df = (
        delivered_df
        .groupBy("product_name")
        .agg(
            count("*").alias("total_order_records"),
            sum(col("quantity").cast("bigint")).alias("total_units_sold"),
            round(sum(order_value), 2).alias("total_revenue"),
            round(sum(order_value) / count("*"), 2).alias("average_order_value"),
        )
    )

    # Rank products by true revenue, not order count.
    ranking_window = Window.orderBy(col("total_revenue").desc())

    return product_sales_df.select(
        "*",
        dense_rank().over(ranking_window).alias("revenue_rank")
    )