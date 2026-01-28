import pandas as pd
from pydantic import BaseModel, Field
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import HumanMessage, AIMessage

# STEP 1: Define the output schema
class SecurityDiagnosis(BaseModel):
    is_breach: bool = Field(description="Has a security policy been violated?")
    risk_score: int = Field(description="Risk level from 0 to 10")
    summary: str = Field(description="Explanation of the data lineage trace")

# STEP 2: The Agent Class
class ShadowTraceAgent:
    def __init__(self, policy_path=None):
        # We define the messages here, but we will handle the iterator 
        # inside the analyze_event method to prevent StopIteration.
        self.response_text = "Data trace indicates a potential policy violation regarding unauthorized data movement."

    def analyze_event(self, event_data: dict):
        # Re-initialize the Fake LLM for EVERY call so it never runs out of messages
        fake_responses = [AIMessage(content=self.response_text)]
        llm = GenericFakeChatModel(messages=iter(fake_responses))
        
        user_activity = str(event_data)
        
        # Simulate the LLM 'Reasoning'
        response = llm.invoke([HumanMessage(content=user_activity)])
        
        # Simple deterministic logic for risk score based on destination
        dest = str(event_data.get('destination', '')).lower()
        is_breach = any(domain in dest for domain in ["chatgpt", "dropbox", "external"])
        
        return SecurityDiagnosis(
            is_breach=is_breach, 
            risk_score=9 if is_breach else 2, 
            summary=response.content
        )