#!/usr/bin/env python
# coding: utf-8


import boto3
import logging
import pytz
import datetime

logging.basicConfig(
    format='%(levelname)s:%(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)

utc=pytz.UTC



session = boto3.session.Session(profile_name='s3-accidental-delete')
s3 = session.resource('s3')


# s3 = boto3.resource('s3')


# TODO: replace date and time accordingly
# datetime(year, month, day, hour, minute, second, microsecond, UTC-00:00)
point_of_restore = datetime.datetime(2022, 5, 6, 16, 0, 0, 0, pytz.UTC)



def revive_object(bucket, object_key):
    """
    Revives a versioned object that was deleted by removing the object's active
    delete marker.
    A versioned object presents as deleted when its latest version is a delete marker.
    By removing the delete marker, we make the previous version the latest version
    and the object then presents as *not* deleted.

    :param bucket: The bucket that contains the object.
    :param object_key: The object to revive.
    """
    # Get the latest version for the object.
    response = s3.meta.client.list_object_versions(
        Bucket=bucket.name, Prefix=object_key, MaxKeys=1)

    if 'DeleteMarkers' in response:
        latest_version = response['DeleteMarkers'][0]
        if latest_version['IsLatest']:
            logger.info("Object %s was deleted on %s. ", object_key, latest_version['LastModified'])

            last_modified = latest_version['LastModified']

            if point_of_restore < last_modified:
                logger.info("Object was deleted after point of restore. Activation will continue for object %s ",
                           object_key)
            
                obj = bucket.Object(object_key)
                obj.Version(latest_version['VersionId']).delete()
                logger.warning("Revived %s", object_key)
            else:
                logger.info("Object was deleted before point of restore. Activation will NOT continue for object %s ",
                           object_key)
        else:
            logger.info("Delete marker is not the latest version for %s!",
                           object_key)
    elif 'Versions' in response:
        logger.info("Got an active version for %s, nothing to do.", object_key)
    else:
        logger.error("Couldn't get any version info for %s.", object_key)
        

        
buckets = s3.meta.client.list_buckets()
        
for bucket in buckets['Buckets']:

    bucket_name = (f'{bucket["Name"]}')
    bucket = s3.Bucket(bucket_name)        
    
    logger.warning("Processing of bucket %s has started.", bucket_name)
	
    bucket_versioning = s3.meta.client.get_bucket_versioning(Bucket=bucket_name)

    if 'Status' in bucket_versioning:
    
    	is_trunckated = True
    	next_key_marker = ""
    	next_version_id_marker = ""
    	
    	while is_trunckated:
    		
    		if next_key_marker:
    		
    			all_objects = s3.meta.client.list_object_versions(Bucket=bucket.name, KeyMarker=next_key_marker, VersionIdMarker = next_version_id_marker)
    			
    		else:
    		
    			all_objects = s3.meta.client.list_object_versions(Bucket=bucket.name)
    			
    		all_versions = all_objects['Versions']
    		
    		for version in all_versions:
    			if not version['IsLatest']:
    				revive_object(bucket, version['Key'])
    				
    		is_trunckated = all_objects['IsTruncated']
    		if is_trunckated:
    			next_key_marker = all_objects['NextKeyMarker']
    			next_version_id_marker = all_objects['NextVersionIdMarker']
    			
    	logger.warning("Processing of bucket %s has been completed.", bucket_name)

    else:
    	logger.warning("Bucket %s does not have versioning enabled.", bucket_name)

