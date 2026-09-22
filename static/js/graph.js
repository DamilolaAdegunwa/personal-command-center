// Interactive Knowledge Graph Visualizer using SVG and Force-Directed Layout
class KnowledgeGraph {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.options = Object.assign({
      width: 900,
      height: 600,
      onNodeClick: null
    }, options);

    this.nodes = [];
    this.edges = [];
    this.nodeMap = new Map();
    this.simulation = null;
    this.transform = { x: 0, y: 0, k: 1 };
    this.isDragging = false;
    this.dragStart = { x: 0, y: 0 };
    this.activeTypeFilter = "all";

    this.init();
  }

  init() {
    this.container.innerHTML = `
      <svg id="kg-svg" width="100%" height="100%" style="cursor: grab;">
        <defs>
          <marker id="arrow" viewBox="0 -5 10 10" refX="22" refY="0" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0,-5L10,0L0,5" fill="#475569"></path>
          </marker>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>
        <g id="kg-viewport">
          <g id="kg-links"></g>
          <g id="kg-nodes"></g>
        </g>
      </svg>
    `;

    this.svg = document.getElementById("kg-svg");
    this.viewport = document.getElementById("kg-viewport");
    this.linksGroup = document.getElementById("kg-links");
    this.nodesGroup = document.getElementById("kg-nodes");

    this.setupEvents();
  }

  setupEvents() {
    // Pan & Zoom
    this.svg.addEventListener("wheel", (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
      this.transform.k = Math.max(0.2, Math.min(3, this.transform.k * zoomFactor));
      this.applyTransform();
    });

    this.svg.addEventListener("mousedown", (e) => {
      if (e.target.closest(".kg-node")) return;
      this.isDragging = true;
      this.dragStart = { x: e.clientX - this.transform.x, y: e.clientY - this.transform.y };
      this.svg.style.cursor = "grabbing";
    });

    window.addEventListener("mousemove", (e) => {
      if (!this.isDragging) return;
      this.transform.x = e.clientX - this.dragStart.x;
      this.transform.y = e.clientY - this.dragStart.y;
      this.applyTransform();
    });

    window.addEventListener("mouseup", () => {
      this.isDragging = false;
      this.svg.style.cursor = "grab";
    });
  }

  applyTransform() {
    this.viewport.setAttribute("transform", `translate(${this.transform.x}, ${this.transform.y}) scale(${this.transform.k})`);
  }

  resetView() {
    const rect = this.container.getBoundingClientRect();
    this.transform = { x: rect.width / 2, y: rect.height / 2, k: 0.85 };
    this.applyTransform();
  }

  setTypeFilter(type) {
    this.activeTypeFilter = type;
    this.render();
  }

  setData(data) {
    const rect = this.container.getBoundingClientRect();
    const width = rect.width || 900;
    const height = rect.height || 600;

    this.nodeMap.clear();
    this.nodes = data.nodes.map((n, i) => {
      // Arrange initial radial cluster
      const angle = (i / data.nodes.length) * 2 * Math.PI;
      const radius = 180 + (i % 3) * 60;
      const node = {
        ...n,
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        vx: 0,
        vy: 0
      };
      this.nodeMap.set(n.id, node);
      return node;
    });

    this.edges = data.edges.filter(e => this.nodeMap.has(e.source) && this.nodeMap.has(e.target));
    this.resetView();
    this.runSimulation();
    this.render();
  }

  runSimulation() {
    // 60 iterations of spring force layout
    for (let step = 0; step < 60; step++) {
      // Repulsion between nodes
      for (let i = 0; i < this.nodes.length; i++) {
        for (let j = i + 1; j < this.nodes.length; j++) {
          const a = this.nodes[i];
          const b = this.nodes[j];
          let dx = b.x - a.x;
          let dy = b.y - a.y;
          let dist = Math.sqrt(dx * dx + dy * dy) || 1;
          if (dist < 260) {
            let force = (260 - dist) / dist * 0.15;
            a.x -= dx * force;
            a.y -= dy * force;
            b.x += dx * force;
            b.y += dy * force;
          }
        }
      }

      // Attraction along edges
      for (const edge of this.edges) {
        const source = this.nodeMap.get(edge.source);
        const target = this.nodeMap.get(edge.target);
        if (!source || !target) continue;
        let dx = target.x - source.x;
        let dy = target.y - source.y;
        let dist = Math.sqrt(dx * dx + dy * dy) || 1;
        let force = (dist - 120) * 0.04;
        source.x += dx / dist * force;
        source.y += dy / dist * force;
        target.x -= dx / dist * force;
        target.y -= dy / dist * force;
      }
    }
  }

  getColor(type) {
    switch (type) {
      case "project": return "#38bdf8"; // Cyan
      case "idea": return "#a78bfa"; // Violet
      case "experiment": return "#fbbf24"; // Amber
      case "decision": return "#34d399"; // Emerald
      case "research": return "#f87171"; // Rose
      case "learning": return "#818cf8"; // Indigo
      case "opportunity": return "#f59e0b"; // Golden
      default: return "#94a3b8";
    }
  }

  render() {
    this.linksGroup.innerHTML = "";
    this.nodesGroup.innerHTML = "";

    const visibleNodes = this.nodes.filter(n => this.activeTypeFilter === "all" || n.type === this.activeTypeFilter);
    const visibleNodeIds = new Set(visibleNodes.map(n => n.id));

    // Render Edges
    for (const edge of this.edges) {
      if (!visibleNodeIds.has(edge.source) || !visibleNodeIds.has(edge.target)) continue;
      const s = this.nodeMap.get(edge.source);
      const t = this.nodeMap.get(edge.target);
      if (!s || !t) continue;

      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", s.x);
      line.setAttribute("y1", s.y);
      line.setAttribute("x2", t.x);
      line.setAttribute("y2", t.y);
      line.setAttribute("stroke", "#334155");
      line.setAttribute("stroke-width", "1.5");
      line.setAttribute("stroke-dasharray", edge.relation === "validates" ? "4,4" : "none");
      line.setAttribute("marker-end", "url(#arrow)");
      line.classList.add("kg-edge");
      this.linksGroup.appendChild(line);
    }

    // Render Nodes
    for (const node of visibleNodes) {
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("transform", `translate(${node.x}, ${node.y})`);
      g.classList.add("kg-node");
      g.style.cursor = "pointer";

      const color = this.getColor(node.type);

      // Node Circle
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("r", node.type === "project" ? "18" : "14");
      circle.setAttribute("fill", "#111827");
      circle.setAttribute("stroke", color);
      circle.setAttribute("stroke-width", "2.5");
      circle.setAttribute("filter", "url(#glow)");
      g.appendChild(circle);

      // Type Initial Icon
      const textIcon = document.createElementNS("http://www.w3.org/2000/svg", "text");
      textIcon.setAttribute("text-anchor", "middle");
      textIcon.setAttribute("dy", "4");
      textIcon.setAttribute("fill", color);
      textIcon.setAttribute("font-size", "11px");
      textIcon.setAttribute("font-weight", "700");
      textIcon.setAttribute("font-family", "monospace");
      textIcon.textContent = node.type.charAt(0).toUpperCase();
      g.appendChild(textIcon);

      // Node Label
      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("text-anchor", "middle");
      label.setAttribute("dy", node.type === "project" ? "32" : "28");
      label.setAttribute("fill", "#e2e8f0");
      label.setAttribute("font-size", "11px");
      label.setAttribute("font-weight", "500");
      const shortLabel = node.label.length > 24 ? node.label.substring(0, 22) + "..." : node.label;
      label.textContent = shortLabel;
      g.appendChild(label);

      // Subtitle
      if (node.subtitle) {
        const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
        sub.setAttribute("text-anchor", "middle");
        sub.setAttribute("dy", node.type === "project" ? "44" : "40");
        sub.setAttribute("fill", "#64748b");
        sub.setAttribute("font-size", "9px");
        sub.textContent = node.subtitle;
        g.appendChild(sub);
      }

      // Interaction
      g.addEventListener("click", () => {
        if (this.options.onNodeClick) {
          this.options.onNodeClick(node);
        }
      });

      this.nodesGroup.appendChild(g);
    }
  }
}
