## Build a Hub-and-Spoke Research Coordinator

What you'll learn

- How hub-and-spoke architecture centralises all communication through a coordinator
- Why subagent isolation means every piece of context must be explicitly passed
- How to implement broad task decomposition that avoids the narrow decomposition failure
- How iterative refinement loops detect and fill coverage gaps
- Why tracing failures to the coordinator decomposition is the correct diagnostic approach

**1. Create a coordinator agent that accepts a broad research topic as input**

**Why:** The coordinator is the central hub in hub-and-spoke architecture. The exam tests whether you understand that the coordinator owns task decomposition, subagent selection, and result aggregation — not the subagents.

**You should see:** A coordinator function that accepts a topic string and returns a structured research report. It should have a system prompt defining its role as the orchestrating hub.

Ans : Created a cordinator **agent** which take the user prompt for example `The future of AI in Healthcare`  and **[step 1]** decompose into 
well define responsibilities given in the `system prompts` 

```text

COORDINATOR_SYSTEM_PROMPT = """
You are a Research Coordinator Agent operating in a
hub-and-spoke architecture.

Your responsibilities are:

1. Accept a broad research topic.
2. Decompose the topic into focused research tasks.
3. Select the appropriate specialized subagents.
4. Delegate tasks to the selected subagents.
5. Collect and evaluate their results.
6. Identify gaps and contradictions in the findings.
7. Aggregate the results into a structured research report.

The coordinator owns planning, orchestration, agent selection,
and final aggregation.

Subagents are responsible only for their assigned tasks.

Never fabricate research findings or evidence.
Clearly identify limitations and unanswered questions.
"""

```
Then the cordinator agent **[step2]** delegate the task to the **reseach sub agent** when the delegation completed coordinator agent **[step 3]** collect the final result and send back to the user. In the completion of all the 3 steps. 
`services/llm` and `models/reseach_model` plays a major roles. 

#### `model/resseach_model`

```python
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
```

#### Models

1. `ResearchReport` This model collect the final report and sent it back to the user.

2. `ResearchPlan` This model plan the complete research as per the `user prompt` and the `system-prompt`

3. `TaskResult` The `reseach sub agent` returns `TaskResult` object the task result given to `services/llm` to give the final result. 

#### Diagram flow 

```text
user-prompt ->
Main -> coordinator -> research agent -> coordinator - Main -> result-to-user
```

**2.Implement task decomposition logic that breaks the topic into at least 5 distinct subtopics covering the full breadth of the subject**

**Why:** Narrow decomposition is a specific exam failure pattern. The coordinator that only assigns solar and wind for renewable energy misses entire categories. The exam expects you to recognise that incomplete output traces back to the coordinator decomposition.

**You should see:** 
A decomposition function that produces 5 or more subtopics for any broad topic. For renewable energy, it should cover solar, wind, geothermal, tidal, biomass, and fusion at minimum.

Spawn two subagents (web search and document analysis) with explicit context passing — include all relevant information in each subagent prompt
Why: Subagent isolation means no shared memory and no inherited context. The exam heavily tests this: if a subagent produces poor results, check whether the coordinator gave it sufficient context, not whether the subagent itself is flawed.

**3. You should see: Two subagent invocations where each receives the full assigned subtopic, the research goal, and any relevant context from prior agents — all explicitly included in the prompt.**

**Why:** Subagent isolation means no shared memory and no inherited context. The exam heavily tests this: if a subagent produces poor results, check whether the coordinator gave it sufficient context, not whether the subagent itself is flawed.

**You should see:** Two subagent invocations where each receives the full assigned subtopic, the research goal, and any relevant context from prior agents — all explicitly included in the prompt.

**4.Aggregate results from both subagents and evaluate coverage completeness**

**Why:** The coordinator must evaluate whether the combined results cover the full breadth of the original topic. This is where iterative refinement starts — gaps detected here trigger re-delegation.

**You should see:** An aggregation function that combines results from both subagents and produces a coverage assessment listing which subtopics are well-covered, partially covered, or missing.

**5.Implement an iterative refinement loop: if the coordinator identifies coverage gaps, re-delegate to subagents with targeted queries and re-invoke until coverage is sufficient**

**Why:** Iterative refinement is a core coordinator responsibility the exam tests. A single-shot delegation is not enough — the coordinator must evaluate output and re-delegate for gaps. This distinguishes a coordinator from a simple dispatcher.

**You should see:** A loop that checks coverage, identifies gaps, sends targeted follow-up queries to subagents for the missing subtopics, and re-evaluates until a coverage threshold is met or a maximum iteration count is reached.

**6.Test with the topic renewable energy technologies and verify that the final output covers solar, wind, geothermal, tidal, biomass, and fusion**

**Why:** This specific test case maps to the exam narrow decomposition failure pattern. If your output only covers solar and wind, the root cause is the coordinator decomposition — the exact diagnostic the exam expects you to make.

**You should see:** A final research report with substantive sections on all six energy types: solar, wind, geothermal, tidal, biomass, and fusion. The coverage evaluation should show 100% completeness.









