from dabs_with_uv.config import Config, OutputSink, Table
from dabs_with_uv.aggregator import Aggregator


def test_aggregator():
    config = Config(
        limit=100,
        output_sink=OutputSink(
            orders_analytics=Table(
                catalog="main", db="default", name="orders_analytics"
            )
        ),
    )
    aggregator = Aggregator(config)
    aggregator.run()

    # check that the output table was created
    assert aggregator.spark.catalog.tableExists(
        config.output_sink.orders_analytics.full_name
    )
    # check that output table is not empty
    assert (
        aggregator.spark.table(config.output_sink.orders_analytics.full_name).count()
        > 0
    )
