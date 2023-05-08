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

    dk = (pl.read_csv(comp_path,sep='\t')).lazy().filter(pl.col('countryId')=='Denmark')
    res = pl.read_csv(res_path,sep='\t').lazy()

    dk_res = dk.join(res,left_on='id',right_on='competitionId').select(["id","personId","personName","endDay","endMonth","year"])

    dk_res = dk_res.groupby(['id','personId']).first().collect().to_pandas()

    dk_res['Sidste comp'] = pd.to_datetime(dk_res.apply(get_date,axis=1))
    max_dates = dk_res.groupby('personId')['Sidste comp'].idxmax()
    dk_res = dk_res.loc[max_dates]
    dk_res = dk_res.rename(columns={'personId':'WCA ID',"personName":'Navn'})
    return dk_res

def get_last_competed(df,wcaid):
    if not pd.isnull(wcaid):
        competed = df[df['WCA ID']==wcaid]['Sidste comp'].iloc[0].to_pydatetime()
        return 200,competed
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