from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
import os
import pyarrow as pa
import pyarrow.parquet as pq


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pedro/Documents/Learning/hybrid-saga-412112-990e2f2af52a.json'

bucket_name = '02-data-orchestration'
project_id = 'hybrid-saga-412112'

table_name = 'taxi_data'
root_path = f'{bucket_name}\{table_name}'


@data_exporter
def export_data_to_gcs(df: DataFrame, **kwargs) -> None:
    """
    Export partitioned parquets into GCS bucket.
    """

    table = pa.Table.from_pandas(df)

    gcs_fs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table, 
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs_fs)
