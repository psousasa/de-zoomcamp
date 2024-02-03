import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    df = df[df.passenger_count != 0]
    df = df[df.trip_distance != 0]

    df = df[~df.VendorID.isnull()]

    df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
    
    df.columns = (df.columns
                .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                .str.lower()
             )
    return df


@test
def test_output(output: pd.DataFrame, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    
    assert output[output['passenger_count'] == 0].empty
    
    assert None not in output.vendor_id.tolist()
    
    assert output['trip_distance'].sum() > 0
