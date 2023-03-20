import pandas as pd
from WCIFManipMedlemmer import *

def check_person(name,wcaid):
    fil = pd.read_csv("members_extern.tsv",delimiter='\t')
    fil['Sidste comp'] = pd.to_datetime(fil['Sidste comp'])
    fil['Postnummer'] = fil['Postnummer'].astype('Int64')

    række = []
    if wcaid:
        række = fil[fil['WCA ID']==wcaid]
    elif name:
        række = fil[fil['Navn']==name]

    if len(række) == 1:
        navn = række['Navn'].iloc[0]
        wcaid = række['WCA ID'].iloc[0]
        sidste_comp = række['Sidste comp'].iloc[0]
        postnummer = række['Postnummer'].iloc[0]

        return (200,(navn,wcaid,sidste_comp,postnummer))
    else:
        return (404,(None,None,None,None))

def helper_import_extern_file():
    fil = pd.read_csv("members_extern.tsv",delimiter='\t')
    fil['Sidste comp'] = pd.to_datetime(fil['Sidste comp'])
    fil['Postnummer'] = fil['Postnummer'].astype('Int64')
    print(fil)

    for row in fil.values:
        if not pd.isnull(row[1]):
            status, (user_id, name, wcaid) = get_data_from_wcaid(row[1])
        else:
            status, (user_id, name, wcaid) = get_data_from_wcaid(row[5])
        if pd.isna(row[3]):
            postnummer=None
        else:
            postnummer = row[3]
        yield status,(user_id, name, wcaid,row[2],postnummer)