import pandas as pd 
from  src.config import OUTPUTS_DIR

def export_to_excel(results : list, filename : str ="content_metadata_catalogue.xlsx"):
    rows = [item.model_dump() for item in results]

    df = pd.DataFrame(rows)

    # as keyword contain a list of words so imporve it readability 
    if "keywords" in df.columns:
        df["keywords"] = df["keywords"].apply(lambda kw_list: ", ".join(kw_list))

    output_path = OUTPUTS_DIR / filename
    df.to_excel(output_path,index=False,sheet_name="Metadata Catalogue")

    print(f"Excel file saved : {output_path}")
    return output_path