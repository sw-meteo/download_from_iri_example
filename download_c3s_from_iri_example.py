cookie = '_ga=GA1.2.1868545142.1662905744; _gid=GA1.2.1317179236.1662905744; __dlauth_id=f4cafdae1a5690a78f88a4e4a4f79a8a70d05744ee787998e37c3ba4b381528ddb705908c903c8d678fac2030587bf98c6468751'

import requests
import time
import os

origins = ["ecmwf", "meteo_france", "dwd", "cmcc"]
origin_name_dict = {
    "ecmwf": "ECMWF",
    "cmcc" : "CMCC",
    "dwd": "DWD",
    "meteo_france": "Meteo_France",
}
model_name_dict = {
    "ecmwf": "SEAS5",
    "cmcc" : "SPSv3p5",
    "dwd": "GCFS2p1",
    "meteo_france": "System8",
}
level_required = {
    "t2m"   : 0,
    "z"     : [500],
    "ua"     : [200, 500, 700, 850],
    "va"     : [500, 700, 850],
}
var_list = ["z", "ua", "va", "t2m"]
odir = "/path/data/hindcast/iri/"


def retrieve_data(url, ofile):
    if os.path.isfile(f"{odir}{ofile}"):
        print(f"File {ofile} already exists, skipping")
    else:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Cookie': cookie,
        }
        time_s = time.time()
        response = session.get(url=url, headers=headers)
        with open(f"{odir}{ofile}", 'wb') as f:
            f.write(response.content)
        time_e = time.time()
        print(f"----- Downloaded {ofile} from {url}")
        if time_e - time_s < 5:
            print("Download fail!") # simple check according time spent
            os.system(f"trash {odir}{ofile}")
            raise IOError

for origin in origins:    
    origin_name = origin_name_dict[origin]; model_name = model_name_dict[origin]
    for lead_num in [1, 2, 3]:
        L = lead_num - 0.5
        
        for var_name in var_list:
            if (level_required[var_name] != 0):
                for level in level_required[var_name]:
                    var_name_full = f"{var_name}{level}"
                    url = f"https://iridl.ldeo.columbia.edu/SOURCES/.EU/.Copernicus/.CDS/.C3S/.{origin_name}/.{model_name}/.hindcast/.{var_name}/S/(Jan%201993)/(Nov%202016)/RANGE/L/({L})/VALUE/P/({level})/VALUE/Y/(4S)/(60N)/RANGE/X/(64E)/(160E)/RANGE/data.nc"
                    ofile = f"hindcast_{origin}_{var_name_full}_lead{lead_num}.nc"
                    retrieve_data(url, ofile)
            else: 
                var_name_full =  var_name
                url = f"https://iridl.ldeo.columbia.edu/SOURCES/.EU/.Copernicus/.CDS/.C3S/.{origin_name}/.{model_name}/.hindcast/.{var_name}/S/(Jan%201993)/(Nov%202016)/RANGE/L/({L})/VALUE/Y/(4S)/(60N)/RANGE/X/(64E)/(160E)/RANGE/data.nc"
                ofile = f"hindcast_{origin}_{var_name_full}_lead{lead_num}.nc"
                retrieve_data(url, ofile)
