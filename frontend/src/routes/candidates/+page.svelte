<script lang="ts">
  import { goto } from '$app/navigation';
  type Vacancy = { id: string; name: string };
  type Matching = { score: number; position: string; decision?: string; reasoning_report?: string };
  type Candidate = { id: string; position: string; score: number; decision?: string; reasoning_report?: string };

  let vacancies: Vacancy[] = [];
  let selected: Set<string> = new Set();
  let candidates: Candidate[] = [];
  let isLoadingVacancies = false;
  let isSearching = false;
  let err = '';

  const hasSelection = () => selected.size > 0;

  const toggleSelect = (id: string) => {
    const next = new Set(selected);
    next.has(id) ? next.delete(id) : next.add(id);
    selected = next;
  };

  const fetchVacancies = async () => {
    isLoadingVacancies = true; err = '';
    try {
      const res = await fetch('/api/vacancy');
      if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
      const data = await res.json() as Array<any>;
      vacancies = data.map(v => ({ id: v.id, name: v.name }));
    } catch (e) {
      err = e instanceof Error ? e.message : 'Неизвестная ошибка загрузки вакансий';
      console.error(e);
    } finally {
      isLoadingVacancies = false;
    }
  };

  // загрузим список слева при входе
  fetchVacancies();

  const runSearch = async () => {
    if (isSearching || selected.size === 0) return;
    isSearching = true; err = '';
    candidates = []; // очистим правую колонку
    try {
      const ids = Array.from(selected);
      const requests = ids.map(async (vacId) => {
        const res = await fetch(`/api/vac/${vacId}/matching`, { method: 'PUT' });
        if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
        const arr = await res.json() as Matching[];
        return arr.map((m, i) => ({
          id: `${vacId}:${i}`,
          position: m.position,
          score: Math.max(0, Math.min(100, Math.round(m.score))),
          decision: m.decision, 
          reasoning_report: m.reasoning_report,
        }));
      });

      const results = await Promise.all(requests);
      candidates = results.flat();
    } catch (e) {
      err = e instanceof Error ? e.message : 'Неизвестная ошибка поиска';
      console.error(e);
    } finally {
      isSearching = false;
    }
  };

  // ─────────────────────────────────────────────────────────────
  // РУЧНОЙ ВВОД ВАКАНСИИ (режим «вместо списка»)
  // ─────────────────────────────────────────────────────────────
  let showManual = false;
  let manualName = '';
  let manualDesc = '';
  let manualYears = '';
  let manualSkills = '';
  let manualErr = '';
  let manualLoading = false;

  const canManualSearch = () => {
    const yearsNum = Number(manualYears);
    return (
      manualName.trim().length > 0 &&
      manualDesc.trim().length > 0 &&
      manualSkills.trim().length > 0 &&
      Number.isFinite(yearsNum) &&
      yearsNum >= 0
    );
  };

  const runManualMatching = async () => {
    if (!canManualSearch() || manualLoading) return;
    manualLoading = true; manualErr = ''; isSearching = true; err = '';
    candidates = [];

    try {
      const yearsNum = Number(manualYears) || 0;
      const min_exp_months = Math.max(0, Math.round(yearsNum * 12));

      const must_have = manualSkills
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);

      const payload = {
        name: manualName.trim(),
        description: manualDesc.trim(),
        min_exp_months,
        must_have
      };

      const res = await fetch('/api/matching/vacancy', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));

      const arr = await res.json() as Matching[];
      candidates = (Array.isArray(arr) ? arr : []).map((m, i) => ({
        id: `manual:${i}`,
        position: String(m.position ?? 'Кандидат'),
        score: Math.max(0, Math.min(100, Math.round(Number(m.score) || 0)))
      }));
    } catch (e) {
      manualErr = e instanceof Error ? e.message : 'Неизвестная ошибка';
    } finally {
      manualLoading = false;
      isSearching = false;
    }
  };

  function goBack() {
    goto(`/vacancy`);
  }

</script>

