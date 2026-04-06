const pagesList = document.getElementById("pages-list");
const pagesStatus = document.getElementById("pages-status");
const edgesList = document.getElementById("edges-list");
const edgesStatus = document.getElementById("edges-status");
const pageDetail = document.getElementById("page-detail");
const selectedUrl = document.getElementById("selected-url");
const filterForm = document.getElementById("filter-form");
const titleFilter = document.getElementById("title-filter");
const deadFilter = document.getElementById("dead-filter");
const resetFiltersButton = document.getElementById("reset-filters");
const reloadEdgesButton = document.getElementById("reload-edges");
const pageCount = document.getElementById("page-count");
const deadCount = document.getElementById("dead-count");
const edgeCount = document.getElementById("edge-count");
const aliveRatio = document.getElementById("alive-ratio");
const filterSummary = document.getElementById("filter-summary");
const activeFilterLabel = document.getElementById("active-filter-label");

let currentPages = [];
let currentSelection = null;

function buildPagesQuery() {
  const params = new URLSearchParams();
  const title = titleFilter.value.trim();
  const isDead = deadFilter.value;

  if (title) {
    params.set("title", title);
  }

  if (isDead !== "") {
    params.set("isDead", isDead);
  }

  const query = params.toString();
  return query ? `/pages?${query}` : "/pages";
}

function createStatusPill(isDead) {
  const statusClass = isDead === 1 ? "dead" : "alive";
  const statusLabel = isDead === 1 ? "Dead Link" : "Alive";
  return `<span class="pill ${statusClass}">${statusLabel}</span>`;
}

function renderPageStats(pages) {
  pageCount.textContent = pages.length;
  deadCount.textContent = pages.filter((page) => page.isDead === 1).length;

  const alivePages = pages.filter((page) => page.isDead === 0).length;
  const ratio = pages.length ? Math.round((alivePages / pages.length) * 100) : 0;
  aliveRatio.textContent = `${ratio}%`;
}

function describeCurrentFilters() {
  const title = titleFilter.value.trim();
  const isDead = deadFilter.value;
  const parts = [];

  if (title) {
    parts.push(`title: "${title}"`);
  }

  if (isDead === "0") {
    parts.push("alive only");
  } else if (isDead === "1") {
    parts.push("dead only");
  }

  if (!parts.length) {
    return "Browsing all pages";
  }

  return parts.join(" • ");
}

function updateFilterCopy() {
  const label = describeCurrentFilters();
  filterSummary.textContent = label;
  activeFilterLabel.textContent = label;
}

function renderPages(pages) {
  currentPages = pages;
  renderPageStats(pages);
  updateFilterCopy();

  if (!pages.length) {
    pagesList.innerHTML = "";
    pagesStatus.textContent = "No pages matched the current filters.";
    clearSelection();
    return;
  }

  pagesStatus.textContent = `Showing ${pages.length} crawler pages.`;
  pagesList.innerHTML = pages
    .map((page) => `
      <article class="page-card${currentSelection?.id === page.id ? " active" : ""}" data-page-id="${page.id}">
        <div class="page-card-header">
          <h3>${page.title || "Untitled page"}</h3>
          ${createStatusPill(page.isDead)}
        </div>
        <p><a class="page-link" href="${page.url}" target="_blank" rel="noreferrer">${page.url}</a></p>
        <div class="meta-grid">
          <div class="meta-item">
            <span class="meta-label">Status Code</span>
            <span class="meta-value">${page.statusCode}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Page ID</span>
            <span class="meta-value">${page.id}</span>
          </div>
        </div>
      </article>
    `)
    .join("");

  document.querySelectorAll(".page-card").forEach((card) => {
    card.addEventListener("click", () => {
      const pageId = Number(card.dataset.pageId);
      const page = currentPages.find((entry) => entry.id === pageId);

      if (page) {
        selectPage(page);
      }
    });
  });
}

