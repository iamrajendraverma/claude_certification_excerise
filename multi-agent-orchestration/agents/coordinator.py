
from models.research_model import ResearchReport,ResearchPlan
from agents.research_agent import execute_research_task
from services.llm import ask_claude_structured
from prompts.coordinator import COORDINATOR_SYSTEM_PROMPT

def coordinator(topic:str) ->ResearchReport:
    """Coordinate research and return a structured report."""
    print("I am a coordinator agent")
    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")
    # step 1 : Decompose the topic and select subagents 
    plan  = ask_claude_structured(system_prompt=COORDINATOR_SYSTEM_PROMPT,user_prompt=f"""
    Create a reseach plan for this topic:
    {topic}
            Break it into focused tasks and select the appropriate
        specialized research agents.
        """,
        response_model=ResearchPlan,

    )
    # step 2 : Delegate the task to selected sub-agents 

    results =[execute_research_task(task) for task in plan.tasks]   

    # step 3 : Aggregate findings into a strcutured report 

    report =  ask_claude_structured(
        system_prompt=COORDINATOR_SYSTEM_PROMPT,
        user_prompt=f"""
        Research topic: {topic}

        Research plan:
        {plan.model_dump_json(indent=2)}

        Subagent results:
        {[result.model_dump() for result in results]}

        Aggregate the findings into a ResearchReport.
        Do not invent evidence or citations.
        """,
        response_model=ResearchReport,
    )
    return report     

