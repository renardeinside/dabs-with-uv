from pyspark.sql import SparkSession
from dabs_with_uv.config import Config
from dabs_with_uv.logger import logger


class Aggregator:

    def __init__(self, config: Config):
        self.config = config
        self.spark = SparkSession.builder.getOrCreate()

    def _prepare_catalog(self):
        self.spark.sql(
            f"CREATE CATALOG IF NOT EXISTS {self.config.output_sink.orders_analytics.catalog}"
        )
        self.spark.sql(
            f"CREATE SCHEMA IF NOT EXISTS {self.config.output_sink.orders_analytics.catalog}.{self.config.output_sink.orders_analytics.db}"
        )

    def run(self):
        logger.info("Preparing aggregated orders table")
        self._prepare_catalog()

        orders_source = self.spark.table(self.config.input_source.orders.full_name)

        # limit if provided in the config
        orders = (
            orders_source
            if not self.config.limit
            else orders_source.limit(self.config.limit)
        )

        # Aggregating orders by o_custkey
        orders_aggregated = orders.groupBy("o_custkey").agg(
            {"o_totalprice": "sum", "o_orderkey": "count"}
        )
        orders_aggregated = orders_aggregated.withColumnRenamed(
            "sum(o_totalprice)", "total_price"
        )
        orders_aggregated = orders_aggregated.withColumnRenamed(
            "count(o_orderkey)", "order_count"
        )

        # Writing aggregated orders to the output sink
        orders_aggregated.write.saveAsTable(
            self.config.output_sink.orders_analytics.full_name,
            mode="overwrite",
        )

        logger.info("Aggregated orders table created")


def entrypoint():
    config = Config.from_args()
    aggregator = Aggregator(config)
    aggregator.run()
