from __future__ import annotations
import sys
from pydantic import BaseModel


class Table(BaseModel):
    catalog: str
    db: str
    name: str

    @property
    def full_name(self) -> str:
        return f"{self.catalog}.{self.db}.{self.name}"


class InputSource(BaseModel):
    orders: Table


class OutputSink(BaseModel):
    orders_analytics: Table


class Config(BaseModel):
    input_source: InputSource = InputSource(
        orders=Table(catalog="samples", db="tpch", name="orders")
    )
    output_sink: OutputSink = OutputSink(
        orders_analytics=Table(catalog="main", db="default", name="orders_analytics")
    )
    limit: int | None = None

    @staticmethod
    def from_args() -> Config:
        args = sys.argv[1:]

        if len(args) != 3:
            raise ValueError(
                "Supported arguments: <output_catalog> <output_db> <output_table>"
            )

        output_catalog, output_db, output_table = args[:3]

        return Config(
            output_sink=OutputSink(
                orders_analytics=Table(
                    catalog=output_catalog, db=output_db, name=output_table
                )
            )
        )
