from pyspark import pipelines as dp
from pyspark.sql.functions import col, sum, count, round, dense_rank
from pyspark.sql.window import Window

@dp.materialized_view(
    name="gold_payment_analysis",
    comment="Payment mode analysis of delivered orders: revenue, order count, average transaction value"
)
def gold_payment_analysis():
    delivered_df = spark.read.table("gold_delivered_orders")

    # quantity and unit_price are stored as strings in gold_delivered_orders,
    # so cast before computing per-order revenue (quantity x unit_price).
    order_value = col("quantity").cast("decimal(18,2)") * col("unit_price").cast("decimal(18,2)")

    payment_analysis_df = (
        delivered_df
        .groupBy("payment_mode")
        .agg(
            count("*").alias("total_delivered_orders"),
            round(sum(order_value), 2).alias("total_revenue"),
            round(sum(order_value) / count("*"), 2).alias("average_transaction_value"),
        )
    )

    ranking_window = Window.orderBy(col("total_revenue").desc())

    return payment_analysis_df.select(
        "*",
        dense_rank().over(ranking_window).alias("revenue_rank")
    )
