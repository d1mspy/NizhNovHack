<script lang="ts">
  // ----- типы -----
  type Vacancy = { id: string; name: string };
  type Candidate = { id: string; position: string; score: number };

  // ----- мок-данные -----
  let vacancies: Vacancy[] = [
    { id: 'v1', name: 'Data Engineer' },
    { id: 'v2', name: 'Frontend Developer' },
    { id: 'v3', name: 'ML Engineer' },
    { id: 'v4', name: 'QA Automation' },
    { id: 'v5', name: 'DevOps' },
    { id: 'v6', name: 'Product Analyst' },
    { id: 'v7', name: 'Backend Go' },
  ];

  let selected: Set<string> = new Set();          // выбранные вакансии
  let candidates: Candidate[] = [];               // появятся после "Поиска"
  let isSearching = false;

  const toggleSelect = (id: string) => {
    const next = new Set(selected);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    selected = next;
  };

  const hasSelection = () => selected.size > 0;

  // имитация ответа от бэка
  const runSearch = async () => {
    if (isSearching) return;
    isSearching = true;
    await new Promise((r) => setTimeout(r, 600));
    candidates = [
      { id: 'c1', position: 'Middle Data Engineer', score: 86 },
      { id: 'c2', position: 'Senior Frontend (React)', score: 74 },
      { id: 'c3', position: 'ML Engineer (NLP)', score: 92 },
      { id: 'c4', position: 'QA Automation', score: 65 },
      { id: 'c5', position: 'DevOps Engineer', score: 80 }
    ];
    isSearching = false;
  };
</script>

<svelte:head>
  <title>Поиск кандидатов - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <div class="search-screen">
    <!-- Левая колонка -->
    <section class="pane left-pane">
      <div class="pane-header">
        <h2>Вакансии</h2>
        <span class="badge">{vacancies.length}</span>
      </div>

      <div class="vacancies-list">
        {#each vacancies as v (v.id)}
          <button
            class="vacancy-card {selected.has(v.id) ? 'selected' : ''}"
            on:click={() => toggleSelect(v.id)}
            aria-pressed={selected.has(v.id)}
          >
            <span class="vacancy-name">{v.name}</span>
            {#if selected.has(v.id)}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M20 6L9 17l-5-5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {/if}
          </button>
        {/each}
      </div>
    </section>

    <!-- Правая колонка -->
    <section class="pane right-pane">
      <div class="pane-header">
        <h2>Кандидаты</h2>
        <span class="badge">{candidates.length}</span>
      </div>

      {#if candidates.length === 0}
        <div class="empty-state">
          <p>Выберите вакансию и нажмите "Поиск"</p>
          <span class="empty-subtitle">Здесь появятся подходящие кандидаты</span>
        </div>
      {:else}
        <div class="candidates-list">
          {#each candidates as c (c.id)}
            <div class="candidate-card">
              <div class="candidate-info">
                <span class="candidate-position">{c.position}</span>
                <div class="score-container">
                  <div class="score-bar">
                    <div class="score-fill" style={`width: ${c.score}%`}></div>
                  </div>
                  <span class="score-value">{c.score}%</span>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </section>

    <!-- Кнопка поиска -->
    <button
      class="search-button"
      on:click={runSearch}
      disabled={isSearching}
    >
      {#if isSearching}
        Поиск...
      {:else}
        Поиск
      {/if}
    </button>
  </div>
</div>

<style>
  :global(body) {
    background: #f8fafc;
    color: #333;
    line-height: 1.5;
    overflow: hidden;
  }

  .page-container {
    width: 100%;
    height: 100vh;
    margin: 0;
    padding: 20px;
    box-sizing: border-box;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .search-screen {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 100px;
    position: relative;
    background: white;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
    height: 75%;
    width: 85%;
    margin: 0 auto;
  }

  .pane {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .pane-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #f1f5f9;
  }

  .pane-header h2 {
    margin: 0;
    font-size: 22px;
    font-weight: 600;
    color: #1f2937;
  }

  .badge {
    background: #e0f2fe;
    color: #1DAFF7;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
  }

  .vacancies-list,
  .candidates-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
    overflow-y: auto;
    padding-right: 5px;
  }

  .vacancy-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    cursor: pointer;
    transition: border-color 0.2s ease;
    text-align: left;
    width: 100%;
  }

  .vacancy-card:hover {
    border-color: #1DAFF7;
  }

  .vacancy-card.selected {
    background: #f0f9ff;
    border-color: #1DAFF7;
    color: #1DAFF7;
  }

  .vacancy-name {
    font-size: 15px;
    font-weight: 500;
    color: #1f2937;
  }

  .vacancy-card.selected .vacancy-name {
    color: #1DAFF7;
    font-weight: 600;
  }

  .candidate-card {
    padding: 16px 18px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
  }

  .candidate-info {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .candidate-position {
    font-size: 15px;
    font-weight: 500;
    color: #1f2937;
  }

  .score-container {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .score-bar {
    flex: 1;
    height: 8px;
    background: #f1f5f9;
    border-radius: 4px;
    overflow: hidden;
  }

  .score-fill {
    height: 100%;
    background: #1DAFF7;
    border-radius: 4px;
  }

  .score-value {
    font-size: 14px;
    font-weight: 600;
    color: #1DAFF7;
    min-width: 40px;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: #64748b;
    padding: 40px 20px;
  }

  .empty-state p {
    margin: 0 0 8px 0;
    font-size: 16px;
    font-weight: 500;
    color: #374151;
  }

  .empty-subtitle {
    font-size: 14px;
    color: #94a3b8;
  }

  .search-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 12px 30px;
    margin: 1rem;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .search-button:hover:not(:disabled) {
    background: #0d8dcd;
  }

  .search-button:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
  }
</style>