function renderSelectedPage(page) {
  pageDetail.className = "detail-card";
  pageDetail.innerHTML = `
    <div class="page-card-header">
      <h3>${page.title || "Untitled page"}</h3>
      ${createStatusPill(page.isDead)}
    </div>
    <p><a class="page-link" href="${page.url}" target="_blank" rel="noreferrer">${page.url}</a></p>
    <div class="meta-grid">
      <div class="meta-item">
        <span class="meta-label">Status Code</span>
        <span class="meta-value">${page.statusCode}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Page ID</span>
        <span class="meta-value">${page.id}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Dead Flag</span>
        <span class="meta-value">${page.isDead}</span>
      </div>
    </div>
  `;
  selectedUrl.textContent = page.url;
  reloadEdgesButton.disabled = false;
}

function clearSelection() {
  currentSelection = null;
  selectedUrl.textContent = "Choose a page to view its outbound links.";
  pageDetail.className = "detail-card empty-state";
  pageDetail.textContent = "Select a page from the list to load its link relationships.";
  edgesList.innerHTML = "";
  edgesStatus.textContent = "No page selected yet.";
  edgeCount.textContent = "0";
  reloadEdgesButton.disabled = true;
}

function renderEdges(edges) {
  edgeCount.textContent = edges.length;

  if (!edges.length) {
    edgesList.innerHTML = "";
    edgesStatus.textContent = "No outbound edges were found for this page.";
    return;
  }

  edgesStatus.textContent = `Loaded ${edges.length} outbound edge${edges.length === 1 ? "" : "s"}.`;
  edgesList.innerHTML = edges
    .map((edge) => `
      <article class="edge-card">
        <span class="meta-label">Target URL</span>
        <p><a href="${edge.targetUrl}" target="_blank" rel="noreferrer">${edge.targetUrl}</a></p>
      </article>
    `)
    .join("");
}

async function loadEdges(sourceUrl) {
  edgesStatus.textContent = "Loading edges...";
  edgesList.innerHTML = "";

  const params = new URLSearchParams({ sourceUrl });
  const response = await fetch(`/edges?${params.toString()}`);

  if (!response.ok) {
    throw new Error(`Failed to load edges (${response.status})`);
  }

  const edges = await response.json();
  renderEdges(edges);
}

async function selectPage(page) {
  currentSelection = page;
  renderSelectedPage(page);
  renderPages(currentPages);

  try {
    await loadEdges(page.url);
  } catch (error) {
    edgeCount.textContent = "0";
    edgesStatus.textContent = error.message;
  }
}

async function loadPages() {
  pagesStatus.textContent = "Loading crawler pages...";
  pagesList.innerHTML = "";

  const response = await fetch(buildPagesQuery());

  if (!response.ok) {
    throw new Error(`Failed to load pages (${response.status})`);
  }

  const pages = await response.json();
  renderPages(pages);
}

filterForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    await loadPages();
  } catch (error) {
    pagesStatus.textContent = error.message;
    pagesList.innerHTML = "";
    renderPageStats([]);
    clearSelection();
  }
});

resetFiltersButton.addEventListener("click", async () => {
  titleFilter.value = "";
  deadFilter.value = "";

  try {
    await loadPages();
  } catch (error) {
    pagesStatus.textContent = error.message;
    pagesList.innerHTML = "";
    renderPageStats([]);
    clearSelection();
  }
});

reloadEdgesButton.addEventListener("click", async () => {
  if (!currentSelection) {
    return;
  }

  try {
    await loadEdges(currentSelection.url);
  } catch (error) {
    edgeCount.textContent = "0";
    edgesStatus.textContent = error.message;
  }
});

async function initializeDashboard() {
  clearSelection();
  updateFilterCopy();

  try {
    await loadPages();
  } catch (error) {
    pagesStatus.textContent = error.message;
    renderPageStats([]);
  }
}

initializeDashboard();
