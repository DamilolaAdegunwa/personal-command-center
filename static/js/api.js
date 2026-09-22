// REST API Client for Personal Command Center
const API = {
  async get(url) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      return await res.json();
    } catch (err) {
      console.error("GET Error:", url, err);
      showToast("Error loading data: " + err.message, "error");
      throw err;
    }
  },

  async post(url, body) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      console.error("POST Error:", url, err);
      showToast("Operation failed: " + err.message, "error");
      throw err;
    }
  },

  async put(url, body) {
    try {
      const res = await fetch(url, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      console.error("PUT Error:", url, err);
      showToast("Update failed: " + err.message, "error");
      throw err;
    }
  },

  async delete(url) {
    try {
      const res = await fetch(url, { method: "DELETE" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error("DELETE Error:", url, err);
      showToast("Delete failed: " + err.message, "error");
      throw err;
    }
  },

  // Specialized Endpoints
  getToday: () => API.get("/api/today"),
  getMetrics: () => API.get("/api/metrics"),
  getGraph: () => API.get("/api/graph"),
  search: (params) => {
    const q = new URLSearchParams(params).toString();
    return API.get(`/api/search?${q}`);
  },

  // Entities
  getProjects: (status, health) => {
    let url = "/api/projects";
    const q = [];
    if (status) q.push(`status=${status}`);
    if (health) q.push(`health=${health}`);
    if (q.length) url += `?${q.join("&")}`;
    return API.get(url);
  },
  createProject: (data) => API.post("/api/projects", data),
  updateProject: (id, data) => API.put(`/api/projects/${id}`, data),
  deleteProject: (id) => API.delete(`/api/projects/${id}`),

  getIdeas: (status, category) => {
    let url = "/api/ideas";
    const q = [];
    if (status) q.push(`status=${status}`);
    if (category) q.push(`category=${category}`);
    if (q.length) url += `?${q.join("&")}`;
    return API.get(url);
  },
  createIdea: (data) => API.post("/api/ideas", data),
  updateIdea: (id, data) => API.put(`/api/ideas/${id}`, data),
  transitionIdea: (id, status) => API.post(`/api/ideas/${id}/transition?target_status=${status}`, {}),
  deleteIdea: (id) => API.delete(`/api/ideas/${id}`),

  getExperiments: (status) => API.get(status ? `/api/experiments?status=${status}` : "/api/experiments"),
  createExperiment: (data) => API.post("/api/experiments", data),
  updateExperiment: (id, data) => API.put(`/api/experiments/${id}`, data),
  deleteExperiment: (id) => API.delete(`/api/experiments/${id}`),

  getDecisions: (status) => API.get(status ? `/api/decisions?status=${status}` : "/api/decisions"),
  createDecision: (data) => API.post("/api/decisions", data),
  updateDecision: (id, data) => API.put(`/api/decisions/${id}`, data),
  deleteDecision: (id) => API.delete(`/api/decisions/${id}`),

  getResearch: (topic, status) => {
    let url = "/api/research";
    const q = [];
    if (topic) q.push(`topic=${topic}`);
    if (status) q.push(`status=${status}`);
    if (q.length) url += `?${q.join("&")}`;
    return API.get(url);
  },
  createResearch: (data) => API.post("/api/research", data),
  updateResearch: (id, data) => API.put(`/api/research/${id}`, data),
  deleteResearch: (id) => API.delete(`/api/research/${id}`),

  getLearning: (status) => API.get(status ? `/api/learning?status=${status}` : "/api/learning"),
  createLearning: (data) => API.post("/api/learning", data),
  updateLearning: (id, data) => API.put(`/api/learning/${id}`, data),
  deleteLearning: (id) => API.delete(`/api/learning/${id}`),

  getOpportunities: (category, status) => {
    let url = "/api/opportunities";
    const q = [];
    if (category) q.push(`category=${category}`);
    if (status) q.push(`status=${status}`);
    if (q.length) url += `?${q.join("&")}`;
    return API.get(url);
  },
  createOpportunity: (data) => API.post("/api/opportunities", data),
  updateOpportunity: (id, data) => API.put(`/api/opportunities/${id}`, data),
  deleteOpportunity: (id) => API.delete(`/api/opportunities/${id}`),

  getTasks: (status, priority, project_id) => {
    let url = "/api/tasks";
    const q = [];
    if (status) q.push(`status=${status}`);
    if (priority) q.push(`priority=${priority}`);
    if (project_id) q.push(`project_id=${project_id}`);
    if (q.length) url += `?${q.join("&")}`;
    return API.get(url);
  },
  createTask: (data) => API.post("/api/tasks", data),
  updateTask: (id, data) => API.put(`/api/tasks/${id}`, data),
  deleteTask: (id) => API.delete(`/api/tasks/${id}`),

  // Knowledge Edges
  createEdge: (data) => API.post("/api/edges", data),
  deleteEdge: (id) => API.delete(`/api/edges/${id}`),

  // AI Intelligence
  getDailyBriefing: () => API.post("/api/ai/daily-briefing", {}),
  getWeeklyReview: () => API.post("/api/ai/weekly-review", {}),
  analyzeProject: (id) => API.post(`/api/ai/analyze-project/${id}`, {}),
  analyzeIdea: (id) => API.post(`/api/ai/analyze-idea/${id}`, {}),
  reviewDecision: (id) => API.post(`/api/ai/review-decision/${id}`, {})
};
