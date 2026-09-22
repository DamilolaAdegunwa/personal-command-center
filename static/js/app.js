// Personal Command Center - Main Application Controller

let activeView = "today";
let kgInstance = null;
let currentSearchQuery = "";
let searchDebounceTimer = null;

// Toast Utility
function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${type === "error" ? "⚠️" : "✨"}</span> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 200);
  }, 3500);
}

// Live Clock
function startClock() {
  const clockEl = document.getElementById("live-clock-time");
  function tick() {
    const now = new Date();
    const utcStr = now.toUTCString().replace("GMT", "UTC");
    const localStr = now.toLocaleTimeString();
    if (clockEl) {
      clockEl.textContent = `${localStr} (Local) • ${now.toISOString().substring(11, 19)} UTC`;
    }
  }
  tick();
  setInterval(tick, 1000);
}

// Navigation View Switcher
function switchView(viewName) {
  activeView = viewName;
  document.querySelectorAll(".nav-item").forEach(item => {
    item.classList.toggle("active", item.getAttribute("data-view") === viewName);
  });
  document.querySelectorAll(".view-container").forEach(view => {
    view.classList.toggle("active", view.id === `view-${viewName}`);
  });

  // Load view-specific data
  switch (viewName) {
    case "today": loadTodayView(); break;
    case "projects": loadProjectsView(); break;
    case "ideas": loadIdeasView(); break;
    case "experiments": loadExperimentsView(); break;
    case "decisions": loadDecisionsView(); break;
    case "research": loadResearchView(); break;
    case "learning": loadLearningView(); break;
    case "opportunities": loadOpportunitiesView(); break;
    case "graph": loadGraphView(); break;
    case "search": loadSearchView(); break;
    case "ai_studio": loadAIStudioView(); break;
    case "metrics": loadMetricsView(); break;
  }
}

// Update Top Badge Counts
async function refreshNavBadges() {
  try {
    const todayData = await API.getToday();
    const metrics = await API.getMetrics();

    const p0Badge = document.getElementById("badge-p0-count");
    if (p0Badge) {
      p0Badge.textContent = todayData.summary.p0_count;
      p0Badge.classList.toggle("alert", todayData.summary.p0_count > 0);
    }

    const projectsBadge = document.getElementById("badge-projects-count");
    if (projectsBadge) projectsBadge.textContent = metrics.active_projects;

    const ideasBadge = document.getElementById("badge-ideas-count");
    if (ideasBadge) ideasBadge.textContent = metrics.ideas_in_flight;

    const blockedBadge = document.getElementById("badge-blocked-count");
    if (blockedBadge) {
      blockedBadge.textContent = todayData.summary.blocked_count;
      blockedBadge.classList.toggle("alert", todayData.summary.blocked_count > 0);
    }
  } catch (e) {
    console.error("Failed to refresh badges:", e);
  }
}

// --- 1. TODAY COCKPIT ---
async function loadTodayView() {
  const container = document.getElementById("today-content");
  if (!container) return;
  container.innerHTML = `<div style="color:var(--text-muted); padding:20px;">Synthesizing situational posture...</div>`;

  try {
    const data = await API.getToday();
    refreshNavBadges();

    let html = `
      <div class="hud-grid-4">
        <div class="hud-card hud-card-accent-rose">
          <div class="hud-card-header">Critical Fire Drills (P0)</div>
          <div class="hud-card-value">${data.critical_p0.length}</div>
          <div class="hud-card-sub">Immediate intervention required</div>
        </div>
        <div class="hud-card hud-card-accent-amber">
          <div class="hud-card-header">Blocked Items</div>
          <div class="hud-card-value">${data.blocked_items.length}</div>
          <div class="hud-card-sub">Dependency stalls identified</div>
        </div>
        <div class="hud-card hud-card-accent-cyan">
          <div class="hud-card-header">Active Projects</div>
          <div class="hud-card-value">${data.active_projects.length}</div>
          <div class="hud-card-sub">In-flight strategic initiatives</div>
        </div>
        <div class="hud-card hud-card-accent-emerald">
          <div class="hud-card-header">Unfinished Work Units</div>
          <div class="hud-card-value">${data.summary.unfinished_total}</div>
          <div class="hud-card-sub">Scheduled backlog items</div>
        </div>
      </div>

      <div class="cockpit-grid">
        <div>
          <!-- Immediate Action Center -->
          <div class="panel">
            <div class="panel-title">
              <span>🎯 High-Priority Tactical Tasks</span>
              <button class="btn btn-ghost btn-sm" onclick="openQuickCapture('task')">+ New Task</button>
            </div>
            <div id="today-tasks-list">
    `;

    const allPriorityTasks = [...data.critical_p0, ...data.high_priority_p1];
    if (allPriorityTasks.length === 0) {
      html += `<div style="color:var(--text-dim); padding:10px;">Zero critical or high priority tasks currently pending.</div>`;
    } else {
      for (const t of allPriorityTasks) {
        html += renderTaskCard(t);
      }
    }

    html += `
            </div>
          </div>

          <!-- Active Deadlines -->
          <div class="panel">
            <div class="panel-title">
              <span>⏰ Approaching Deadlines</span>
            </div>
            <div id="today-deadlines-list">
    `;

    if (data.upcoming_deadlines.length === 0) {
      html += `<div style="color:var(--text-dim); padding:10px;">No critical upcoming deadlines in active buffer.</div>`;
    } else {
      for (const d of data.upcoming_deadlines) {
        html += renderTaskCard(d);
      }
    }

    html += `
            </div>
          </div>
        </div>

        <!-- Right Side: Grounded AI Tactical Briefing Callout & Blockers -->
        <div>
          <div class="panel" style="border: 1px solid var(--violet);">
            <div class="panel-title" style="color: var(--violet);">
              <span>⚡ AI Tactical Briefing</span>
              <button class="btn btn-ai btn-sm" onclick="triggerDailyBriefing()">Full Briefing (B)</button>
            </div>
            <div style="font-size:12px; color:var(--text-muted); line-height:1.5;">
              <p>Situational engine analyzes P0 fire drills, blocked dependency chains, and active target dates.</p>
              <div style="margin-top:10px; display:flex; flex-direction:column; gap:6px;">
                <button class="btn btn-ghost btn-sm" style="text-align:left; justify-content:flex-start;" onclick="triggerDailyBriefing()">
                  🛰️ Run Grounded Morning Briefing
                </button>
                <button class="btn btn-ghost btn-sm" style="text-align:left; justify-content:flex-start;" onclick="triggerWeeklyReview()">
                  📊 Run Weekly Operational Review
                </button>
              </div>
            </div>
          </div>

          <div class="panel">
            <div class="panel-title">
              <span>🚫 Active Blockers</span>
            </div>
    `;

    if (data.blocked_items.length === 0) {
      html += `<div style="color:var(--text-dim); padding:10px;">No blocked items. Velocity unconstrained.</div>`;
    } else {
      for (const b of data.blocked_items) {
        html += `
          <div class="item-card priority-p0">
            <div class="card-title">${b.title}</div>
            <div class="card-desc" style="color:var(--rose);">⚠️ Blocker: ${b.blocker_reason || 'Unspecified dependency stall'}</div>
            <div class="card-actions">
              <button class="btn btn-ghost btn-sm" onclick="resolveBlocker('${b.id}')">Unblock</button>
            </div>
          </div>
        `;
      }
    }

    html += `
          </div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose); padding:20px;">Failed to load situational dashboard: ${err.message}</div>`;
  }
}

