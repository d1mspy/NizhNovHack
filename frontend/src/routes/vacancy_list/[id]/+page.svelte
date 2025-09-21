<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { get } from 'svelte/store';

  type FitVacancy = {
    id: string;
    name: string;
    score: number;
    reason: string;
  };

  let fits: FitVacancy[] = [];

  let openId: string | null = null;
  const toggleCard = (id: string) => {
    openId = openId === id ? null : id;
  };

  function onDocClick(e: MouseEvent) {
    const t = e.target as HTMLElement;
    if (!t.closest('.vacancy-card')) openId = null;
  }
  function onKey(e: KeyboardEvent) {
    if (e.key === 'Escape') openId = null;
  }

  function goBack() {
    const id = get(page).params.id;
    goto(`/user/${id}`);
  }

  onMount(() => {
    document.addEventListener('click', onDocClick);
    document.addEventListener('keydown', onKey);

    const id = get(page).params.id;
    const raw = sessionStorage.getItem(`vacancyMatch:${id}`);
    if (raw) {
      try {
        const parsed = JSON.parse(raw) as Array<any>;
        fits = (Array.isArray(parsed) ? parsed : [])
          .map((x, i) => ({
            id: String(x.id ?? i),
            name: String(x.name ?? ''),
            score: clamp(Number(x.score ?? 0)),
            reason: String(x.reason ?? '')
          }))
          // фильтруем по score
          .filter((x) => x.score > 65)
          // сортируем по убыванию score
          .sort((a, b) => b.score - a.score);
      } catch {
        fits = [];
      }
    }

    return () => {
      document.removeEventListener('click', onDocClick);
      document.removeEventListener('keydown', onKey);
    };
  });

  const clamp = (n: number) => Math.max(0, Math.min(100, Math.round(n)));
</script>

<svelte:head>
  <title>Подходящие вакансии</title>
</svelte:head>

<div class="page-container">
  <div class="header-row">
    <button class="back-btn" on:click={goBack} type="button" aria-label="Назад на главную">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Назад
    </button>
    <h1 class="page-title">Вам подходят эти вакансии</h1>
  </div>

  {#if fits.length === 0}
    <div class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <p>Пока нет рекомендаций</p>
      <span class="empty-subtitle">Вернитесь на страницу пользователя и запустите «Карьерные перспективы»</span>
    </div>
  {:else}
    <div class="grid">
      {#each fits as v (v.id)}
        <button
          class="vacancy-card"
          on:click={() => toggleCard(v.id)}
          type="button"
          aria-expanded={openId === v.id}
          aria-label={`Вакансия: ${v.name}. Оценка соответствия: ${clamp(v.score)} из 100`}
        >
          <div class="card-top">
            <div class="vacancy-name">{v.name}</div>
            <div class="score-wrap">
              <div class="score-bar" aria-hidden="true">
                <div class="score-fill" style={`width:${clamp(v.score)}%`}></div>
              </div>
              <div class="score-value" aria-label="Оценка">{clamp(v.score)}%</div>
            </div>
          </div>

          {#if openId === v.id}
            <div class="popover" role="dialog" aria-label="Почему эта вакансия подходит">
              <div class="popover-content">{v.reason}</div>
              <div class="popover-arrow" aria-hidden="true"></div>
            </div>
          {/if}
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  :global(body) {
    background: #f8fafc;
    color: #333;
    line-height: 1.5;
  }

  .page-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 20px;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .header-row {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
  }

  .page-title {
    font-size: 28px;
    font-weight: 700;
    color: #1f2937;
  }

  .back-btn {
    padding: 10px 16px;
    background: white;
    color: #1DAFF7;
    border: 2px solid #1DAFF7;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .back-btn:hover {
    background: #1DAFF7;
    color: white;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
  }

  .vacancy-card {
    position: relative;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    text-align: left;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
    cursor: pointer;
  }
  .vacancy-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 26px rgba(0,0,0,0.08);
    border-color: #cbd5e1;
  }

  .card-top { display: grid; gap: 12px; }
  .vacancy-name { font-weight: 600; font-size: 16px; color: #1f2937; }

  .score-wrap {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 10px;
  }
  .score-bar {
    height: 10px;
    background: #f1f5f9;
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
  }
  .score-fill {
    height: 100%;
    background: linear-gradient(90deg, #60a5fa, #22d3ee);
    width: 0%;
    transition: width .35s ease;
  }
  .score-value {
    font-size: 13px;
    font-weight: 700;
    color: #1DAFF7;
    min-width: 40px;
    text-align: right;
  }

  .popover {
    position: absolute;
    left: 16px; right: 16px; bottom: -10px;
    transform: translateY(100%);
    background: #0f172a;
    color: #e5e7eb;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    border: 1px solid #1f2937;
    z-index: 5;
  }
  .popover-content { margin: 0; }
  .popover-arrow {
    position: absolute;
    top: -6px; left: 28px;
    width: 12px; height: 12px;
    background: #0f172a;
    border-left: 1px solid #1f2937;
    border-top: 1px solid #1f2937;
    transform: rotate(45deg);
  }

  .empty-state {
    text-align: center;
    padding: 48px 20px;
    color: #64748b;
  }
  .empty-state svg { margin-bottom: 16px; opacity: .5; }
  .empty-state p { margin: 0 0 8px 0; font-size: 18px; font-weight: 500; color: #64748b; }
  .empty-subtitle { font-size: 14px; color: #94a3b8; }
</style>
