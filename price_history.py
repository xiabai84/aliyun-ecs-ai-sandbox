# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from tabulate import tabulate

from utils import Config, do_action, RegionIdSelect, ZonesSelect

import click

from aliyunsdkecs.request.v20140526 import DescribeSpotPriceHistoryRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeZonesRequest


@click.command()
@click.option('--merge', default=True)
def main(merge):
    config = Config()
    config.obtain_secret('access_key_id')
    config.obtain_secret('access_key_secret')

    client  = config.create_api_client('eu-central-1') # eu-central-1 frankfurt
    RegionIdSelect(config).show(config)
    ZonesSelect(config).show(config)
    client  = config.create_api_client()

    table = []
    request = DescribeSpotPriceHistoryRequest.DescribeSpotPriceHistoryRequest()
    request.set_ZoneId(config.get(['CreateInstanceParams', 'ZoneId']))
    request.set_NetworkType('vpc')
    instance_type = click.prompt('Enter instance type for querying price', type=str, default='ecs.gn5-c4g1.xlarge')
    request.set_InstanceType(instance_type)
    start_time = datetime.now() - timedelta(days=29)
    request.set_StartTime(start_time.strftime('%Y-%m-%dT00:00:00Z'))
    result = do_action(client, request)
    for idx, item in enumerate(result['SpotPrices']['SpotPriceType']):
        if merge and idx > 0:
            prev_item = result['SpotPrices']['SpotPriceType'][idx-1]
            if item['SpotPrice'] != prev_item['SpotPrice']:
                table.append((item['Timestamp'], item['SpotPrice']))
        else:
            table.append((item['Timestamp'], item['SpotPrice']))
    if not table:
        print('Can not find history price in this region')
    print(tabulate(table))


def get_zones(client):
    request = DescribeZonesRequest.DescribeZonesRequest()
    result = do_action(client, request)
    return result['Zones']['Zone']


if __name__ == "__main__":
    main()