function renderTaskCard(t) {
  const isDone = t.status === "completed";
  const pClass = `priority-${t.priority.replace('_critical', '').replace('_high', '').replace('_medium', '').replace('_low', '')}`;
  const badgeClass = `badge-${t.priority.split('_')[0]}`;
  
  return `
    <div class="item-card ${pClass}">
      <div class="card-top">
        <div style="display:flex; align-items:center; gap:8px;">
          <input type="checkbox" ${isDone ? "checked" : ""} onchange="toggleTaskDone('${t.id}', this.checked)" style="cursor:pointer;" />
          <span class="card-title" style="${isDone ? 'text-decoration:line-through; color:var(--text-dim);' : ''}">${t.title}</span>
        </div>
        <span class="badge ${badgeClass}">${t.priority.replace('_', ' ')}</span>
      </div>
      <div class="card-meta">
        ${t.deadline ? `<span>📅 ${t.deadline.substring(0, 10)}</span>` : ''}
        <span>⚡ ${t.energy_level.replace('_', ' ')}</span>
        <span>Status: ${t.status}</span>
        ${t.tags && t.tags.length ? t.tags.map(tag => `<span class="badge badge-p3">#${tag}</span>`).join(' ') : ''}
      </div>
      ${t.blocker_reason ? `<div class="card-desc" style="color:var(--rose);">⚠️ ${t.blocker_reason}</div>` : ''}
    </div>
  `;
}

async function toggleTaskDone(taskId, completed) {
  try {
    await API.updateTask(taskId, { status: completed ? "completed" : "todo" });
    showToast(completed ? "Task marked complete." : "Task reopened.");
    loadTodayView();
  } catch (e) {
    console.error(e);
  }
}

async function resolveBlocker(taskId) {
  try {
    await API.updateTask(taskId, { status: "in_progress", blocker_reason: null });
    showToast("Blocker cleared. Moved to in-progress.");
    loadTodayView();
  } catch (e) {
    console.error(e);
  }
}

// --- 2. PROJECTS VIEW ---
async function loadProjectsView() {
  const container = document.getElementById("projects-content");
  if (!container) return;

  try {
    const projects = await API.getProjects();
    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="color:var(--text-muted); font-size:12px;">Tracking ${projects.length} Strategic Initiatives</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('project')">+ New Project</button>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap:16px;">
    `;

    for (const p of projects) {
      const healthBadge = `badge-${p.health}`;
      html += `
        <div class="panel" style="margin-bottom:0; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
              <span class="badge ${healthBadge}">HEALTH: ${p.health.toUpperCase()}</span>
              <span class="badge badge-p3">${p.category}</span>
            </div>
            <h3 style="font-size:15px; font-weight:700; margin-bottom:6px; color:var(--text-main);">${p.title}</h3>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.4; margin-bottom:12px;">${p.description || 'No description provided.'}</p>
            
            <div style="display:flex; justify-content:space-between; font-size:11px; font-family:var(--font-mono); color:var(--text-dim); margin-bottom:4px;">
              <span>PROGRESS</span>
              <span>${p.progress_pct}%</span>
            </div>
            <div class="progress-container">
              <div class="progress-bar ${p.health}" style="width: ${p.progress_pct}%"></div>
            </div>

            ${p.next_actions && p.next_actions.length ? `
              <div style="margin-top:12px; background:var(--bg-surface-elevated); padding:8px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
                <div style="font-size:10px; font-weight:700; color:var(--text-dim); text-transform:uppercase; margin-bottom:4px;">Next Action</div>
                <div style="font-size:12px; color:var(--text-main); font-weight:500;">👉 ${p.next_actions[0]}</div>
              </div>
            ` : ''}
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:10px; border-top:1px solid var(--border-subtle); font-size:11px; color:var(--text-muted);">
            <span>Target: ${p.target_date || 'No target date'}</span>
            <div style="display:flex; gap:6px;">
              <button class="btn btn-ai btn-sm" onclick="runProjectDiagnostic('${p.id}')">Audit AI</button>
            </div>
          </div>
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading projects: ${err.message}</div>`;
  }
}

