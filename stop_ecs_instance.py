# -*- coding: utf-8 -*-
import time

from utils import Config, do_action, wait_for_instance_status

import click
from aliyunsdkecs.request.v20140526 import (DeleteInstanceRequest,
                                            DeleteSnapshotRequest,
                                            DeleteDiskRequest,
                                            CreateSnapshotRequest,
                                            StopInstanceRequest)


def main():
    config = Config()
    config.obtain_secret('access_key_id')
    config.obtain_secret('access_key_secret')
    config.load()

    stop_instance(config)
    wait_for_instance_status(config, "Stopped")
    delete_instance(config)
    answer = click.prompt("do you want to make a snapshot, then delete disk for reducing cost? [y/n]")
    if answer == 'y':
        OldSnapshotId = config.get('SnapshotId')
        time.sleep(20)
        create_snapshot(config)
        time.sleep(20)
        delete_disk(config)
        if OldSnapshotId:
            delete_snapshot(config, OldSnapshotId)

    cleanup(config)


def stop_instance(config):
    click.echo(click.style("stoping instance ...", fg="green"))
    client = config.create_api_client()
    req = StopInstanceRequest.StopInstanceRequest()
    req.set_InstanceId(config.get('InstanceId'))
    result = do_action(client, req)


def delete_instance(config):
    click.echo(click.style("deleting instance ...", fg="green"))
    client = config.create_api_client()
    req = DeleteInstanceRequest.DeleteInstanceRequest()
    req.set_InstanceId(config.get('InstanceId'))
    result = do_action(client, req)

def create_snapshot(config):
    client = config.create_api_client()
    request = CreateSnapshotRequest.CreateSnapshotRequest()
    request.set_DiskId(config.get('DiskId'))
    result = do_action(client, request)
    SnapshotId= result['SnapshotId']
    config.set('SnapshotId', SnapshotId)

def delete_snapshot(config, snapshot_id):
    client = config.create_api_client()
    request = DeleteSnapshotRequest.DeleteSnapshotRequest()
    request.set_SnapshotId(snapshot_id)
    do_action(client, request)

def delete_disk(config):
    client = config.create_api_client()
    request = DeleteDiskRequest.DeleteDiskRequest()
    request.set_DiskId(config.get('DiskId'))
    do_action(client, request)
    config.pop("DiskId")




def cleanup(config):
    click.echo(click.style("updating config file ...", fg="green"))
    config.pop("InstanceId")
    config.save()

if __name__ == '__main__':
    main()
