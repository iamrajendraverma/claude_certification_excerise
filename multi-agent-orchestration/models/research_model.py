
from pydantic import BaseModel, Field


class ResearchReport(BaseModel):
    """This model defines the format of the coordinator's final output """
    topic: str
    executive_summary: str
    key_findings: list[str] = Field(default_factory=list)
    supporting_evidence: list[str] = Field(default_factory=list)
    risks_and_limitations: list[str] = Field(default_factory=list)
    conclusion: str

class ResearchTask(BaseModel):
    task_id:str
    description:str
    agent_type:str

class ResearchPlan(BaseModel):
    topic: str
    tasks: list[ResearchTask]

class TaskResult(BaseModel):
    task_id: str
    agent_type: str
    findings: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)