// --- 3. IDEAS VIEW (KANBAN PIPELINE) ---
async function loadIdeasView() {
  const container = document.getElementById("ideas-content");
  if (!container) return;

  try {
    const ideas = await API.getIdeas();
    const stages = ["captured", "explored", "validated", "planned", "executing", "completed", "abandoned"];

    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="color:var(--text-muted); font-size:12px;">Idea-to-Execution Stage Machine (${ideas.length} total concepts)</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('idea')">+ Capture Idea</button>
      </div>
      <div class="kanban-grid">
    `;

    for (const stage of stages) {
      const stageIdeas = ideas.filter(i => i.status === stage);
      html += `
        <div class="kanban-lane">
          <div class="kanban-lane-header">
            <span>${stage}</span>
            <span class="badge badge-p3">${stageIdeas.length}</span>
          </div>
          <div class="kanban-lane-items">
      `;

      for (const i of stageIdeas) {
        html += `
          <div class="item-card" style="margin-bottom:0;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
              <span class="badge badge-p3">${i.category}</span>
              <span class="badge badge-${i.priority === 'high' ? 'p1' : 'p2'}">${i.priority}</span>
            </div>
            <div class="card-title" style="margin-bottom:6px;">${i.title}</div>
            <div class="card-desc" style="font-size:11px;">${i.description ? i.description.substring(0, 90) + '...' : ''}</div>
            ${i.next_action ? `<div style="margin-top:6px; font-size:11px; color:var(--cyan);">Next: ${i.next_action}</div>` : ''}
            
            <div class="card-actions" style="justify-content:space-between;">
              <select onchange="changeIdeaStage('${i.id}', this.value)" style="font-size:10px; background:var(--bg-base); color:var(--text-muted); border:1px solid var(--border-subtle); border-radius:3px; padding:2px;">
                ${stages.map(s => `<option value="${s}" ${s === i.status ? 'selected' : ''}>${s}</option>`).join('')}
              </select>
              <button class="btn btn-ai btn-sm" style="padding:2px 6px; font-size:10px;" onclick="runIdeaStressTest('${i.id}')">Stress Test</button>
            </div>
          </div>
        `;
      }

      html += `
          </div>
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading ideas: ${err.message}</div>`;
  }
}

async function changeIdeaStage(ideaId, newStatus) {
  try {
    await API.transitionIdea(ideaId, newStatus);
    showToast(`Idea transitioned to '${newStatus}'`);
    loadIdeasView();
  } catch (e) {
    console.error(e);
  }
}

// --- 4. EXPERIMENTS VIEW ---
async function loadExperimentsView() {
  const container = document.getElementById("experiments-content");
  if (!container) return;

  try {
    const exps = await API.getExperiments();
    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="color:var(--text-muted); font-size:12px;">Scientific Validation Engine: Idea ➔ Hypothesis ➔ Evidence ➔ Decision</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('experiment')">+ New Experiment</button>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap:16px;">
    `;

    for (const e of exps) {
      const isConcluded = e.status === "concluded";
      html += `
        <div class="panel" style="margin-bottom:0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge ${isConcluded ? 'badge-green' : 'badge-amber'}">STATUS: ${e.status.toUpperCase()}</span>
            <span style="font-size:11px; color:var(--text-dim);">${e.created_at.substring(0, 10)}</span>
          </div>
          <h3 style="font-size:15px; font-weight:700; margin-bottom:10px; color:var(--text-main);">${e.title}</h3>
          
          <div style="background:var(--bg-base); padding:10px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); margin-bottom:10px;">
            <div style="font-size:10px; font-weight:700; color:var(--cyan); text-transform:uppercase;">Hypothesis</div>
            <div style="font-size:12px; color:var(--text-main); line-height:1.4; margin-top:2px;">${e.hypothesis}</div>
          </div>

          <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">
            <strong>Objective:</strong> ${e.objective}
          </div>

          ${e.actual_result ? `
            <div style="background:var(--emerald-dim); border:1px solid rgba(52, 211, 153, 0.3); padding:10px; border-radius:var(--radius-sm); margin-bottom:10px;">
              <div style="font-size:10px; font-weight:700; color:var(--emerald); text-transform:uppercase;">Empirical Evidence & Result</div>
              <div style="font-size:12px; color:var(--text-main); line-height:1.4; margin-top:2px;">${e.actual_result}</div>
              ${e.evidence ? `<div style="font-size:11px; color:var(--text-dim); margin-top:4px;">Log: ${e.evidence}</div>` : ''}
            </div>
          ` : ''}

          ${e.conclusion ? `
            <div style="font-size:12px; color:var(--text-main); margin-bottom:8px;">
              <strong>Conclusion:</strong> ${e.conclusion}
            </div>
          ` : ''}

          <div style="margin-top:12px; padding-top:8px; border-top:1px solid var(--border-subtle); font-size:11px; color:var(--text-dim);">
            Next Step: ${e.next_step || 'Awaiting test completion'}
          </div>
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading experiments: ${err.message}</div>`;
  }
}

// --- 5. DECISIONS LOG (DECISION INTELLIGENCE) ---
async function loadDecisionsView() {
  const container = document.getElementById("decisions-content");
  if (!container) return;

  try {
    const decisions = await API.getDecisions();
    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="color:var(--text-muted); font-size:12px;">Decision Intelligence Journal: "What decisions have I made and what happened after?"</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('decision')">+ Record Decision</button>
      </div>
      <div style="display:flex; flex-direction:column; gap:14px;">
    `;

    for (const d of decisions) {
      const isReviewed = d.status === "reviewed";
      html += `
        <div class="panel" style="margin-bottom:0;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="badge ${isReviewed ? 'badge-green' : 'badge-amber'}">${d.status.toUpperCase()}</span>
              <span class="badge badge-cyan">Confidence: ${d.confidence_level}%</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:11px; font-family:var(--font-mono); color:var(--text-dim);">Date: ${d.date}</span>
              <button class="btn btn-ai btn-sm" onclick="runDecisionAudit('${d.id}')">Audit Outcome</button>
            </div>
          </div>

          <h3 style="font-size:16px; font-weight:700; color:var(--text-main); margin-bottom:8px;">${d.title}</h3>
          
          <div style="font-size:12px; color:var(--text-muted); line-height:1.5; margin-bottom:12px;">
            <strong>Context:</strong> ${d.context}
          </div>

          ${d.alternatives_considered && d.alternatives_considered.length ? `
            <div style="margin-bottom:12px; background:var(--bg-base); padding:10px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
              <div style="font-size:10px; font-weight:700; color:var(--text-dim); text-transform:uppercase; margin-bottom:6px;">Alternatives Considered</div>
              <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:8px;">
                ${d.alternatives_considered.map(alt => `
                  <div style="font-size:11px; padding:6px; background:var(--bg-surface); border-radius:4px;">
                    <div style="font-weight:600; color:var(--text-main);">${alt.option}</div>
                    <div style="color:var(--emerald);">+ ${alt.pros}</div>
                    <div style="color:var(--rose);">- ${alt.cons}</div>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:12px; margin-bottom:10px;">
            <div>
              <span style="color:var(--amber); font-weight:600;">Assumptions:</span>
              <p style="color:var(--text-muted); margin-top:2px;">${d.assumptions}</p>
            </div>
            <div>
              <span style="color:var(--cyan); font-weight:600;">Evidence Base:</span>
              <p style="color:var(--text-muted); margin-top:2px;">${d.evidence}</p>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:12px; background:var(--bg-surface-elevated); padding:10px; border-radius:var(--radius-sm);">
            <div>
              <span style="color:var(--text-main); font-weight:600;">Expected Outcome:</span>
              <p style="color:var(--text-muted); margin-top:2px;">${d.expected_outcome}</p>
            </div>
            <div>
              <span style="color:var(--emerald); font-weight:600;">Actual Outcome:</span>
              <p style="color:var(--text-main); margin-top:2px;">${d.actual_outcome || 'Pending verification review'}</p>
            </div>
          </div>

          ${d.lessons_learned ? `
            <div style="margin-top:10px; font-size:12px; color:var(--violet);">
              <strong>Lessons Learned:</strong> ${d.lessons_learned}
            </div>
          ` : ''}
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading decisions: ${err.message}</div>`;
  }
}

// --- 6. RESEARCH VIEW ---
async function loadResearchView() {
  const container = document.getElementById("research-content");
  if (!container) return;

  try {
    const research = await API.getResearch();
    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="color:var(--text-muted); font-size:12px;">Deep Research Dossiers (${research.length} active investigations)</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('research')">+ New Investigation</button>
      </div>
      <div style="display:flex; flex-direction:column; gap:14px;">
    `;

    for (const r of research) {
      html += `
        <div class="panel" style="margin-bottom:0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="display:flex; gap:8px;">
              <span class="badge badge-rose">TOPIC: ${r.topic}</span>
              <span class="badge badge-p3">${r.status.toUpperCase()}</span>
            </div>
            <span style="font-size:11px; color:var(--text-dim);">${r.created_at.substring(0, 10)}</span>
          </div>

          <h3 style="font-size:16px; font-weight:700; color:var(--text-main); margin-bottom:10px;">${r.research_question}</h3>
          
          <div style="font-size:12px; color:var(--text-muted); line-height:1.5; margin-bottom:12px;">
            <strong>Investigation:</strong> ${r.investigations}
          </div>

          ${r.findings && r.findings.length ? `
            <div style="background:var(--bg-base); padding:10px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); margin-bottom:10px;">
              <div style="font-size:10px; font-weight:700; color:var(--emerald); text-transform:uppercase; margin-bottom:6px;">Verified Findings</div>
              ${r.findings.map(f => `
                <div style="font-size:12px; margin-bottom:6px; line-height:1.4;">
                  <span style="color:var(--emerald);">✔</span> <strong>${f.claim}</strong>
                  ${f.evidence ? `<div style="font-size:11px; color:var(--text-dim); margin-left:14px;">Evidence: ${f.evidence}</div>` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${r.sources && r.sources.length ? `
            <div style="font-size:11px; color:var(--text-dim); margin-bottom:8px;">
              <strong>Sources:</strong> ${r.sources.map(s => `${s.title} (${s.url_or_citation})`).join(' • ')}
            </div>
          ` : ''}

          ${r.conclusions ? `
            <div style="font-size:12px; color:var(--text-main); margin-bottom:8px;">
              <strong>Conclusions:</strong> ${r.conclusions}
            </div>
          ` : ''}

          ${r.unresolved_questions && r.unresolved_questions.length ? `
            <div style="font-size:11px; color:var(--amber); margin-top:8px;">
              <strong>Unresolved Questions:</strong> ${r.unresolved_questions.join(' • ')}
            </div>
          ` : ''}
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading research: ${err.message}</div>`;
  }
}

// --- 7. LEARNING VIEW ---
async function loadLearningView() {
  const container = document.getElementById("learning-content");
  if (!container) return;

  try {
    const items = await API.getLearning();
    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="color:var(--text-muted); font-size:12px;">Curriculum & Practical Skill Mastery (${items.length} tracks)</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('learning')">+ New Learning Track</button>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap:16px;">
    `;

    for (const l of items) {
      html += `
        <div class="panel" style="margin-bottom:0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span class="badge badge-violet">${l.subject}</span>
            <span class="badge badge-p3">${l.type.toUpperCase()}</span>
          </div>

          <h3 style="font-size:15px; font-weight:700; color:var(--text-main); margin-bottom:6px;">${l.title}</h3>
          
          <div style="display:flex; justify-content:space-between; font-size:11px; font-family:var(--font-mono); color:var(--text-dim); margin-bottom:4px;">
            <span>MASTERY PROGRESS</span>
            <span>${l.progress_pct}%</span>
          </div>
          <div class="progress-container">
            <div class="progress-bar" style="width: ${l.progress_pct}%; background-color: var(--violet);"></div>
          </div>

          <p style="font-size:12px; color:var(--text-muted); line-height:1.4; margin:10px 0;">${l.notes || ''}</p>

          ${l.practical_exercises && l.practical_exercises.length ? `
            <div style="background:var(--bg-base); padding:8px 10px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); margin-bottom:10px;">
              <div style="font-size:10px; font-weight:700; color:var(--text-dim); text-transform:uppercase; margin-bottom:4px;">Practical Exercises</div>
              ${l.practical_exercises.map(ex => `
                <div style="font-size:11px; display:flex; align-items:center; gap:6px; margin-bottom:2px;">
                  <span style="color:${ex.completed ? 'var(--emerald)' : 'var(--text-dim)'};">${ex.completed ? '✓' : '○'}</span>
                  <span style="${ex.completed ? 'color:var(--text-muted); text-decoration:line-through;' : 'color:var(--text-main);'}">${ex.title}</span>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${l.key_takeaways ? `
            <div style="font-size:11px; color:var(--cyan); margin-top:8px;">
              <strong>Key Takeaway:</strong> ${l.key_takeaways}
            </div>
          ` : ''}
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading learning items: ${err.message}</div>`;
  }
}

// --- 8. OPPORTUNITY RADAR ---
async function loadOpportunitiesView() {
  const container = document.getElementById("opportunities-content");
  if (!container) return;

  try {
    const opps = await API.getOpportunities();
    let html = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="color:var(--text-muted); font-size:12px;">Opportunity Radar: Discover, Evaluate, and Pursue Asymmetric Opportunities</div>
        <button class="btn btn-primary btn-sm" onclick="openQuickCapture('opportunity')">+ New Opportunity</button>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap:16px;">
    `;

    for (const o of opps) {
      const isPursuing = o.status === "pursuing";
      html += `
        <div class="panel" style="margin-bottom:0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge ${isPursuing ? 'badge-green' : 'badge-amber'}">${o.status.toUpperCase()}</span>
            <span class="badge badge-p3">${o.category.replace('_', ' ').toUpperCase()}</span>
          </div>

          <h3 style="font-size:15px; font-weight:700; color:var(--text-main); margin-bottom:8px;">${o.title}</h3>
          <p style="font-size:12px; color:var(--text-muted); line-height:1.4; margin-bottom:10px;">${o.description || ''}</p>

          <div style="background:var(--bg-base); padding:8px 10px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); margin-bottom:8px;">
            <div style="font-size:10px; font-weight:700; color:var(--emerald); text-transform:uppercase;">Potential Upside</div>
            <div style="font-size:12px; color:var(--text-main); margin-top:2px;">${o.potential_upside}</div>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; font-size:11px; margin-bottom:8px;">
            <div>
              <span style="color:var(--text-dim); font-weight:600;">Requirements:</span>
              <p style="color:var(--text-muted);">${o.requirements}</p>
            </div>
            <div>
              <span style="color:var(--rose); font-weight:600;">Risks:</span>
              <p style="color:var(--text-muted);">${o.risks}</p>
            </div>
          </div>

          <div style="margin-top:10px; padding-top:8px; border-top:1px solid var(--border-subtle); font-size:11px; color:var(--cyan);">
            👉 Next Action: ${o.next_action || 'Pending evaluation'}
          </div>
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading opportunities: ${err.message}</div>`;
  }
}

// --- 9. KNOWLEDGE GRAPH VIEW ---
async function loadGraphView() {
  const container = document.getElementById("kg-canvas-container");
  if (!container) return;

  if (!kgInstance) {
    kgInstance = new KnowledgeGraph("kg-canvas-container", {
      onNodeClick: (node) => {
        showGraphNodeDetails(node);
      }
    });
  }

  try {
    const data = await API.getGraph();
    kgInstance.setData(data);
  } catch (err) {
    console.error("Error loading graph data:", err);
  }
}

function showGraphNodeDetails(node) {
  const inspector = document.getElementById("graph-node-inspector");
  if (!inspector) return;
  inspector.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
      <span class="badge badge-cyan">${node.type.toUpperCase()}</span>
      <button class="modal-close" onclick="document.getElementById('graph-node-inspector').classList.remove('open')">✕</button>
    </div>
    <h3 style="font-size:14px; font-weight:700; color:var(--text-main); margin-bottom:8px;">${node.label}</h3>
    <div style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">${node.subtitle || ''}</div>
    <div style="font-size:12px; color:var(--text-muted); line-height:1.4;">
      ${JSON.stringify(node.data, null, 2)}
    </div>
  `;
  inspector.classList.add("open");
}

function filterGraphNodes(type) {
  if (kgInstance) {
    kgInstance.setTypeFilter(type);
  }
}

// --- 10. UNIVERSAL OMNI-SEARCH ---
function openSearchModal() {
  const modal = document.getElementById("search-modal");
  if (modal) {
    modal.classList.add("active");
    const input = document.getElementById("omni-search-input");
    if (input) {
      input.focus();
      input.select();
    }
  }
}

function closeSearchModal() {
  const modal = document.getElementById("search-modal");
  if (modal) modal.classList.remove("active");
}

async function handleOmniSearchInput(query) {
  currentSearchQuery = query;
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(async () => {
    const resultsContainer = document.getElementById("omni-search-results");
    if (!resultsContainer) return;

    if (!query.trim()) {
      resultsContainer.innerHTML = `<div style="color:var(--text-dim); padding:20px; text-align:center;">Type keywords to search across projects, ideas, research, decisions, tasks, learning, and opportunities...</div>`;
      return;
    }

    try {
      const results = await API.search({ q: query, limit: 30 });
      if (results.length === 0) {
        resultsContainer.innerHTML = `<div style="color:var(--text-dim); padding:20px; text-align:center;">No matching items found for "${query}".</div>`;
        return;
      }

      let html = `<div class="search-results-list">`;
      for (const item of results) {
        html += `
          <div class="search-result-row" onclick="handleSearchResultClick('${item.entity_type}', '${item.id}')">
            <div>
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span class="badge badge-p2">${item.entity_type.toUpperCase()}</span>
                <span style="font-weight:600; font-size:13px; color:var(--text-main);">${item.title}</span>
              </div>
              <div style="font-size:11px; color:var(--text-muted);">${item.snippet}</div>
            </div>
            <div style="font-size:11px; font-family:var(--font-mono); color:var(--text-dim);">
              ${item.date || ''}
            </div>
          </div>
        `;
      }
      html += `</div>`;
      resultsContainer.innerHTML = html;
    } catch (err) {
      resultsContainer.innerHTML = `<div style="color:var(--rose); padding:10px;">Search error: ${err.message}</div>`;
    }
  }, 180);
}

function handleSearchResultClick(type, id) {
  closeSearchModal();
  switch (type) {
    case "project": switchView("projects"); break;
    case "idea": switchView("ideas"); break;
    case "experiment": switchView("experiments"); break;
    case "decision": switchView("decisions"); break;
    case "research": switchView("research"); break;
    case "learning": switchView("learning"); break;
    case "opportunity": switchView("opportunities"); break;
    case "task": switchView("today"); break;
  }
}

// --- 11. AI INTELLIGENCE STUDIO ---
async function triggerDailyBriefing() {
  openAIModal("Daily Briefing", "Generating grounded situational briefing from SQLite records...");
  try {
    const res = await API.getDailyBriefing();
    renderAIModalContent(res.content);
  } catch (err) {
    renderAIModalContent(`Error generating briefing: ${err.message}`);
  }
}

async function triggerWeeklyReview() {
  openAIModal("Weekly Operational Retrospective", "Synthesizing accomplishments, blocked work, and learning pace...");
  try {
    const res = await API.getWeeklyReview();
    renderAIModalContent(res.content);
  } catch (err) {
    renderAIModalContent(`Error generating review: ${err.message}`);
  }
}

async function runProjectDiagnostic(projectId) {
  openAIModal("Project Diagnostic Audit", "Analyzing project health, dependencies, and gaps...");
  try {
    const res = await API.analyzeProject(projectId);
    renderAIModalContent(res.content);
  } catch (err) {
    renderAIModalContent(`Error auditing project: ${err.message}`);
  }
}

async function runIdeaStressTest(ideaId) {
  openAIModal("Idea Adversarial Stress-Test", "Evaluating value proposition, hidden assumptions, and validation tests...");
  try {
    const res = await API.analyzeIdea(ideaId);
    renderAIModalContent(res.content);
  } catch (err) {
    renderAIModalContent(`Error stress-testing idea: ${err.message}`);
  }
}

async function runDecisionAudit(decisionId) {
  openAIModal("Decision Retrospective Audit", "Auditing confidence calibration, expected vs actual outcome...");
  try {
    const res = await API.reviewDecision(decisionId);
    renderAIModalContent(res.content);
  } catch (err) {
    renderAIModalContent(`Error auditing decision: ${err.message}`);
  }
}

function openAIModal(title, initialStatus) {
  const modal = document.getElementById("ai-modal");
  const titleEl = document.getElementById("ai-modal-title");
  const contentEl = document.getElementById("ai-modal-content");
  if (!modal || !contentEl) return;

  titleEl.textContent = title;
  contentEl.innerHTML = `<div style="color:var(--text-muted); display:flex; align-items:center; gap:8px;"><span>⚡</span> ${initialStatus}</div>`;
  modal.classList.add("active");
}

function renderAIModalContent(markdownText) {
  const contentEl = document.getElementById("ai-modal-content");
  if (!contentEl) return;

  // Highlight ground-truth bracket tags
  let formatted = markdownText
    .replace(/\[FACT\]/g, `<span class="tag-fact">[FACT]</span>`)
    .replace(/\[USER CONTEXT\]/g, `<span class="tag-user-context">[USER CONTEXT]</span>`)
    .replace(/\[ASSUMPTION\]/g, `<span class="tag-assumption">[ASSUMPTION]</span>`)
    .replace(/\[AI RECOMMENDATION\]/g, `<span class="tag-ai-rec">[AI RECOMMENDATION]</span>`);

  contentEl.innerHTML = formatted;
}

function closeAIModal() {
  const modal = document.getElementById("ai-modal");
  if (modal) modal.classList.remove("active");
}

// --- 12. SITUATIONAL METRICS VIEW ---
async function loadMetricsView() {
  const container = document.getElementById("metrics-content");
  if (!container) return;

  try {
    const m = await API.getMetrics();
    let html = `
      <div class="hud-grid-4">
        <div class="hud-card hud-card-accent-cyan">
          <div class="hud-card-header">Active Projects</div>
          <div class="hud-card-value">${m.active_projects} <span style="font-size:12px; color:var(--emerald);">(${m.completed_projects} done)</span></div>
          <div class="hud-card-sub">Stalled (>14d): ${m.stalled_projects}</div>
        </div>
        <div class="hud-card hud-card-accent-violet">
          <div class="hud-card-header">Idea Conversion</div>
          <div class="hud-card-value">${m.ideas_validated} <span style="font-size:12px; color:var(--text-dim);">/ ${m.ideas_captured}</span></div>
          <div class="hud-card-sub">In flight: ${m.ideas_in_flight}</div>
        </div>
        <div class="hud-card hud-card-accent-emerald">
          <div class="hud-card-header">Decision Calibration</div>
          <div class="hud-card-value">${m.decisions_logged}</div>
          <div class="hud-card-sub">Pending review: ${m.decisions_pending_review}</div>
        </div>
        <div class="hud-card hud-card-accent-amber">
          <div class="hud-card-header">Active Experiments</div>
          <div class="hud-card-value">${m.experiments_running}</div>
          <div class="hud-card-sub">Concluded: ${m.experiments_concluded}</div>
        </div>
      </div>

      <div class="cockpit-grid">
        <div class="panel">
          <div class="panel-title">
            <span>🚨 Stagnation & Blocker Radar</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px;">
    `;

    if (m.stagnation_alerts.length === 0) {
      html += `<div style="color:var(--text-dim); padding:10px;">Zero stagnation alerts. All initiatives progressing within healthy bounds.</div>`;
    } else {
      for (const alert of m.stagnation_alerts) {
        html += `
          <div class="item-card priority-p0">
            <div class="card-title">${alert.title}</div>
            <div class="card-desc" style="color:var(--amber);">${alert.reason}</div>
          </div>
        `;
      }
    }

    html += `
          </div>
        </div>

        <div class="panel">
          <div class="panel-title">
            <span>📊 Health Breakdown</span>
          </div>
          <div style="font-size:13px; line-height:2;">
            <div style="display:flex; justify-content:space-between;"><span style="color:var(--emerald);">● Healthy (Green):</span> <strong>${m.project_health_breakdown.green || 0}</strong></div>
            <div style="display:flex; justify-content:space-between;"><span style="color:var(--amber);">● Attention (Yellow):</span> <strong>${m.project_health_breakdown.yellow || 0}</strong></div>
            <div style="display:flex; justify-content:space-between;"><span style="color:var(--rose);">● Critical (Red):</span> <strong>${m.project_health_breakdown.red || 0}</strong></div>
          </div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="color:var(--rose);">Error loading metrics: ${err.message}</div>`;
  }
}

// --- 13. QUICK CAPTURE MODAL ---
function openQuickCapture(defaultType = "task") {
  const modal = document.getElementById("quick-capture-modal");
  const typeSelect = document.getElementById("qc-type-select");
  if (typeSelect) {
    typeSelect.value = defaultType;
    renderQuickCaptureFields(defaultType);
  }
  if (modal) modal.classList.add("active");
}

function closeQuickCapture() {
  const modal = document.getElementById("quick-capture-modal");
  if (modal) modal.classList.remove("active");
}

function renderQuickCaptureFields(type) {
  const container = document.getElementById("qc-dynamic-fields");
  if (!container) return;

  switch (type) {
    case "task":
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Task Title</label>
          <input type="text" id="qc-title" class="form-input" placeholder="e.g. Implement zero-copy buffer..." required />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Priority</label>
            <select id="qc-priority" class="form-select">
              <option value="p0_critical">P0 - Critical</option>
              <option value="p1_high">P1 - High</option>
              <option value="p2_medium" selected>P2 - Medium</option>
              <option value="p3_low">P3 - Low</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Energy Level</label>
            <select id="qc-energy" class="form-select">
              <option value="deep_work" selected>Deep Work</option>
              <option value="quick_win">Quick Win</option>
              <option value="administrative">Administrative</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Deadline (YYYY-MM-DD)</label>
          <input type="date" id="qc-deadline" class="form-input" />
        </div>
      `;
      break;

    case "project":
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Project Title</label>
          <input type="text" id="qc-title" class="form-input" placeholder="e.g. Distributed Agent Mesh..." required />
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea id="qc-desc" class="form-textarea" placeholder="Strategic objective and scope..."></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Category</label>
            <select id="qc-category" class="form-select">
              <option value="ai_systems" selected>AI Systems</option>
              <option value="research">Research</option>
              <option value="product">Product</option>
              <option value="infrastructure">Infrastructure</option>
              <option value="career">Career</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Target Completion Date</label>
            <input type="date" id="qc-target-date" class="form-input" />
          </div>
        </div>
      `;
      break;

    case "idea":
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Idea Title</label>
          <input type="text" id="qc-title" class="form-input" placeholder="e.g. Adaptive speculative decoding heuristic..." required />
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea id="qc-desc" class="form-textarea" placeholder="Core concept and value proposition..."></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Category</label>
            <select id="qc-category" class="form-select">
              <option value="software" selected>Software</option>
              <option value="research">Research</option>
              <option value="venture">Venture</option>
              <option value="personal">Personal</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Origin</label>
            <input type="text" id="qc-origin" class="form-input" placeholder="How did this come to mind?" />
          </div>
        </div>
      `;
      break;

    case "experiment":
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Experiment Title</label>
          <input type="text" id="qc-title" class="form-input" placeholder="e.g. Speculative decoding throughput on MPS..." required />
        </div>
        <div class="form-group">
          <label class="form-label">Hypothesis (If X, then Y because Z)</label>
          <textarea id="qc-hypothesis" class="form-textarea" placeholder="Formal falsifiable hypothesis..."></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Objective & Test Design</label>
          <textarea id="qc-design" class="form-textarea" placeholder="How will you measure this?"></textarea>
        </div>
      `;
      break;

    case "decision":
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Decision Statement</label>
          <input type="text" id="qc-title" class="form-input" placeholder="e.g. Adopt SQLite WAL over PostgreSQL..." required />
        </div>
        <div class="form-group">
          <label class="form-label">Context & Driving Constraints</label>
          <textarea id="qc-context" class="form-textarea" placeholder="Why must this decision be made?"></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Confidence (1-100%)</label>
            <input type="number" id="qc-confidence" class="form-input" value="80" min="1" max="100" />
          </div>
          <div class="form-group">
            <label class="form-label">Outcome Review Date</label>
            <input type="date" id="qc-review-date" class="form-input" />
          </div>
        </div>
      `;
      break;

    case "opportunity":
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Opportunity Title</label>
          <input type="text" id="qc-title" class="form-input" placeholder="e.g. Strategic advisory role at Edge AI startup..." required />
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Category</label>
            <select id="qc-category" class="form-select">
              <option value="career" selected>Career</option>
              <option value="business">Business</option>
              <option value="technology">Technology</option>
              <option value="investment">Investment</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Source</label>
            <input type="text" id="qc-source" class="form-input" placeholder="Inbound email, referral, discovery..." />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Potential Upside</label>
          <input type="text" id="qc-upside" class="form-input" placeholder="Equity grant, $100k ARR, skill acquisition..." />
        </div>
      `;
      break;

    default:
      container.innerHTML = `
        <div class="form-group">
          <label class="form-label">Title</label>
          <input type="text" id="qc-title" class="form-input" required />
        </div>
      `;
  }
}

async function submitQuickCapture() {
  const type = document.getElementById("qc-type-select").value;
  const title = document.getElementById("qc-title")?.value?.trim();
  if (!title) {
    showToast("Title is required", "error");
    return;
  }

  try {
    switch (type) {
      case "task":
        await API.createTask({
          title,
          priority: document.getElementById("qc-priority").value,
          energy_level: document.getElementById("qc-energy").value,
          deadline: document.getElementById("qc-deadline")?.value || null
        });
        showToast("Task registered in Today cockpit.");
        break;

      case "project":
        await API.createProject({
          title,
          description: document.getElementById("qc-desc")?.value || "",
          category: document.getElementById("qc-category").value,
          target_date: document.getElementById("qc-target-date")?.value || null
        });
        showToast("Project created.");
        break;

      case "idea":
        await API.createIdea({
          title,
          description: document.getElementById("qc-desc")?.value || "",
          category: document.getElementById("qc-category").value,
          origin: document.getElementById("qc-origin")?.value || ""
        });
        showToast("Idea captured in stage pipeline.");
        break;

      case "experiment":
        await API.createExperiment({
          title,
          hypothesis: document.getElementById("qc-hypothesis")?.value || "Hypothesis pending formulation",
          objective: "Empirical verification",
          experiment_design: document.getElementById("qc-design")?.value || "Standard test harness",
          expected_result: "Verification of hypothesis"
        });
        showToast("Experiment registered.");
        break;

      case "decision":
        await API.createDecision({
          title,
          date: new Date().toISOString().substring(0, 10),
          context: document.getElementById("qc-context")?.value || "Operational decision",
          assumptions: "Key working assumptions",
          evidence: "Empirical observation",
          expected_outcome: "Positive system progression",
          confidence_level: parseInt(document.getElementById("qc-confidence")?.value || "75"),
          review_date: document.getElementById("qc-review-date")?.value || null
        });
        showToast("Decision logged.");
        break;

      case "opportunity":
        await API.createOpportunity({
          title,
          date_discovered: new Date().toISOString().substring(0, 10),
          category: document.getElementById("qc-category").value,
          source: document.getElementById("qc-source")?.value || "",
          potential_upside: document.getElementById("qc-upside")?.value || ""
        });
        showToast("Opportunity logged on radar.");
        break;
    }

    closeQuickCapture();
    refreshNavBadges();
    switchView(activeView);
  } catch (err) {
    showToast("Error creating entity: " + err.message, "error");
  }
}

// Global Keyboard Shortcuts
function setupKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    // Ignore in inputs and textareas
    if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) {
      if (e.key === "Escape") {
        closeSearchModal();
        closeQuickCapture();
        closeAIModal();
      }
      return;
    }

    // Cmd+K or Ctrl+K or /
    if ((e.metaKey || e.ctrlKey) && e.key === "k" || e.key === "/") {
      e.preventDefault();
      openSearchModal();
    }
    // C key for Quick Capture
    else if (e.key === "c" || e.key === "C") {
      e.preventDefault();
      openQuickCapture("task");
    }
    // B key for Daily Briefing
    else if (e.key === "b" || e.key === "B") {
      e.preventDefault();
      triggerDailyBriefing();
    }
    // Number keys for view switching
    else if (e.key >= "1" && e.key <= "9") {
      const views = ["today", "projects", "ideas", "experiments", "decisions", "research", "learning", "opportunities", "graph"];
      const target = views[parseInt(e.key) - 1];
      if (target) switchView(target);
    }
    // Esc closes modals
    else if (e.key === "Escape") {
      closeSearchModal();
      closeQuickCapture();
      closeAIModal();
    }
  });
}

// Application Startup
document.addEventListener("DOMContentLoaded", () => {
  startClock();
  setupKeyboardShortcuts();
  switchView("today");
  refreshNavBadges();
});
