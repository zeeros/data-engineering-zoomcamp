import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    return (
        data
        .rename(
            columns={
                'VendorID': 'vendor_id',
                'RatecodeID': 'rate_code_id',
                'PULocationID': 'pu_location_id',
                'DOLocationID': 'do_location_id'
            }
        )
        .loc[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
        .assign(lpep_pickup_date=lambda x: x['lpep_pickup_datetime'].dt.date)
    )

@test
def test_output(output, *args) -> None:
    assert 'vendor_id' in output.columns
    assert output.loc[output['passenger_count'] <= 0].shape[0] == 0
    assert output.loc[output['trip_distance'] <= 0].shape[0] == 0
