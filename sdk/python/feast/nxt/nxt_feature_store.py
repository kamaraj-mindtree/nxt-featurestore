from datetime import datetime, timedelta
import datetime
from pyexpat import features
from unicodedata import name
import pandas as pd
from feast import FeatureStore 
import numpy as np
import random

from cmath import e
import os
import yaml
import sqlalchemy
from feast_postgres import PostgreSQLOfflineStoreConfig

import feast
from datetime import timedelta

from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Int64, Float32, Float64, UnixTimestamp, String, Bytes




def feast_function(parquet_path:str,entity_column:str,feature_views_name:str):
    """ Upload parquet into database """
    table_name = "nxt_" + str(os.path.basename(parquet_path).split('.')[0])
    # try:
    df = pd.read_parquet(parquet_path)
    list_column= df.columns
    data_type=df.dtypes
    size=len(list_column)
    # df.columns = [c.lower() for c in df.columns]
    ## upload parquet to DB
    with open("feature_store.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    offline_config = config["offline_store"]
    del offline_config["type"]
    offline_config = PostgreSQLOfflineStoreConfig(**offline_config)
    # print(offline_config)

    def get_sqlalchemy_engine(config: PostgreSQLOfflineStoreConfig):
        url = f"postgresql+psycopg2://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
        # print(url)
        # print(config.db_schema)
        return sqlalchemy.create_engine(url, client_encoding='utf8', connect_args={'options': '-c search_path={}'.format(config.db_schema)})

    con = get_sqlalchemy_engine(offline_config)
    
    df.to_sql(table_name, con,if_exists='append',index=False) 

    # table = table_name
    # con.execute("DROP TABLE IF EXISTS " + table)
    # create_table_sql = pd.io.sql.get_schema(df, table, con=con)
    # con.execute(create_table_sql)
    # buffer = StringIO()
    # df.to_csv(buffer, header=False, index=False, na_rep="\\N")
    # buffer.seek(0)
    # raw_con = con.raw_connection()
    # with raw_con.cursor() as cursor:
    #     cursor.copy_from(buffer, table, sep=",")
    # raw_con.commit()
    # return{"Message":"Data added successfully"}
    

    # except FileNotFoundError:
    #     # print("File not found")
    #     return{"Mesage":"File or path not found"}
    # except pandas.errors.EmptyDataError:
    #     # print("file is empty")
    #     return{"Mesage":"File Is Empty"}
    # except yaml.YAMLError as exc:
    #         # print(exc)
    #     return{"Message":e}
    
    ## Timestamp Creation
    stime= "20-01-2018 13:30:00"
    etime="23-01-2018 04:50:34"
    n=len(df)

    def randomtimes(start, end, n):
            """TimeStamp Creation"""
            frmt = '%d-%m-%Y %H:%M:%S'
            stime = datetime.datetime.strptime(start, frmt)
            etime = datetime.datetime.strptime(end, frmt)
            td = etime - stime
            return [random.random() * td + stime for _ in range(n)]
        
    def current_datetime():
        """Created column Creation"""
        for i in range(n):
            return[datetime.datetime.now() for _ in range(n)]

    result_current = current_datetime()
    # print(result_current)

    random_result = randomtimes(stime, etime, n)
    # print(random_result[0])

    # Creating Random_id
    data = np.random.randint(1,5,size=len(df))
    # df['random_entity_id'] = data
    # print(data)


    if 'event_timestamp' not in df.columns:
        df['event_timestamp'] = random_result
        df.to_parquet(parquet_path)
        print("event_timestamp added")
    else:
        pass
        
    if "created" not in df.columns:
        df['created'] = result_current
        df.to_parquet(parquet_path)
        print("created added")
    else:
        pass


    if "random_entity_id" not in df.columns:
        df['random_entity_id'] = data
        df.to_parquet(parquet_path)
        print("random_id added")
    else:
        pass
        
    
    def schema_views():
        list=[]
        dict1={
            
            'float32':Float32,
            'float64' : Float64,
            'int64' : Int64,
            'datetime64[ns]' : UnixTimestamp,
            'string' : String,
            'bytes' : Bytes,
            'object' : String
            # "int": ValueType.INT64,
            # "str": ValueType.STRING,
            # "string": ValueType.STRING,  # pandas.StringDtype
            # "float": ValueType.DOUBLE,
            # "bytes": ValueType.BYTES,
            # "float64": ValueType.DOUBLE,
            # "float32": ValueType.FLOAT,
            # "int64": ValueType.INT64,
            # "uint64": ValueType.INT64,
            # "int32": ValueType.INT32,
            # "uint32": ValueType.INT32,
            # "int16": ValueType.INT32,
            # "uint16": ValueType.INT32,
            # "uint8": ValueType.INT32,
            # "int8": ValueType.INT32,
            # "bool": ValueType.BOOL,
            # "timedelta": ValueType.UNIX_TIMESTAMP,
            # "timestamp": ValueType.UNIX_TIMESTAMP,
            # "datetime": ValueType.UNIX_TIMESTAMP,
            # "datetime64[ns]": ValueType.UNIX_TIMESTAMP,
            # "datetime64[ns, tz]": ValueType.UNIX_TIMESTAMP,
            # "category": ValueType.STRING,
        }
        for i in range (size):
            if list_column[i] == 'random_entity_id':
               continue
            if list_column[i] == 'event_timestamp':
                continue
            if list_column[i] == 'created':
                 continue
            else:
                ob = Field(name=list_column[i], dtype=dict1[str(data_type[i])])
                list.append(ob)
            
        return list
    
    feature_schema = schema_views()
    
    random_id = Entity(name=entity_column,value_type=ValueType.INT64 ,join_keys=[entity_column],)


    sample_source = PostgreSQLSource(
        name=table_name,
        query=f"SELECT * FROM {table_name}".format(table_name),
        timestamp_field="event_timestamp",
        created_timestamp_column="created",
    )

    # sample_source=FileSource(
    #     path=parquet_path,
    #     timestamp_field="event_timestamp",
    #     created_timestamp_column="created",
    # )

    sample_fv = FeatureView(
        name=feature_views_name,
        entities=[random_id],
        ttl=timedelta(weeks=52),
        # schema=[
        #     Field(name="AT", dtype=Float64),
        #     Field(name="AP", dtype=Float64),
        #     Field(name="AH", dtype=Float64),
        #     Field(name="AFDP", dtype=Float64),
        #     Field(name="GTEP", dtype=Float64),
        #     Field(name="TIT", dtype=Float64),
        #     Field(name="TAT", dtype=Float64),
        #     Field(name="CDP", dtype=Float64),
        #     Field(name="CO", dtype=Float64),
        #     Field(name="NOX", dtype=Float64),
        #     Field(name="TEY", dtype=Float64),
        # ],
        schema = feature_schema,
        source = sample_source,
    )

    
    
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    
    # start= '20-01-2018 13:30:00'  
    # time1= datetime.time(3,45,12) 
    # end= '23-01-2018 04:50:34'
    start_date=datetime.datetime(2018,1,20,13,30,20)
    end_date=datetime.datetime(2018,1,23,4,50,34)

    # Load the feature store from the current path
    fs = FeatureStore(repo_path=".")

    print("Deploying feature store to Postgres...")
    # return{"Message":"Deploying feature store to Postgres..."}
    fs.apply([random_id, sample_fv])
    # fs.apply()

    # Select features
    list_1=[]
    for i in range (size):
        if list_column[i] == 'random_entity_id':
            continue
        if list_column[i] == 'event_timestamp':
            continue
        if list_column[i] == 'created':
            continue
        else:
                ab1=f"{sample_fv.name}:{list_column[i]}".format(sample_fv.name,list_column)
                list_1.append(ab1)
        # print(list_1)
    features = list_1
    # features = ["sample_feature_views:AT", "sample_feature_views:AP","sample_feature_views:AH",
    #             "sample_feature_views:AFDP","sample_feature_views:GTEP","sample_feature_views:TIT",
    #             "sample_feature_views:CDP","sample_feature_views:CO","sample_feature_views:NOX",
    #             "sample_feature_views:TEY"]

    # Create an entity dataframe. This is the dataframe that will be enriched with historical features
    entity_df = pd.DataFrame(
        {
            "event_timestamp": [
                pd.Timestamp(dt, unit="ms", tz="UTC").round("ms")
                for dt in pd.date_range(
                    start='20-01-2018 13:30:00',
                    end='23-01-2018 04:50:34',
                    periods=5,
                )
            ],
            random_id.name: [3, 4,1,2,0],
        }
    )

    print("Retrieving training data...")

    training_df = fs.get_historical_features(
        features=features, entity_df=entity_df
    ).to_df()

    print()
    print(training_df)

    print()
    print("Loading features into the online store...")
    # fs.materialize_incremental(end_date=datetime.now())
    fs.materialize(start_date,end_date)
    

    print()
    print("Retrieving online features...")

    # Retrieve features from the online store
    online_features = fs.get_online_features(
        features=features, entity_rows=[{random_id.name: 2}, {random_id.name: 3},{random_id.name: 4},{random_id.name: 1},{random_id.name: 0}],
    ).to_dict()

    print()
    print(pd.DataFrame.from_dict(online_features))