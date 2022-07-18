# Importing dependencies
from feast import FeatureStore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import pandas as pd
import os
from typing import List

import datetime
from cmath import e
# from io import StringIO
import os
# import re
# import pandas
import os.path
from os import path
# import sqlite3
import yaml
import sqlalchemy
from feast_postgres import PostgreSQLOfflineStoreConfig
# from sqlalchemy import inspect
# from feast.feature_view import Field
import random
import numpy as np
import feast
from datetime import timedelta, datetime

# from feast import Entity, FeatureView,  ValueType
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource
from feast import Entity, FeatureView, Field, FileSource, ValueType, FeatureService
from feast.types import Int64, Float32, Float64, UnixTimestamp, String, Bytes,Int32

# Instantiating the API
app = FastAPI()



### DATA MODELS FOR REQUEST BODIES ###


# Data model for creating entity DataFrames
class EntityDF(BaseModel):
    entity_keys: List[int]
    entity_name: str
    feature_view_names: List[str]
    start_date:str
    end_date:str 
 




### API ENDPOINTS ###

# Endpoint for cloning the GitHub repo with a feature repository
app.store=FeatureStore(repo_path=".")

# Endpoint for getting the cloned feature store
def feast_function(parquet_path:str,entity_column:str,feature_views_name:str,feature_service_name:str):
    """ Upload parquet into database """
    table_name = "nxt_" + str(os.path.basename(parquet_path).split('.')[0])
    # try:
    df = pd.read_parquet(parquet_path)
    # global list_column 
    list_column = df.columns
    data_type=df.dtypes
    size=len(list_column)
    app.size = size
    app.list_column = list_column
    # df.columns = [c.lower() for c in df.columns]
     ## Timestamp Creation
    stime= datetime.now()
    etime=stime- timedelta(days=2)
    n=len(df)

    def randomtimes(start, end, n):
            """TimeStamp Creation"""
            frmt = '%d-%m-%Y %H:%M:%S'
            # stime = datetime.datetime.strptime(start, frmt)
            # etime = datetime.datetime.strptime(end, frmt)
            td = etime - stime
            return [random.random() * td + stime for _ in range(n)]
        
    def current_datetime():
        """Created column Creation"""
        for i in range(n):
            return[datetime.now() for _ in range(n)]

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

    if entity_column not in df.columns:
        df[entity_column] = data
        df.to_parquet(parquet_path)
        print("random_id added")
    else:
        pass
        
    
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
    
    df.to_sql(table_name, con,if_exists='replace',index=False) 

    ## Timestamp Creation
    # stime= datetime.now()
    # etime=stime- timedelta(days=2)
    # n=len(df)

    # def randomtimes(start, end, n):
    #         """TimeStamp Creation"""
    #         frmt = '%d-%m-%Y %H:%M:%S'
    #         # stime = datetime.datetime.strptime(start, frmt)
    #         # etime = datetime.datetime.strptime(end, frmt)
    #         td = etime - stime
    #         return [random.random() * td + stime for _ in range(n)]
        
    # def current_datetime():
    #     """Created column Creation"""
    #     for i in range(n):
    #         return[datetime.now() for _ in range(n)]

    # result_current = current_datetime()
    # # print(result_current)

    # random_result = randomtimes(stime, etime, n)
    # # print(random_result[0])

    # # Creating Random_id
    # data = np.random.randint(1,5,size=len(df))
    # # df['random_entity_id'] = data
    # # print(data)


    # if 'event_timestamp' not in df.columns:
    #     df['event_timestamp'] = random_result
    #     df.to_parquet(parquet_path)
    #     print("event_timestamp added")
    # else:
    #     pass

    # if entity_column not in df.columns:
    #     df[entity_column] = data
    #     df.to_parquet(parquet_path)
    #     print("random_id added")
    # else:
    #     pass
        
    
    def schema_views():
        list=[]
        dict1={
            
            'float32':Float32,
            'float64' : Float64,
            'int64' : Int64,
            'datetime64[ns]' : UnixTimestamp,
            'string' : String,
            'bytes' : Bytes,
            'object' : String,
            'int32' : Int32
        }
        for i in range (size):
            if list_column[i] == entity_column:
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
    sample_fv = FeatureView(
        name=feature_views_name,
        entities=[random_id],
        ttl=timedelta(weeks=52),
        schema = feature_schema,
        source = sample_source,
    )
    app.sample_fv= sample_fv
    sample_sv=FeatureService(
        name=feature_service_name,
    features=[sample_fv]
    )

    app.store.apply([random_id, sample_fv,sample_sv])
    # fs.apply()
    return{'status':True,"Message":"Deploying feature store to Postgres..."}
    # return(size,list_column)

