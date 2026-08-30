#!/usr/bin/env python3
"""Agents SDK orchestration for Medium course lesson generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRunResult:
    article: str
    evidence_review: str
    draft: str
    technical_review: str
    continuity_review: str


def _load_agents_sdk():
    try:
        from agents import Agent, ModelSettings, RunConfig, Runner
    except ImportError as exc:
        raise RuntimeError(
            "GENERATION_BACKEND=agents requires the openai-agents package. "
            "Install dependencies with `pip install -r requirements.txt`."
        ) from exc
    return Agent, ModelSettings, RunConfig, Runner


def build_course_agents(model: str, max_tokens: int = 7000):
    Agent, ModelSettings, _, _ = _load_agents_sdk()
    from agents import WebSearchTool

    settings = ModelSettings(max_tokens=max_tokens)

    evidence_researcher = Agent(
        name="Primary-source evidence researcher",
        handoff_description="Finds current primary sources for the lesson's technical claims.",
        instructions=(
            "Research the requested lesson using web search. Return a compact evidence brief with "
            "claim-to-source mappings and direct HTTPS URLs. Prefer official documentation, standards, "
            "and original papers. Verify that every URL supports the mapped claim; do not invent URLs."
        ),
        tools=[WebSearchTool()],
        model=model,
        model_settings=ModelSettings(max_tokens=2600),
    )

    draft_agent = Agent(
        name="Course lesson draft agent",
        handoff_description="Writes the first complete Medium course lesson draft.",
        instructions=(
            "Write practical Medium course lessons for software engineers. "
            "Use concrete examples, clear section headings, and a human technical voice. "
            "Do not invent citations or URLs. Mark uncertain claims with [SOURCE NEEDED: reason]."
        ),
        model=model,
        model_settings=settings,
    )

    technical_reviewer = Agent(
        name="Technical reviewer agent",
        handoff_description="Reviews technical correctness, overclaims, and missing nuance.",
        instructions=(
            "Review the lesson for technical correctness, production realism, unsupported claims, "
            "missing nuance, and misleading simplifications. Return concise revision notes."
        ),
        model=model,
        model_settings=ModelSettings(max_tokens=1800),
    )

    continuity_reviewer = Agent(
        name="Course continuity reviewer agent",
        handoff_description="Checks whether the lesson fits the course sequence.",
        instructions=(
            "Review the lesson as part of a course series. Check prerequisites, previous/next "
            "navigation, project progression, repeated setup context, and unexplained future concepts. "
            "Return concise revision notes."
        ),
        model=model,
        model_settings=ModelSettings(max_tokens=1800),
    )

    publishing_editor = Agent(
        name="Publishing editor agent",
        handoff_description="Applies review notes and produces final Medium-ready Markdown.",
        instructions=(
            "Produce the final Medium-ready Markdown article. Preserve useful examples and exercises. "
            "Apply technical and continuity review notes. Include Learning Outcomes, Worked Example, "
            "Exercise, Recap, and Next Lesson sections. Keep the article focused and human."
        ),
        model=model,
        model_settings=settings,
    )

    manager = Agent(
        name="Course generation manager",
        instructions=(
            "Coordinate a Medium course lesson workflow. Use specialist agents for drafting, "
            "technical review, continuity review, and final publishing edits when the task requires it."
        ),
        handoffs=[evidence_researcher, draft_agent, technical_reviewer, continuity_reviewer, publishing_editor],
        model=model,
        model_settings=ModelSettings(max_tokens=1200),
    )

    return {
        "manager": manager,
        "evidence_research": evidence_researcher,
        "draft": draft_agent,
        "technical_review": technical_reviewer,
        "continuity_review": continuity_reviewer,
        "publishing_editor": publishing_editor,
    }


def run_course_generation_with_agents(
    prompt: str,
    *,
    model: str,
    group_id: str | None = None,
    tracing_disabled: bool = False,
    scripted_model=None,
) -> AgentRunResult:
    """Run a code-sequenced Agents SDK workflow for scheduled lesson generation."""

    _, _, RunConfig, Runner = _load_agents_sdk()
    course_agents = build_course_agents(model)
    run_config = RunConfig(
        model=scripted_model or model,
        workflow_name="Daily Medium Course DOCX",
        group_id=group_id,
        trace_metadata={"backend": "agents", "content_type": "medium_course_lesson"},
        tracing_disabled=tracing_disabled,
    )

    evidence_result = Runner.run_sync(
        course_agents["evidence_research"],
        prompt,
        max_turns=4,
        run_config=run_config,
    )
    evidence_review = str(evidence_result.final_output).strip()

    draft_result = Runner.run_sync(
        course_agents["draft"],
        f"{prompt}\n\nVerified primary-source research brief:\n{evidence_review}",
        max_turns=3,
        run_config=run_config,
    )
    draft = str(draft_result.final_output).strip()

    technical_result = Runner.run_sync(
        course_agents["technical_review"],
        f"Original prompt:\n{prompt}\n\nDraft:\n{draft}",
        max_turns=2,
        run_config=run_config,
    )
    technical_review = str(technical_result.final_output).strip()

    continuity_result = Runner.run_sync(
        course_agents["continuity_review"],
        f"Original prompt:\n{prompt}\n\nDraft:\n{draft}",
        max_turns=2,
        run_config=run_config,
    )
    continuity_review = str(continuity_result.final_output).strip()

    final_result = Runner.run_sync(
        course_agents["publishing_editor"],
        (
            f"Original prompt:\n{prompt}\n\n"
            f"Verified evidence brief:\n{evidence_review}\n\n"
            f"Draft:\n{draft}\n\n"
            f"Technical review notes:\n{technical_review}\n\n"
            f"Course continuity review notes:\n{continuity_review}\n\n"
            "Return only the final Medium-ready Markdown article."
        ),
        max_turns=3,
        run_config=run_config,
    )
    article = str(final_result.final_output).strip()

    return AgentRunResult(
        article=article,
        evidence_review=evidence_review,
        draft=draft,
        technical_review=technical_review,
        continuity_review=continuity_review,
    )
