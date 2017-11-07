import os
import json
import requests
import pandas as pd


qs = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={:}&tickInterval="
periods = ["day", "hour", "thirtyMin", "fiveMin", "oneMin"]

r = requests.get("https://bittrex.com/api/v1.1/public/getmarkets")
markets = json.loads(r.content)["result"]

for m in markets:

    if m["IsActive"]:

        name = m["MarketName"].lower()
        name = "_".join(name.split("-"))
        print(name)

        for p in periods:

            r = requests.get(qs.format(m["MarketName"]) + p)
            res = json.loads(r.content)["result"]

            df = pd.DataFrame()
            df["open"] = [a["O"] for a in res]
            df["high"] = [a["H"] for a in res]
            df["low"] = [a["L"] for a in res]
            df["close"] = [a["C"] for a in res]
            df["date"] = pd.to_datetime([a["T"] for a in res],
                                        infer_datetime_format=True)
            df["volume"] = [a["V"] for a in res]
            df["basevol"] = [a["BV"] for a in res]

            fout = open("../dat/bittrex/tickdat/{:}_{:}.csv".format(name, p), 'w')
            df.to_csv(fout)




