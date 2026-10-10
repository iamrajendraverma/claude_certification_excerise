from models.research_model import TaskResult, ResearchTask




def execute_research_task(task: ResearchTask) -> TaskResult:
    """
    Execute one research task delegated by the coordinator.

    This is a placeholder. Replace it with actual web search
    and LLM-based research logic.
    """

    return TaskResult(
        task_id=task.task_id,
        agent_type=task.agent_type,
        findings=[
            f"Research has not been implemented yet for: "
            f"{task.description}"
        ],
        evidence=[],
    )