# Endpoint for getting feature views
@app.get("/get_feature_views")
def get_feature_views():
    # Getting feature views
    feature_views = app.store.list_feature_views()

    # Initializing a list for feature view names
    feature_view_names = []

    # Iterating over the feature views
    for feature_view in feature_views:
        # Adding each feature view name
        # to the list we created earlier
        feature_view_names.append(feature_view.name)

    # Returning the feature view names
    return {"feature_view_names": feature_view_names}


# Endpoint for getting feature names
@app.get("/get_feature_names")
def get_feature_names(feature_view_name: str):
    # Initializing a list for feature names
    feature_names = []

    # Iterating over the features under the given feature view
    # and appending their names to our list
    for feature in app.store.get_feature_view(name=feature_view_name).features:
        feature_names.append(feature.name)

    # Returning the features
    return {"feature_names": feature_names}


# Endpoint for getting entities
@app.get("/get_entities")
def get_entities():
    # Fetching entities
    entities = app.store.list_entities()

    # Initializing lists for entity names and descriptions
    entity_names = []
    entity_descriptions = []

    # Iterating over entities
    for entity in entities:
        # Appending entity names and descriptions
        # to the lists created earlier
        entity_names.append(entity.name)
        entity_descriptions.append(entity.description)

    # Returning entity names and their descriptions
    return {"entity_names": entity_names, "entity_descriptions": entity_descriptions}


# Endpoint for registering entity DataFrames
def register_entity_df(entity_keys:List[int],entity_name: str,feature_view_names: List[str],start_date:str,end_date:str ):
    # Generating timestamps based on provided params
    # and converting them to a DataFrame
    timestamps = pd.date_range(
        start=start_date,
        end=end_date,
        # freq=entity_df_params.frequency,
    ).to_frame(index=False, name="event_timestamp")

    # Creating a DataFrame with entity keys
    entity_ids = pd.DataFrame(
        data=entity_keys, columns=[entity_name]
    )

    # Merging the timestamps and entity key DataFrame
    entity_df = timestamps.merge(right=entity_ids, how="cross")

    # Saving the entity DataFrame to the app
    app.entity_df = entity_df
    features_to_get = []

    # Iterating over requested feature view names
    # and generating feature names in
    # the feature_view_name:feature_name format
    for feature_view in feature_view_names:
        for feature in app.store.get_feature_view(name=feature_view).features:
            features_to_get.append(feature_view + ":" + feature.name)
    print(app.entity_df)
    # Retrieving requested features from the feature store
    app.store.get_historical_features(
        entity_df=app.entity_df, features=features_to_get
    ).to_df()
    return{'status':True,"Message":"Entity DateFrame Created"}




# Endpoint for materialization
def materialize(start_date: str, end_date: str):
    # Converting string dates to datetimes
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Materializing features between given dates
    app.store.materialize(end_date=end_date, start_date=start_date)
    return{'status':True, 'message':'Data Pushed To Online Store'}





# Launching the API
# if __name__ == '__main__':
    
#     uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, access_log=True,debug= True)

