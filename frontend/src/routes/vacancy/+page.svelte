<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  interface Vacancy {
    id: number;
    title: string;
    fileName?: string;
  }

  let vacancies: Vacancy[] = [];
  let vacancyTitle = '';
  let pdfFile: File | null = null;
  let nextId = 1;

  onMount(() => {
    const savedVacancies = localStorage.getItem('vacancies');
    const savedNextId = localStorage.getItem('nextId');
    
    if (savedVacancies) {
      vacancies = JSON.parse(savedVacancies);
    }
    
    if (savedNextId) {
      nextId = parseInt(savedNextId);
    }
  });

  function addVacancy() {
    if (!vacancyTitle.trim()) return;

    const newVacancy: Vacancy = {
      id: nextId++,
      title: vacancyTitle.trim(),
      fileName: pdfFile?.name
    };

    vacancies = [...vacancies, newVacancy];
    vacancyTitle = '';
    pdfFile = null;
    
    localStorage.setItem('vacancies', JSON.stringify(vacancies));
    localStorage.setItem('nextId', nextId.toString());
  }

  function deleteVacancy(id: number) {
    vacancies = vacancies.filter(v => v.id !== id);
    localStorage.setItem('vacancies', JSON.stringify(vacancies));
  }

  function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      pdfFile = input.files[0];
    }
  }

  function goToCandidateSearch() {
    goto('/candidates');
  }
</script>

<svelte:head>
  <title>Вакансии - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <button class="search-candidates-btn" on:click={goToCandidateSearch}>
    Поиск кандидатов
  </button>

  <div class="add-vacancy-container">
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
      disabled={!vacancyTitle.trim()}
      class="add-btn"
    >
      Добавить
    </button>
  </div>

  <!-- Список вакансий -->
  <div class="vacancies-section">
    <h3>Вакансии ({vacancies.length})</h3>
    
    {#if vacancies.length > 0}
      <div class="vacancies-list">
        {#each vacancies as vacancy (vacancy.id)}
          <div class="vacancy-item">
            <span class="vacancy-title">{vacancy.title}</span>
            <div class="vacancy-actions">
              {#if vacancy.fileName}
                <span class="file-badge">PDF</span>
              {/if}
              <button
                on:click={() => deleteVacancy(vacancy.id)}
                class="delete-btn"
                title="Удалить"
              >
                ×
              </button>
            </div>
          </div>
        {/each}
      </div>
    {:else}
      <div class="empty-state">
        <p>Нет добавленных вакансий</p>
      </div>
    {/if}
  </div>
</div>

<style>
  :global(body) {
    background: #ffffff;
    color: #333;
    line-height: 1.5;
  }

  .page-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 40px 20px;
  }

  .search-candidates-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    padding: 8px 16px;
    background: transparent;
    color: #0056b3;
    border: 1px solid #0056b3;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
  }

  .search-candidates-btn:hover {
    background: #0056b3;
    color: white;
  }

  .add-vacancy-container {
    background: #fafafa;
    padding: 30px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    margin-bottom: 30px;
  }

  .add-vacancy-container h2 {
    margin: 0 0 25px 0;
    font-size: 20px;
    font-weight: 600;
    color: #333;
    text-align: center;
  }

  .input-group {
    margin-bottom: 20px;
  }

  .input-field {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    box-sizing: border-box;
    transition: border-color 0.2s ease;
  }

  .input-field:focus {
    outline: none;
    border-color: #0056b3;
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
    padding: 12px;
    border: 1px dashed #ddd;
    border-radius: 6px;
    text-align: center;
    color: #666;
    transition: all 0.2s ease;
  }

  .file-text:hover {
    border-color: #0056b3;
    color: #0056b3;
  }

  .add-btn {
    width: 100%;
    padding: 12px;
    background: #0056b3;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .add-btn:hover:not(:disabled) {
    background: #004494;
  }

  .add-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .vacancies-section {
    background: #fafafa;
    padding: 30px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
  }

  .vacancies-section h3 {
    margin: 0 0 20px 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }

  .vacancies-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .vacancy-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background: white;
    border-radius: 6px;
    border: 1px solid #e0e0e0;
  }

  .vacancy-title {
    font-weight: 500;
    color: #333;
  }

  .vacancy-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .file-badge {
    padding: 4px 8px;
    background: #e8f4ff;
    color: #0056b3;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
  }

  .delete-btn {
    padding: 4px 8px;
    background: transparent;
    color: #ff4444;
    border: 1px solid #ff4444;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    line-height: 1;
    transition: all 0.2s ease;
  }

  .delete-btn:hover {
    background: #ff4444;
    color: white;
  }

  .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #999;
  }

  @media (max-width: 768px) {
    .page-container {
      padding: 20px 15px;
    }

    .search-candidates-btn {
      position: static;
      margin-bottom: 20px;
      width: 100%;
    }

    .add-vacancy-container,
    .vacancies-section {
      padding: 20px;
    }
  }
</style>