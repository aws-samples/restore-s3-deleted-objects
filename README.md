[Restore accidentally deleted files from Amazon S3](#1---English-Version)
[Restaure arquivos acidentalmente apagados do Amazon S3](#2---Portuguese-Version)


## Restore accidentally deleted files from Amazon S3

### When should you use this script?

These scripts were developed to help users restore files that have been accidentally deleted from Amazon S3. 

- Restore files from all buckets:

    [This script](https://github.com/aws-samples/restore-s3-deleted-objects/blob/main/revive_s3_objects_from_all_buckets.py) iterates through all of the files in all of the buckets in an AWS account. If the files have been deleted after a specific point in time (*point_of_restore*), then the script restores the files to their latest state.

- Restore files from one specific bucket:

    [This script](https://github.com/aws-samples/restore-s3-deleted-objects/blob/main/revive_s3_objects_from_1_bucket.py) iterates through all of the files in a specific bucket in an AWS account. If the files have been deleted after a specific point in time (*point_of_restore*), then the script restores the files to their latest state.
---
### Pre-requirements
1) **Attention!** In order for this script to work, [versioning ](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html) must have been enabled in the Amazon S3 bucket **before** the files were deleted.
1) Edit the chosen script to set the *point_of_restore* variable. This should represent the date and time of the incident. Make sure to round down, so we don't miss any files.
1) If you chose the script that restores from one specific bucket, set the name of the bucket (*bucket_name*) as well
1) If you need a list of all of the objects restored, set *list_all_restored_objects* to True
1) If you feel more comfortable running Jupyter Notebooks, a .ipynb file has also been provided.

---
### How to run this script
In order for you to run this Python 3 script, you will need a User with the permissions described in [this IAM policy](https://github.com/aws-samples/restore-s3-deleted-objects/blob/main/policy-s3-restore-deleted-objects.json).

There are a few options to run this script. We describe two possibilities below. Choose the one that best fits your needs:

##### 1) If you have access to the AWS console
a. Access [AWS Cloud Shell](https://console.aws.amazon.com/cloudshell/home)
    
For more information on AWS Cloud Shell: https://aws.amazon.com/cloudshell/
    
b. Clone this GitHub repository

    git clone https://github.com/aws-samples/restore-s3-deleted-objects


c Execute the desired script. Example:

    cd restore-s3-deleted-objects/
    python3 revive_s3_objects_from_all_buckets.py 

d. Logs will show up as the script runs

##### 2) If you have access key and secret key credentials:
a.  If you have AWS CLI configured, you may skip this. Otherwise, [configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in a command line tool/terminal. 

b.  Clone this GitHub repository

    git clone https://github.com/aws-samples/restore-s3-deleted-objects

c. Execute the desired script. Example:
   
    cd restore-s3-deleted-objects/
    python3 revive_s3_objects_from_all_buckets.py
d. Logs will show up as the script runs

---
### Costs

This script executes requests made against Amazon S3 buckets and files, like GET, LIST, and PUT. Costs will vary depending on how many objects and buckets a customer is restoring. For more details on Amazon S3 pricing, take a look at [Amazon S3 pricing page](https://aws.amazon.com/s3/pricing/)


---
## Restaure arquivos acidentalmente apagados do Amazon S3

TBD

---
### Disclaimer

This script is for information purposes only and should not be used for production workloads. 

---
## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

