import uuid 
from src.agents.compliance_agent import check_compliance
from src.ingestion.loader import load_all_assets
from src.agents.metadata_generator import generate_metadata
from src.agents.enrichment import(
    load_product_info, get_product_info,
    load_historical_performance, get_performance_metrics,
    load_activation_history,get_activation_summary
)
from src.schemas import AssetMetadata

def run_pipeline():
    assets = load_all_assets()
    product_info = load_product_info()
    performance_data = load_historical_performance()
    activation_data = load_activation_history()

    final_results = []
    
    for asset in assets : 
        print(f"\nProcessing : {asset['filename']}")

        context = asset["context"]
        #----- LLM se metadta genrate karwate hai ---- 
        generated = generate_metadata(asset["content"])

        #-- Step 4 - product_info.json se looku 
        product_facts = get_product_info(generated.product, product_info)

        #Step 5 - histoorical_performance.csv se lookup h 
        #Note- channel context se at hai , LLM se nahi 
        performance = get_performance_metrics(
            product = generated.product,
            channel = context.get("channel",""),
            audience=context.get("target_audience",""),
            campaign_type=context.get("campaign_type",""),
            performance_data = performance_data,
        )
        # activation history se lookup 
        activation = get_activation_summary(asset['filename'],activation_data)

        #Compliance cheup 
        compliance_result = check_compliance(
            summary=generated.summary,
            description=generated.description,
            approved_indication=product_facts["approved_indication"],
        )


        # =----Step 7 : Sab Luch jodkar final AssetMetadata banate hai 
        final_metadata = AssetMetadata(
            asset_id = str(uuid.uuid4())[:8],
            filename=asset["filename"],

            #LLM se 
              title=generated.title,
            summary=generated.summary,
            description=generated.description,
            keywords=generated.keywords,
            tone=generated.tone,
            confidence_score=generated.confidence_score,
            product=generated.product,

            # context se
            mlr_status=context.get("mlr_status", "pending"),
            country=context.get("country"),
            language=context.get("language", "en"),
            campaign_type=context.get("campaign_type"),
            target_audience=context.get("target_audience"),

            # product_info se
            therapeutic_area=product_facts["therapeutic_area"],
            approved_indication=product_facts["approved_indication"],

            # performance se
            avg_ctr=performance["avg_ctr"],
            avg_open_rate=performance["avg_open_rate"],
            avg_conversion_rate=performance["avg_conversion_rate"],
            avg_engagement_score=performance["avg_engagement_score"],
            performance_sample_size=performance["sample_size"],

            # activation se
            times_activated=activation["times_activated"],
            last_activated_channel=activation["last_activated_channel"],
            last_activated_date=activation["last_activated_date"],

            #compliance check se 
            compliance_status = compliance_result.status,
            compliance_notes = compliance_result.notes,
        )

        final_results.append(final_metadata)
        print(f"Done : {final_metadata.title}")

    return final_results


from src.export.excel_export import export_to_excel

if __name__ == "__main__":
    results = run_pipeline()
    print(f"\n\nTotal processed: {len(results)}")

    export_to_excel(results)



