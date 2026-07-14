from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import GROQ_API_KEY, LLM_MODEL
from src.schemas import ComplianceCheckResult


llm = ChatGroq(model=LLM_MODEL, temperature=0.0, api_key=GROQ_API_KEY)
structured_llm = llm.with_structured_output(ComplianceCheckResult)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a pharmaceutical regulatory compliance reviewer. "
     "Your job is to check if generated marketing metadata makes any medical "
     "claim that goes beyond the officially approved indication. "
     "Flag anything uncertain as 'needs_review' rather than assuming it's fine. "
     "Be specific in your notes about which claim is concerning and why."),
    ("human",
     "GENERATED SUMMARY:\n{summary}\n\n"
     "GENERATED DESCRIPTION:\n{description}\n\n"
     "APPROVED INDICATION FOR THIS PRODUCT:\n{approved_indication}\n\n"
     "Does the summary or description make any claim beyond the approved indication?")
])

compliance_chain = prompt | structured_llm


def check_compliance(summary: str, description: str, approved_indication: str) -> ComplianceCheckResult:
   
    if not approved_indication:
        # Agar humare paas approved indication hi nahi hai is product ke liye,
        # to hum confidently "pass" nahi keh sakte - safe default "needs_review"
        return ComplianceCheckResult(
            status="needs_review",
            notes=["No approved indication found on record for this product."]
        )

    result = compliance_chain.invoke({
        "summary": summary,
        "description": description,
        "approved_indication": approved_indication,
    })
    return result