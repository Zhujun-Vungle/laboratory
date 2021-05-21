## How to use 
- Setting environment variable 

```
export AWS_ACCESS_KEY_ID=${YOUR_AWS_KEY}
export AWS_SECRET_ACCESS_KEY=${YOUR_AWS_SECRET}
export RDS_METASTORE_USER=${YOUR_HIVE_METASTORE_DB_USER}
export RDS_METASTORE_PASS=${YOUR_HIVE_METASTORE_DB_PASS}

```

- Generate config files by running 

```
sh generate_blueprint.sh
```


You will have a file `emr_blueprint.json`, this is for EMR v6.0.0 configs.

## Blueprint components

- Spark 2.4.4 
- Hadoop 3.2.1
- Livy 0.6.0
