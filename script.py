import os
import csv
import flask_login
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql
from flask import flash
from flask_login import login_required, current_user
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')


db = mysql.connector.connect(
    host=MAGIC_INVENTORY_HOST,
    user=MAGIC_INVENTORY_USER,
    passwd=MAGIC_INVENTORY_PASSWORD,
    database=MAGIC_INVENTORY_DATABASE,
    auth_plugin='mysql_native_password'
)


def process_csv(filename):
    alchDB = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD}@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'
    #alchDB = "mysql+pymysql://inventorybot:gio91030@localhost/testingdatabase"
    engine = create_engine(alchDB)

    SQL_Query = pd.read_sql_query('Select Name from cards', alchDB)

    df_Database = pd.DataFrame(SQL_Query, columns=['Name'])


    df_CSV_Name = pd.read_csv(filename, usecols=["Name"])

    df_CSV_Edition = pd.read_csv(filename, usecols=["Name","Edition"])

    df_CSV_all = pd.read_csv(filename,header = 0, index_col=False, low_memory=False, delimiter = ',')

    df_merge = df_Database.merge(df_CSV_Name, indicator=True, how='outer')

    df_check_name = df_merge.loc[lambda x: x['_merge'] == 'right_only']

    current_user_discordid = flask_login.current_user.discordid

    if df_check_name.empty == True:
        Names_Correct = True
    else:
        Names_Correct = False
        flash('Names that are not valid: ' + df_check_name.Name.to_string(index=False), category='error')

    df_check_edition = df_CSV_Edition['Edition'].isnull().values.any()


    if df_check_edition == False:
        Editions_Correct = True
    else:
        Editions_Correct = False
        flash('One or More entries are missing an edition', category='error')

    if Names_Correct and Editions_Correct is True:
        with engine.begin() as connection:
            df_add_discordid = df_CSV_all.assign(discordid = f'{current_user_discordid}')
            DF_toinport = df_add_discordid.rename({'Card Number':'cardnumber'}, axis='columns')
            DF_toinport.to_sql("inventory", con=connection, if_exists='append', index=False)
            flash('Have Been Imported', category='success')
            print('Committed')

