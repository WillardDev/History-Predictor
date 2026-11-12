const API = "/api/v1";

const form = document.getElementById("generate-form");
const presetSelect = document.getElementById("preset");
const submitButton = document.getElementById("submit-button");
const resetButton = document.getElementById("reset-button");
const statusBox = document.getElementById("status");
const results = document.getElementById("results");

let presets = [];

const fields = {
  name: document.getElementById("name"),
  start_date: document.getElementById("start_date"),
  end_date: document.getElementById("end_date"),
  event_type: document.getElementById("event_type"),
  geographic_scope: document.getElementById("geographic_scope"),
  description: document.getElementById("description"),
  key_figures: document.getElementById("key_figures"),
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entities[character];
  });
}

function formatLabel(key) {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", isError);
  statusBox.hidden = false;
}

function clearStatus() {
  statusBox.hidden = true;
  statusBox.textContent = "";
  statusBox.classList.remove("error");
}

async function loadPresets() {
  try {
    const response = await fetch(`${API}/events`);
    if (!response.ok) return;
    const data = await response.json();
    presets = data.events || [];
    presets.forEach((event, index) => {
      const option = document.createElement("option");
      option.value = String(index);
      option.textContent = event.name;
      presetSelect.appendChild(option);
    });
  } catch (error) {
    // Presets are a convenience; the form still works without them.
  }
}

function fillFromPreset(event) {
  fields.name.value = event.name || "";
  fields.start_date.value = event.start_date || "";
  fields.end_date.value = event.end_date || "";
  fields.event_type.value = event.event_type || "general";
  fields.geographic_scope.value = event.geographic_scope || "";
  fields.description.value = event.description || "";
  fields.key_figures.value = (event.key_figures || []).join(", ");
}

presetSelect.addEventListener("change", () => {
  const selected = presets[Number(presetSelect.value)];
  if (selected) fillFromPreset(selected);
});

function buildPayload() {
  const pillars = Array.from(
    document.querySelectorAll('input[type="checkbox"]:checked')
  ).map((checkbox) => checkbox.value);

  const keyFigures = fields.key_figures.value
    .split(",")
    .map((name) => name.trim())
    .filter(Boolean);

  return {
    event: {
      name: fields.name.value.trim(),
      start_date: fields.start_date.value.trim(),
      end_date: fields.end_date.value.trim() || null,
      description: fields.description.value.trim(),
      key_figures: keyFigures,
      geographic_scope: fields.geographic_scope.value.trim(),
      event_type: fields.event_type.value.trim() || "general",
    },
    num_years: Number(document.getElementById("num_years").value),
    focus_pillars: pillars.length ? pillars : null,
    additional_context:
      document.getElementById("additional_context").value.trim() || null,
  };
}

function renderDetail(label, value) {
  return `
    <div class="detail">
      <strong>${escapeHtml(formatLabel(label))}</strong>
      <p>${escapeHtml(value)}</p>
    </div>
  `;
}

function renderPillar(name, pillar) {
  const rows = Object.entries(pillar || {})
    .map(
      ([key, value]) => `
        <dt>${escapeHtml(formatLabel(key))}</dt>
        <dd>${escapeHtml(value)}</dd>
      `
    )
    .join("");

  return `
    <div class="pillar ${escapeHtml(name)}">
      <h4>${escapeHtml(name)}</h4>
      <dl>${rows}</dl>
    </div>
  `;
}

function renderResults(data, eventName) {
  const pivot = Object.entries(data.pivot || {})
    .map(([key, value]) => renderDetail(key, value))
    .join("");

  const years = (data.timeline || [])
    .map(
      (entry) => `
        <article class="card year-card">
          <div class="year">${escapeHtml(entry.year)}</div>
          <div class="pillars">
            ${renderPillar("social", entry.social)}
            ${renderPillar("economy", entry.economy)}
            ${renderPillar("political", entry.political)}
          </div>
        </article>
      `
    )
    .join("");

  const consequences = Object.entries(data.long_term_consequences || {})
    .map(([key, value]) => renderDetail(key, value))
    .join("");

  const time = data.processing_time_ms
    ? `${(data.processing_time_ms / 1000).toFixed(1)}s`
    : "—";

  results.innerHTML = `
    <div class="result-head">
      <div>
        <h2>${escapeHtml(eventName)}</h2>
        <p>${(data.timeline || []).length} years projected after the divergence point.</p>
      </div>
      <div class="badges">
        <span class="badge">Plausibility ${escapeHtml(data.plausibility_score)}/10</span>
        <span class="badge">${escapeHtml(data.confidence_level)} confidence</span>
        <span class="badge">Generated in ${escapeHtml(time)}</span>
      </div>
    </div>

    <article class="card">
      <h3>The divergence point</h3>
      <div class="pivot-grid">${pivot}</div>
    </article>

    ${years}

    <article class="card">
      <h3>Long-term consequences</h3>
      <div class="consequence-grid">${consequences}</div>
    </article>

    <article class="card">
      <h3>Historical grounding</h3>
      <p>${escapeHtml(data.historical_grounding)}</p>
    </article>
  `;

  results.hidden = false;
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearStatus();
  results.hidden = true;
  submitButton.disabled = true;
  submitButton.textContent = "Simulating…";
  setStatus("Consulting the historical record and building your timeline…");

  try {
    const payload = buildPayload();
    const response = await fetch(`${API}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(body.detail || `Request failed (${response.status})`);
    }

    clearStatus();
    renderResults(body.data, payload.event.name);
  } catch (error) {
    setStatus(error.message || "Something went wrong. Please try again.", true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Generate alternate timeline";
  }
});

resetButton.addEventListener("click", () => {
  form.reset();
  presetSelect.value = "";
  clearStatus();
  results.hidden = true;
  results.innerHTML = "";
  window.scrollTo({ top: 0, behavior: "smooth" });
});

loadPresets();
