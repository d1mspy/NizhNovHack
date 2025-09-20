<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  interface Vacancy {
    id: string;
    name: string;
  }

  let vacancies: Vacancy[] = [];
  let vacancyTitle = '';
  let pdfFile: File | null = null;
  let loading = false;
  let saving = false;
  let err = '';

  const fetchVacancies = async () => {
    loading = true; err = '';
    try {
      const res = await fetch('/api/vacancy');
      if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
      vacancies = await res.json();
    } catch (e) {
      err = e instanceof Error ? e.message : 'Неизвестная ошибка';
    } finally {
      loading = false;
    }
  };

  onMount(fetchVacancies);

  function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      pdfFile = input.files[0];
      if (!vacancyTitle.trim()) {
        const name = pdfFile.name;
        const dot = name.lastIndexOf('.');
        vacancyTitle = dot > 0 ? name.slice(0, dot) : name;
      }
    }
  }

  const addVacancy = async () => {
    if (!pdfFile) return;
    const name = vacancyTitle.trim() || (pdfFile ? (pdfFile.name.replace(/\.[^.]+$/, '')) : '');
    if (!name) return;

    saving = true; err = '';
    try {
      const fd = new FormData();
      fd.append('name', name);
      fd.append('vacancy', pdfFile);
      const res = await fetch('/api/vacancy', { method: 'POST', body: fd });
      if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
      vacancyTitle = '';
      pdfFile = null;
      const fileInput = document.querySelector('.file-input') as HTMLInputElement | null;
      if (fileInput) fileInput.value = '';
      await fetchVacancies();
    } catch (e) {
      err = e instanceof Error ? e.message : 'Неизвестная ошибка';
    } finally {
      saving = false;
    }
  };

  const deleteVacancy = async (id: string) => {
    err = '';
    try {
      const res = await fetch(`/api/vacancy/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`));
      vacancies = vacancies.filter(v => v.id !== id);
    } catch (e) {
      err = e instanceof Error ? e.message : 'Неизвестная ошибка';
    }
  };

  function goToCandidateSearch() {
    goto('/candidates');
  }
</script>


<svelte:head>
  <title>Вакансии - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <button class="search-candidates-btn" on:click={goToCandidateSearch}>
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    Поиск кандидатов
  </button>

  <div class="main-content">
    <div class="section-card">
      <h2>Добавить вакансию</h2>
      
      <div class="input-group">
        <input
          type="text"
          bind:value={vacancyTitle}
          placeholder="Название вакансии"
          class="input-field"
        />
      </div>

      <div class="input-group">
        <label class="file-label">
          <input
            type="file"
            accept=".pdf"
            on:change={handleFileUpload}
            class="file-input"
          />
          <span class="file-text">
            {pdfFile ? pdfFile.name : 'Загрузить описание (PDF)'}
          </span>
        </label>
      </div>

      <button
        on:click={addVacancy}
        disabled={saving || !pdfFile}
        class="primary-btn"
      >
        {saving ? 'Загружаем…' : 'Добавить вакансию'}
      </button>
    </div>
    <!-- Список вакансий -->
    <div class="section-card">
      <div class="section-header">
        <h3>Мои вакансии</h3>
        <span class="badge">{vacancies.length}</span>
      </div>
      
      {#if vacancies.length > 0}
        <div class="vacancies-list">
          {#each vacancies as vacancy (vacancy.id)}
            <div class="vacancy-item">
              <div class="vacancy-info">
                <span class="vacancy-title">{vacancy.name}</span>
              </div>
              <button
                on:click={() => deleteVacancy(vacancy.id)}
                class="delete-btn"
                title="Удалить вакансию"
                aria-label="Удалить вакансию"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
          {/each}
            {#if loading}<p>Загружаем список…</p>{/if}
            {#if err}<p style="color:#b91c1c">{err}</p>{/if}
        </div>
      {:else}
        <div class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>Нет добавленных вакансий</p>
          <span class="empty-subtitle">Добавьте первую вакансию</span>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  :global(body) {
    background: #f8fafc;
    color: #333;
    line-height: 1.5;
  }

  .page-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 40px 20px;
    position: relative;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .search-candidates-btn {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(29, 175, 247, 0.3);
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 1000;
  }

  .search-candidates-btn:hover {
    background: #0d8dcd;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(29, 175, 247, 0.4);
  }

  .search-candidates-btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(29, 175, 247, 0.3);
  }

  .search-candidates-btn svg {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }

  .main-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding-top: 10px;
  }

  .section-card {
    background: white;
    padding: 32px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
  }

  .section-card h2 {
    margin: 0 0 24px 0;
    font-size: 24px;
    font-weight: 600;
    color: #1f2937;
    text-align: center;
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }

  .section-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: #1f2937;
  }

  .badge {
    background: #e0f2fe;
    color: #1DAFF7;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
  }

  .input-group {
    margin-bottom: 20px;
  }

  .input-field {
    width: 100%;
    padding: 14px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 16px;
    box-sizing: border-box;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .input-field:focus {
    outline: none;
    border-color: #1DAFF7;
  }

  .file-label {
    display: block;
    cursor: pointer;
  }

  .file-input {
    display: none;
  }

  .file-text {
    display: block;
    padding: 14px;
    border: 2px dashed #e2e8f0;
    border-radius: 8px;
    text-align: center;
    color: #64748b;
    transition: all 0.2s ease;
    font-size: 16px;
  }

  .file-text:hover {
    border-color: #1DAFF7;
    color: #1DAFF7;
    background: #f0f9ff;
  }

  .primary-btn {
    width: 100%;
    padding: 16px;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .primary-btn:hover:not(:disabled) {
    background: #0d8dcd;
    transform: translateY(-1px);
  }

  .primary-btn:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
    transform: none;
  }

  .vacancies-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .vacancy-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    background: #f8fafc;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease;
  }

  .vacancy-item:hover {
    border-color: #cbd5e1;
    background: #f1f5f9;
  }

  .vacancy-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .vacancy-title {
    font-weight: 500;
    color: #1f2937;
    font-size: 16px;
  }

  .delete-btn {
    padding: 8px;
    background: transparent;
    color: #ef4444;
    border: 1px solid #fecaca;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .delete-btn:hover {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
  }

  .empty-state {
    text-align: center;
    padding: 48px 20px;
    color: #64748b;
  }

  .empty-state svg {
    margin-bottom: 16px;
    opacity: 0.5;
  }

  .empty-state p {
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 500;
    color: #64748b;
  }

  .empty-subtitle {
    font-size: 14px;
    color: #94a3b8;
  }

  @media (max-width: 768px) {
    .page-container {
      padding: 30px 16px;
    }

    .search-candidates-btn {
      top: 15px;
      right: 15px;
      padding: 10px 16px;
      font-size: 13px;
    }

    .search-candidates-btn svg {
      width: 14px;
      height: 14px;
    }

    .section-card {
      padding: 24px;
    }

    .section-card h2 {
      font-size: 20px;
    }

    .section-header h3 {
      font-size: 18px;
    }
  }

  @media (max-width: 480px) {
    .page-container {
      padding: 25px 12px;
    }

    .search-candidates-btn {
      top: 12px;
      right: 12px;
      padding: 8px 14px;
      font-size: 12px;
    }

    .section-card {
      padding: 20px;
    }

    .input-field,
    .file-text {
      padding: 12px;
    }

    .primary-btn {
      padding: 14px;
    }

    .vacancy-item {
      padding: 12px;
    }
  }
</style>