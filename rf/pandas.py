#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("/home/pi/ecg/sensor_data.db")
df = pd.read_sql_query("SELECT * from sensor_data", con)

# verify that result of SQL query is stored in the dataframe
print(df.head())

con.close()