<svelte:head>
  <title>Поиск кандидатов - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <button class="back-btn" on:click={goBack}>
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    Назад
  </button>
  <div class="search-screen">
    <!-- Левая колонка -->
    <section class="pane left-pane">
      <div class="pane-header">
        <h2>Вакансии</h2>
        <div class="left-actions">
          <button
            class="manual-toggle"
            on:click={() => (showManual = !showManual)}
            aria-expanded={showManual}
            type="button"
          >
            {#if showManual}
              ← К списку
            {:else}
              Добавить вручную
            {/if}
          </button>
          <span class="badge">{vacancies.length}</span>
        </div>
      </div>

      <!-- ТУТ ВКЛ/ВЫКЛ КОНТЕНТА: ЛИБО СПИСОК, ЛИБО ФОРМА -->
      {#if showManual}
        <div class="manual-card">
          <div class="input-group">
            <label class="form-label" for="mn-name">Название вакансии *</label>
            <input
              id="mn-name"
              class="form-input"
              type="text"
              bind:value={manualName}
              placeholder="Например: Data Engineer"
            />
          </div>

          <div class="input-group">
            <label class="form-label" for="mn-desc">Описание вакансии *</label>
            <textarea
              id="mn-desc"
              class="form-textarea"
              rows="5"
              bind:value={manualDesc}
              placeholder="Кратко опишите задачи и требования"
            ></textarea>
          </div>

          <div class="input-row">
            <div class="input-group">
              <label class="form-label" for="mn-years">Требуемый опыт (лет) *</label>
              <input
                id="mn-years"
                class="form-input"
                type="number"
                min="0"
                step="1"
                bind:value={manualYears}
                placeholder="Например: 2"
                inputmode="numeric"
              />
            </div>

            <div class="input-group">
              <label class="form-label" for="mn-skills">Навыки (через запятую) *</label>
              <input
                id="mn-skills"
                class="form-input"
                type="text"
                bind:value={manualSkills}
                placeholder="Python, SQL, Airflow"
              />
              <div class="input-hint">Указывайте навыки через запятую — превратим в список.</div>
            </div>
          </div>

          {#if manualErr}
            <div class="err-text">Ошибка: {manualErr}</div>
          {/if}

          <div class="manual-actions">
            <button
              class="manual-search-btn"
              on:click={runManualMatching}
              disabled={!canManualSearch() || manualLoading}
              type="button"
            >
              {manualLoading ? 'Ищем…' : 'Найти'}
            </button>
          </div>
        </div>
      {:else}
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
          {#if isLoadingVacancies}<div class="list-hint">Загружаем вакансии…</div>{/if}
          {#if err && !isLoadingVacancies}<div class="list-error">Ошибка: {err}</div>{/if}
        </div>
      {/if}
    </section>

    <!-- Правая колонка -->
    <section class="pane right-pane">
      <div class="pane-header">
        <h2>Кандидаты</h2>
        <span class="badge">{candidates.length}</span>
      </div>

      {#if candidates.length === 0}
        <div class="empty-state">
          <p>Выберите вакансию слева и нажмите «Поиск»</p>
          <span class="empty-subtitle">Либо добавьте вакансию вручную и нажмите «Найти»</span>
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

                {#if c.decision} 
                  <div class="recommendation"> 
                    <span class="rec-label">Рекомендация:</span>
                    <span class="rec-text">{c.decision}</span>
                  </div>
                {/if} 
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </section>

    <!-- Центральная кнопка поиска для выбранных вакансий -->
    <button
      class="search-button"
      on:click={runSearch}
      disabled={isSearching || !hasSelection()}
      title={hasSelection() ? 'Поиск по выбранным вакансиям' : 'Выберите вакансии слева'}
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
    min-height: 0;
  }

  .pane-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid #f1f5f9;
  }

  .pane-header h2 {
    margin: 0;
    font-size: 22px;
    font-weight: 600;
    color: #1f2937;
  }

  .left-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .badge {
    background: #e0f2fe;
    color: #1DAFF7;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
  }

  .recommendation {
    display: flex;
    align-items: baseline;
    gap: 8px;
    padding-top: 6px;
  }
  .rec-label {
    font-size: 13px;
    font-weight: 700;
    color: #374151;
  }
  .rec-text {
    font-size: 13px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #111827;
    max-width: 100%;
    word-break: break-word;
  }

  .vacancies-list,
  .manual-card,
  .candidates-list {
    flex: 1;
    overflow-y: auto;
    padding-right: 5px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
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
  .vacancy-card:hover { border-color: #1DAFF7; }
  .vacancy-card.selected {
    background: #f0f9ff;
    border-color: #1DAFF7;
    color: #1DAFF7;
  }
  .vacancy-name { font-size: 15px; font-weight: 500; color: #1f2937; }
  .vacancy-card.selected .vacancy-name { color: #1DAFF7; font-weight: 600; }

  .candidate-card {
    padding: 16px 18px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
  }

  .candidate-info { display: flex; flex-direction: column; gap: 12px; }
  .candidate-position { font-size: 15px; font-weight: 500; color: #1f2937; }

  .score-container { display: flex; align-items: center; gap: 12px; }
  .score-bar {
    flex: 1; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden;
  }
  .score-fill { height: 100%; background: #1DAFF7; border-radius: 4px; }
  .score-value { font-size: 14px; font-weight: 600; color: #1DAFF7; min-width: 40px; }

  .empty-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    height: 100%; text-align: center; color: #64748b; padding: 40px 20px;
  }
  .empty-state p { margin: 0 0 8px 0; font-size: 16px; font-weight: 500; color: #374151; }
  .empty-subtitle { font-size: 14px; color: #94a3b8; }

  .search-button {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    padding: 12px 30px; margin: 1rem; background: #1DAFF7; color: white;
    border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer;
    transition: background-color 0.2s ease;
  }
  .search-button:hover:not(:disabled) { background: #0d8dcd; }
  .search-button:disabled { background: #cbd5e1; cursor: not-allowed; }

  .back-btn {
    position: absolute; top: 30px; left: 6.2%;
    padding: 10px 16px; background: white; color: #1DAFF7;
    border: 2px solid #1DAFF7; border-radius: 8px; cursor: pointer;
    font-size: 14px; font-weight: 600; transition: all 0.2s ease;
    display: flex; align-items: center; gap: 8px; z-index: 1000;
    margin-bottom: 1rem;
  }
  .back-btn:hover { background: #1DAFF7; color: white; }

  /* Кнопка-переключатель режима в шапке левой колонки */
  .manual-toggle {
    padding: 8px 12px;
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 700;
    color: #1f2937;
    cursor: pointer;
    transition: border-color .15s ease, background .15s ease;
  }
  .manual-toggle:hover { border-color: #1DAFF7; background: #f0f9ff; }

  /* Стили формы */
  .manual-card {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px;
    gap: 12px;
  }
  
  .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start;}
  .input-group { display: flex; flex-direction: column; height: 100%; gap: 6px; }
  .form-label { font-size: 14px; font-weight: 600; color: #374151; }
  .form-input, .form-textarea {
    width: 100%; padding: 12px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 14px;
    transition: border-color .15s ease; font-family: inherit; box-sizing: border-box; background: #fff;
  }
  .form-input:focus, .form-textarea:focus { outline: none; border-color: #1DAFF7; }
  .form-textarea { resize: vertical; min-height: 120px; }
  .input-hint { font-size: 12px; color: #6b7280; }

  .manual-actions { display: flex; justify-content: flex-end; }
  .manual-search-btn {
    padding: 10px 18px; background: #1DAFF7; color: white; border: none; border-radius: 8px;
    font-size: 14px; font-weight: 700; cursor: pointer; transition: background-color .15s ease;
  }
  .manual-search-btn:hover:not(:disabled) { background: #0d8dcd; }
  .manual-search-btn:disabled { background: #cbd5e1; cursor: not-allowed; }
  .err-text { color: #b91c1c; font-size: 13px; }

  .list-hint { color: #64748b; font-size: 13px; padding: 4px 2px; }
  .list-error { color: #b91c1c; font-size: 13px; padding: 4px 2px; }

  @media (max-width: 900px) {
    .input-row { grid-template-columns: 1fr; }
  }
</style>
