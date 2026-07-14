from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from src.schemas import GeneratedMetadata

#----- LLM SETUP ------ 
llm = ChatGroq(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    api_key=GROQ_API_KEY,
)

structured_llm = llm.with_structured_output(GeneratedMetadata)

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a pharmaceutical marketing content analyst."
     "Read the given content carefully and extract accurate metadata."
     "Only state facts that are directly supported by the content."
     "Do not invent information that is not present"),
     ("human","CONTENT:\n\n{content}")
])

metadata_chain = prompt | structured_llm

def generate_metadata(content : str) -> GeneratedMetadata:
    result = metadata_chain.invoke({"content" : content})
    return result
if __name__ == "__main__":
    sample_content = """
    Entresto - A New Standard in Heart Failure Management

    Entresto has shown significant reduction in cardiovascular death and heart
    failure hospitalization compared to standard therapy. Suitable for adult
    patients with chronic heart failure with reduced ejection fraction.
    """

    result = generate_metadata(sample_content)
    print(result)
    print("\n--- As dictionary ---")
    print(result.model_dump())