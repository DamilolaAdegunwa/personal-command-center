from typing import List, Dict, Any, Optional
from app.repository import Repository
from app.models import GraphData, GraphNode, GraphEdge

class GraphService:
    @staticmethod
    def get_full_graph() -> GraphData:
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        seen_node_ids = set()
        seen_edge_keys = set()

        # 1. Projects
        projects = Repository.get_projects()
        for p in projects:
            if p.id not in seen_node_ids:
                seen_node_ids.add(p.id)
                nodes.append(GraphNode(
                    id=p.id,
                    label=p.title,
                    type="project",
                    subtitle=f"{p.category} • {p.progress_pct}%",
                    status=p.status,
                    health=p.health,
                    data={"description": p.description, "category": p.category, "health": p.health, "progress": p.progress_pct}
                ))

        # 2. Ideas
        ideas = Repository.get_ideas()
        for i in ideas:
            if i.id not in seen_node_ids:
                seen_node_ids.add(i.id)
                nodes.append(GraphNode(
                    id=i.id,
                    label=i.title,
                    type="idea",
                    subtitle=f"{i.category} • {i.status}",
                    status=i.status,
                    data={"description": i.description, "origin": i.origin, "priority": i.priority, "next_action": i.next_action}
                ))
            if i.related_project_id and i.related_project_id in seen_node_ids:
                edge_key = (i.id, i.related_project_id, "spawns")
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(GraphEdge(
                        id=f"edge-{i.id}-{i.related_project_id}",
                        source=i.id,
                        target=i.related_project_id,
                        relation="spawns",
                        notes="Idea attached to project"
                    ))

        # 3. Experiments
        experiments = Repository.get_experiments()
        for e in experiments:
            if e.id not in seen_node_ids:
                seen_node_ids.add(e.id)
                nodes.append(GraphNode(
                    id=e.id,
                    label=e.title,
                    type="experiment",
                    subtitle=f"Status: {e.status}",
                    status=e.status,
                    data={"hypothesis": e.hypothesis, "objective": e.objective, "conclusion": e.conclusion}
                ))
            if e.idea_id and e.idea_id in seen_node_ids:
                edge_key = (e.idea_id, e.id, "validates")
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(GraphEdge(
                        id=f"edge-{e.idea_id}-{e.id}",
                        source=e.idea_id,
                        target=e.id,
                        relation="validates",
                        notes="Experiment tests idea"
                    ))
            if e.project_id and e.project_id in seen_node_ids:
                edge_key = (e.id, e.project_id, "informs")
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(GraphEdge(
                        id=f"edge-{e.id}-{e.project_id}",
                        source=e.id,
                        target=e.project_id,
                        relation="informs",
                        notes="Experiment outcome informs project"
                    ))

        # 4. Decisions
        decisions = Repository.get_decisions()
        for d in decisions:
            if d.id not in seen_node_ids:
                seen_node_ids.add(d.id)
                nodes.append(GraphNode(
                    id=d.id,
                    label=d.title,
                    type="decision",
                    subtitle=f"Confidence: {d.confidence_level}% • {d.date}",
                    status=d.status,
                    data={"context": d.context, "confidence": d.confidence_level, "outcome": d.actual_outcome or d.expected_outcome}
                ))

        # 5. Research Entries
        research = Repository.get_research_entries()
        for r in research:
            if r.id not in seen_node_ids:
                seen_node_ids.add(r.id)
                nodes.append(GraphNode(
                    id=r.id,
                    label=r.research_question,
                    type="research",
                    subtitle=f"{r.topic} • {r.status}",
                    status=r.status,
                    data={"topic": r.topic, "conclusions": r.conclusions}
                ))
            if r.related_project_id and r.related_project_id in seen_node_ids:
                edge_key = (r.id, r.related_project_id, "informs")
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(GraphEdge(
                        id=f"edge-{r.id}-{r.related_project_id}",
                        source=r.id,
                        target=r.related_project_id,
                        relation="informs",
                        notes="Research supports project"
                    ))

        # 6. Learning Items
        learning = Repository.get_learning_items()
        for l in learning:
            if l.id not in seen_node_ids:
                seen_node_ids.add(l.id)
                nodes.append(GraphNode(
                    id=l.id,
                    label=l.title,
                    type="learning",
                    subtitle=f"{l.subject} • {l.progress_pct}%",
                    status=l.status,
                    data={"subject": l.subject, "progress": l.progress_pct, "key_takeaways": l.key_takeaways}
                ))

        # 7. Opportunities
        opps = Repository.get_opportunities()
        for o in opps:
            if o.id not in seen_node_ids:
                seen_node_ids.add(o.id)
                nodes.append(GraphNode(
                    id=o.id,
                    label=o.title,
                    type="opportunity",
                    subtitle=f"{o.category} • {o.status}",
                    status=o.status,
                    data={"category": o.category, "upside": o.potential_upside, "risks": o.risks}
                ))

        # 8. Explicit Knowledge Edges
        explicit_edges = Repository.get_edges()
        for ee in explicit_edges:
            if ee.source_id in seen_node_ids and ee.target_id in seen_node_ids:
                edge_key = (ee.source_id, ee.target_id, ee.relation_type)
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(GraphEdge(
                        id=ee.id,
                        source=ee.source_id,
                        target=ee.target_id,
                        relation=ee.relation_type,
                        notes=ee.notes
                    ))

        return GraphData(nodes=nodes, edges=edges)
