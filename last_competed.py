import polars as pl
import pandas as pd
from datetime import datetime,timedelta
# from models import *
import os
from models import Users,External_payments

def get_date(x):
    return f"{x['year']}-{x['endMonth']}-{x['endDay']}"

def get_df():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    comp_path = os.path.join(script_dir, '../wca_export/WCA_export_Competitions.tsv')
    res_path = os.path.join(script_dir, '../wca_export/WCA_export_Results.tsv')

    dk = (pl.read_csv(comp_path,separator='\t',quote_char='',low_memory=True)).lazy().filter(pl.col('countryId')=='Denmark')
    res = pl.read_csv(res_path,separator='\t',quote_char='',low_memory=True).lazy()

    dk_res = dk.join(res,left_on='id',right_on='competitionId').select(["id","personId","endDay","endMonth","year"])

    dk_res = dk_res.group_by(['id','personId']).first()

    dk_res = dk_res.with_columns(
        pl.concat_str(
            [pl.col("year").cast(str), pl.col("endMonth").cast(str), pl.col("endDay").cast(str)],
            separator="-"
        ).str.strptime(pl.Date, "%Y-%m-%d").alias("Sidste comp")
    ).select(["Sidste comp","personId"])

    dk_res = (
        dk_res.sort("Sidste comp", descending=True)
            .group_by("personId")
            .first()
    )

    return dk_res

def get_last_competed(df,wcaid):
    if not pd.isnull(wcaid):
        try:
            competed = df.filter(pl.col("personId") == wcaid).select("Sidste comp").collect().to_series(0).to_list()[0]
            return 200,competed
        except IndexError: # If they have a WCA ID, but haven't competed in Denmark
            return 404,'blank'
    return 404,"blank"

def active_member(user:Users):
    fourteen_months_ago = datetime.now() - timedelta(days=14*30)
    if user.sidste_comp:
        eligible = user.sidste_comp >= fourteen_months_ago
    else:
        eligible = False
    wants_to = user.medlem

    payment = External_payments.query.filter_by(user_id=user.user_id).order_by(External_payments.payment_date.desc()).first()
    has_payment = payment is not None and payment.payment_date >= fourteen_months_ago
    eligible = eligible or has_payment

    return eligible,wants_to