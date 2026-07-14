from pydantic import BaseModel, Field
from typing import List, Optional


class GeneratedMetadata(BaseModel):
    """
    LLM sirf ye fields banayega - content padhkar.
    """
    title: str = Field(description="A short, clear title for the content")
    summary: str = Field(description="2-3 sentence summary of what the content covers")
    description: str = Field(description="Slightly longer description than summary")
    keywords: List[str] = Field(description="5-8 relevant keywords")
    product: str = Field(description="The drug/product name mentioned in the content")
    tone: str = Field(description="Tone of the content, e.g. Clinical, Empathetic, Formal")
    confidence_score: float = Field(description="Model's confidence in this output, 0 to 1")


class AssetMetadata(BaseModel):
    """
    Final row - Excel me jaayegi. Teen sources se banti hai:
    1. GeneratedMetadata (LLM se)
    2. asset_context.json (MLR, country, language, campaign_type, audience)
    3. product_info.json + historical_performance.csv (lookups)
    """
    asset_id: str
    filename: str

    # ---- LLM se (GeneratedMetadata se copy hoga) ----
    title: str = ""
    summary: str = ""
    description: str = ""
    keywords: List[str] = Field(default_factory=list)
    tone: str = ""
    confidence_score: float = 0.0

    # ---- asset_context.json se (given, per-asset) ----
    mlr_status: str = "pending"
    country: Optional[str] = None
    language: str = "en"
    campaign_type: Optional[str] = None
    target_audience: Optional[str] = None

    # ---- product_info.json se (lookup, using product name) ----
    product: str = ""
    therapeutic_area: str = ""
    approved_indication: str = ""

    # ---- historical_performance.csv se (lookup) ----
    avg_ctr: float = 0.0
    avg_open_rate: float = 0.0
    avg_conversion_rate: float = 0.0
    avg_engagement_score: float = 0.0
    performance_sample_size: int = 0

    # ---- activation_history.csv se (lookup) ----
    times_activated: int = 0
    last_activated_channel: Optional[str] = None
    last_activated_date: Optional[str] = None

    # ---- Compliance Agent se (baad me banayenge) ----
    compliance_status: str = "needs_review"
    compliance_notes: List[str] = Field(default_factory=list)



from typing import Literal

class ComplianceCheckResult(BaseModel):
    status : Literal["pass","needs_review"]=Field(
        description=" 'pass' if content matches approved indication, 'needs_review'  if there's a mismatch or concern  "

    )
    notes : List[str] = Field(
        default_factory= list,
        description="Specific Reasons for flagging, empty list if status is 'pass' "
    )