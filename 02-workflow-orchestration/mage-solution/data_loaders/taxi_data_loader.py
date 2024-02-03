import io
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/'
    file_base = 'green_tripdata_'
    files = [url + file_base + f'2020-{10 + i}.csv.gz' for i in range(3)]

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    df = pd.DataFrame()
    for _file in files:  # file seems to be reserved keyword
        print(_file)
        _df = pd.read_csv(_file, sep=",", compression="gzip", parse_dates=parse_dates)
        df = pd.concat([df, _df])


    return df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
