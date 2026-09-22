from typing import List, Optional
from app.repository import Repository
from app.models import SearchResultItem

class SearchService:
    @staticmethod
    def search(
        query: str = "",
        entity_types: Optional[List[str]] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 40
    ) -> List[SearchResultItem]:
        q_tokens = [t.lower() for t in query.strip().split() if t]
        results: List[SearchResultItem] = []

        def match_score(text: str, title: str = "") -> float:
            if not q_tokens:
                return 1.0
            score = 0.0
            text_lower = text.lower()
            title_lower = title.lower()
            for token in q_tokens:
                if token in title_lower:
                    score += 5.0
                elif token in text_lower:
                    score += 1.5
            return score

        types_to_search = set(entity_types) if entity_types else {
            "task", "project", "idea", "experiment", "decision", "research", "learning", "opportunity"
        }

        # 1. Tasks
        if "task" in types_to_search:
            tasks = Repository.get_tasks()
            for t in tasks:
                if status and t.status.value != status:
                    continue
                if priority and t.priority.value != priority:
                    continue
                if tag and tag not in t.tags:
                    continue
                full_text = f"{t.title} {t.blocker_reason or ''} {' '.join(t.tags)}"
                score = match_score(full_text, t.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=t.id,
                        entity_type="task",
                        title=t.title,
                        subtitle=f"Task • {t.priority.value.upper()} • {t.status.value}",
                        status=t.status.value,
                        priority=t.priority.value,
                        snippet=t.blocker_reason or f"Energy: {t.energy_level.value}",
                        date=t.deadline or t.scheduled_date,
                        tags=t.tags,
                        relevance_score=score
                    ))

        # 2. Projects
        if "project" in types_to_search:
            projects = Repository.get_projects()
            for p in projects:
                if status and p.status.value != status:
                    continue
                full_text = f"{p.title} {p.description or ''} {p.category.value} {' '.join(p.next_actions)}"
                score = match_score(full_text, p.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=p.id,
                        entity_type="project",
                        title=p.title,
                        subtitle=f"Project • {p.category.value} • Health: {p.health.value}",
                        status=p.status.value,
                        category=p.category.value,
                        snippet=(p.description or "")[:140] + ("..." if len(p.description or "") > 140 else ""),
                        date=p.target_date,
                        tags=[p.category.value, f"health:{p.health.value}"],
                        relevance_score=score + 1.0  # Projects get slight boost
                    ))

        # 3. Ideas
        if "idea" in types_to_search:
            ideas = Repository.get_ideas()
            for i in ideas:
                if status and i.status.value != status:
                    continue
                if priority and i.priority.value != priority:
                    continue
                full_text = f"{i.title} {i.description or ''} {i.origin or ''} {i.next_action or ''}"
                score = match_score(full_text, i.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=i.id,
                        entity_type="idea",
                        title=i.title,
                        subtitle=f"Idea • {i.category.value} • Stage: {i.status.value}",
                        status=i.status.value,
                        priority=i.priority.value,
                        category=i.category.value,
                        snippet=(i.description or i.next_action or "")[:140],
                        date=i.created_at[:10],
                        tags=[i.category.value, i.status.value],
                        relevance_score=score
                    ))

        # 4. Experiments
        if "experiment" in types_to_search:
            exps = Repository.get_experiments()
            for e in exps:
                if status and e.status.value != status:
                    continue
                full_text = f"{e.title} {e.hypothesis} {e.objective} {e.evidence or ''} {e.conclusion or ''}"
                score = match_score(full_text, e.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=e.id,
                        entity_type="experiment",
                        title=e.title,
                        subtitle=f"Experiment • Status: {e.status.value}",
                        status=e.status.value,
                        snippet=f"Hypothesis: {e.hypothesis[:120]}...",
                        date=e.created_at[:10],
                        tags=[e.status.value],
                        relevance_score=score
                    ))

        # 5. Decisions
        if "decision" in types_to_search:
            decisions = Repository.get_decisions()
            for d in decisions:
                if status and d.status.value != status:
                    continue
                full_text = f"{d.title} {d.context} {d.assumptions} {d.actual_outcome or d.expected_outcome} {d.lessons_learned or ''}"
                score = match_score(full_text, d.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=d.id,
                        entity_type="decision",
                        title=d.title,
                        subtitle=f"Decision • Confidence: {d.confidence_level}% • {d.date}",
                        status=d.status.value,
                        snippet=f"Context: {d.context[:120]}...",
                        date=d.date,
                        tags=[d.status.value, f"confidence:{d.confidence_level}%"],
                        relevance_score=score
                    ))

        # 6. Research
        if "research" in types_to_search:
            research = Repository.get_research_entries()
            for r in research:
                if status and r.status.value != status:
                    continue
                full_text = f"{r.research_question} {r.topic} {r.investigations or ''} {r.conclusions or ''}"
                score = match_score(full_text, r.research_question)
                if score > 0:
                    results.append(SearchResultItem(
                        id=r.id,
                        entity_type="research",
                        title=r.research_question,
                        subtitle=f"Research • Topic: {r.topic} • {r.status.value}",
                        status=r.status.value,
                        category=r.topic,
                        snippet=(r.conclusions or r.investigations or "")[:140],
                        date=r.created_at[:10],
                        tags=[r.topic, r.status.value],
                        relevance_score=score
                    ))

        # 7. Learning
        if "learning" in types_to_search:
            learning = Repository.get_learning_items()
            for l in learning:
                if status and l.status.value != status:
                    continue
                full_text = f"{l.title} {l.subject} {l.notes or ''} {l.key_takeaways or ''}"
                score = match_score(full_text, l.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=l.id,
                        entity_type="learning",
                        title=l.title,
                        subtitle=f"Learning • {l.subject} • {l.progress_pct}%",
                        status=l.status.value,
                        category=l.subject,
                        snippet=(l.key_takeaways or l.notes or "")[:140],
                        date=l.created_at[:10],
                        tags=[l.subject, l.type.value],
                        relevance_score=score
                    ))

        # 8. Opportunities
        if "opportunity" in types_to_search:
            opps = Repository.get_opportunities()
            for o in opps:
                if status and o.status.value != status:
                    continue
                full_text = f"{o.title} {o.description or ''} {o.category.value} {o.potential_upside or ''} {o.risks or ''}"
                score = match_score(full_text, o.title)
                if score > 0:
                    results.append(SearchResultItem(
                        id=o.id,
                        entity_type="opportunity",
                        title=o.title,
                        subtitle=f"Opportunity • {o.category.value} • {o.status.value}",
                        status=o.status.value,
                        category=o.category.value,
                        snippet=(o.potential_upside or o.description or "")[:140],
                        date=o.date_discovered,
                        tags=[o.category.value, o.status.value],
                        relevance_score=score
                    ))

        # Sort descending by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]
