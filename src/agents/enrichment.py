import json
import csv
from src.config import PRODUCT_INFO_FILE,HISTORICAL_PERFORMANCE_FILE,ACTIVATION_HISOTRY_FILE


def load_product_info() -> dict:
    with open(PRODUCT_INFO_FILE,"r") as f:
        return json.load(f)
    
def get_product_info(product_name : str, product_info : dict)->dict:
    for key,value in product_info.items():
        if key.lower() == product_name.lower():
            return value
    return {"approved_indication": "", "therapeutic_area": ""}
#-----Load_historical_performace----------

def load_historical_performance() -> list:
    
    with open(HISTORICAL_PERFORMANCE_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _format_performance_row(row: dict) -> dict:
    """CSV se aaya row hamesha string hota hai, isliye numbers me convert karte hai."""
    return {
        "avg_ctr": float(row["avg_ctr"]),
        "avg_open_rate": float(row["avg_open_rate"]),
        "avg_conversion_rate": float(row["avg_conversion_rate"]),
        "avg_engagement_score": float(row["avg_engagement_score"]),
        "sample_size": int(row["sample_size"]),
    }


def get_performance_metrics(product: str, channel: str, audience: str,
                             campaign_type: str, performance_data: list) -> dict:
    """
    Best matching row dhundta hai. Pehle exact match try karta hai,
    agar na mile to dheere-dheere match ko dheela (broaden) karta hai.
    """
    # Level 1: exact match (product + channel + audience + campaign_type)
    for row in performance_data:
        if (row["product"].lower() == product.lower()
                and row["channel"].lower() == channel.lower()
                and row["audience"].lower() == audience.lower()
                and row["campaign_type"].lower() == campaign_type.lower()):
            return _format_performance_row(row)

    # Level 2: sirf product + channel se match
    for row in performance_data:
        if row["product"].lower() == product.lower() and row["channel"].lower() == channel.lower():
            return _format_performance_row(row)

    # Level 3: sirf product se match (sabse pehla match jo mile)
    for row in performance_data:
        if row["product"].lower() == product.lower():
            return _format_performance_row(row)

    # Kuch na mile to default (0 values + sample_size 0, taaki pata chale "no data")
    return {"avg_ctr": 0.0, "avg_open_rate": 0.0, "avg_conversion_rate": 0.0,
            "avg_engagement_score": 0.0, "sample_size": 0}


#------- Activation History Lookup -------

def load_activation_history()-> list :
    with open(ACTIVATION_HISOTRY_FILE,"r") as f:
        reader = csv.DictReader(f)
        return list(reader)
    

def get_activation_summary(filename:str, activation_data : list) -> dict:
    matches = [row for row in activation_data if row["filename"] == filename]

    if not matches:
        return {"times_activated":0, "last_activated_channel":None,"last_activated_date":None}
    matches.sort(key=lambda r: r["activation_date"])
    latest = matches[-1]

    return{
          "times_activated": len(matches),
        "last_activated_channel": latest["activated_channel"],
        "last_activated_date": latest["activation_date"],

    }