import sys
import os
import click
from app.models.dba.dba import dba


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@click.command()
@click.option("--schema", is_flag=False, help="Run only schema creation/update.")
@click.option("--data", is_flag=False, help="Run only data import.")
def cli(schema, data):
    dba(run_schema=schema, run_data=data)


if __name__ == "__main__":
    cli()
