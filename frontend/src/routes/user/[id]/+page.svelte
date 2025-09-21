<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { get } from 'svelte/store';

  type Step = 'idle' | 'skills';
  let step: Step = 'idle';

  let isMatching = false;

  type Skills = {
    level?: number | null;
    discipline?: number | null;
    focus?: number | null;
    speed?: number | null;
    flexibility?: number | null;
    experience?: number | null;
  };

  let skills: Skills | null = null;

  function goToProfile() {
    const id = get(page).params.id;
    goto(`/profile/${id}`);
  }

  function backToIdle() {
    const id = get(page).params.id;
    goto(`/user/${id}`);
  }

  const order: Array<keyof Skills> = [
    'level','discipline','focus','speed','flexibility','experience'
  ];
  const rand40_92 = () => Math.floor(40 + Math.random() * 52);
  const labels = {
    level: 'Уровень', discipline: 'Опыт в индустрии', focus: 'Индекс достижений',
    speed: 'Уровень образования', flexibility: 'Коэффициент карьерного прогресса', experience: 'Стабильность'
  } as const;
  
  function bars() {
    const s = (skills ?? getSkills()) as Required<Skills>;
    return order.map((k) => ({
      key: k,
      name: labels[k],
      value: s[k]!
    }));
  }
  $: all = bars();

  async function proceedToChat() {
    const id = get(page).params.id;
    try {
      const res = await fetch(`/api/start_chat/${id}`, { method: 'PUT' });
      if (res.ok) {
        const raw = (await res.text()).trim();
        const text = raw.replace(/^"(.+)"$/, '$1');
        sessionStorage.setItem(`chatInit:${id}`, text);
      }
    } catch { /* игнор */ }
    await goto(`/career-chat/${id}`);
  }

  function getSkills(): Required<Skills> {
    return {
      level:       rand40_92(),
      discipline:  rand40_92(),
      focus:       rand40_92(),
      speed:       rand40_92(),
      flexibility: rand40_92(),
      experience:  rand40_92()
    };
  }

  async function goToCareerProspects() {
    const id = get(page).params.id;
    if (isMatching) return;

    isMatching = true;
    try {
      const res = await fetch(`/api/${id}/matching`, { method: 'PUT' });
      if (!res.ok) {
        const errText = await res.text().catch(() => '');
        throw new Error(errText || `HTTP ${res.status}`);
      }
      const data = await res.json();
      const normalized = (Array.isArray(data) ? data : []).map((x: any, i: number) => ({
        id: String(i),
        name: String(x.vac_name ?? ''),
        score: Math.max(0, Math.min(100, Math.round(Number(x.score) || 0))),
        reason: String(x.reasoning_report ?? '')
      }));

      const uid = get(page).params.id;
      sessionStorage.setItem(`vacancyMatch:${uid}`, JSON.stringify(normalized));
      await goto(`/vacancy_list/${uid}`);
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Неизвестная ошибка';
      alert(`Не удалось получить карьерные перспективы: ${msg}`);
    } finally {
      isMatching = false;
    }
  }

  function goToCareerConsultant() {
    skills = getSkills();
    step = 'skills';
  }
</script>

<svelte:head>
  <title>Главная - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <button class="profile-btn" on:click={goToProfile}>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="12" cy="7" r="4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    Профиль
  </button>

  <div class="main-content">
    <div class="welcome-section">
      <h1>Готовы к консультации?</h1>
    </div>

    {#if step === 'idle'}
      <div class="buttons-container">
        <button class="feature-btn" on:click={goToCareerConsultant}>
          <div class="feature-content">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="feature-text">
              <span class="feature-title">Карьерный консультант</span>
              <span class="feature-description">Сначала оценим ваши параметры</span>
            </div>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" class="arrow-icon">
              <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </button>

        <button
          class="feature-btn"
          on:click={goToCareerProspects}
          disabled={isMatching}
          aria-busy={isMatching}
          aria-label="Карьерные перспективы"
          title="Карьерные перспективы"
        >
          <div class="feature-content">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="feature-text">
              <span class="feature-title">Карьерные перспективы</span>
              <span class="feature-description">{isMatching ? 'Подбираем…' : 'Анализ роста и развития'}</span>
            </div>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" class="arrow-icon" aria-hidden="true">
              <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </button>
      </div>

    {:else if step === 'skills'}
      <div class="skills-panel">
        <div class="skills-header">
          <h2>Ваши характеристики</h2>
        </div>

        <!-- Карточки со шкалами -->
        <div class="cards-grid">
          {#each all as item}
            <div class="skill-card" aria-label={`${item.name}: ${item.value} из 100`}>
              <div class="skill-head">
                <span class="skill-name">{item.name}</span>
                <span class="skill-value">{item.value}</span>
              </div>
              <div class="hbar-track">
                <div class="hbar-fill" style:width={`${item.value}%`}></div>
              </div>
              <div class="hbar-scale">
                <span>0</span><span>25</span><span>50</span><span>75</span><span>100</span>
              </div>
            </div>
          {/each}
        </div>

        <!-- CTA под карточками -->
        <div class="cta-row">
          <button class="btn-secondary" on:click={backToIdle}>Назад</button>
          <button class="btn-primary" on:click={proceedToChat}>Перейти в чат</button>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  :global(body) { background: #f8fafc; color: #333; line-height: 1.5; }

  .page-container { max-width: 900px; margin: 0 auto; padding: 80px 30px 50px; position: relative; min-height: 100vh; box-sizing: border-box; }

  .profile-btn { position: fixed; top: 25px; left: 25px; padding: 14px 20px; background: #fff; color: #1DAFF7; border: 2px solid #1DAFF7; border-radius: 12px; cursor: pointer; font-size: 16px; font-weight: 600; transition: all .3s; box-shadow: 0 6px 20px rgba(29,175,247,.25); display: flex; align-items: center; gap: 10px; z-index: 1000; }
  .profile-btn:hover { background: #1DAFF7; color: #fff; transform: translateY(-3px); box-shadow: 0 8px 25px rgba(29,175,247,.35); }

  .main-content { display: flex; flex-direction: column; gap: 40px; align-items: center; padding-top: 30px; }
  .welcome-section { text-align: center; max-width: 600px; }
  .welcome-section h1 { margin: 0; font-size: 38px; font-weight: 800; color: #1f2937; background: #1DAFF7; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

  .buttons-container { display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 520px; }
  .feature-btn { width: 100%; padding: 28px; background: #fff; border: 2px solid #e2e8f0; border-radius: 16px; cursor: pointer; transition: all .3s; text-align: left; }
  .feature-btn:hover { border-color: #1DAFF7; transform: translateY(-3px); box-shadow: 0 12px 35px rgba(29,175,247,.2); }
  .feature-content { display: flex; align-items: center; gap: 20px; width: 100%; }
  .feature-btn svg:first-child { color: #1DAFF7; flex-shrink: 0; }
  .feature-title { font-size: 20px; font-weight: 700; color: #1f2937; }
  .feature-description { font-size: 15px; color: #64748b; }

  /* ===== SKILLS (cards) ===== */
  .skills-panel { width: 100%; background: #fff; border: 2px solid #e2e8f0; border-radius: 18px; padding: 22px; box-shadow: 0 12px 30px rgba(29,175,247,.08); }
  .skills-header h2 { margin: 0 0 6px 0; font-size: 22px; color: #0f172a; }
  .skills-header p { margin: 0; color: #64748b; }

  .cards-grid { margin-top: 18px; display: grid; grid-template-columns: repeat(2, minmax(260px, 1fr)); gap: 16px; }
  @media (max-width: 640px) { .cards-grid { grid-template-columns: 1fr; } }

  .skill-card { border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 14px; background: #fff; transition: box-shadow .2s, transform .2s, border-color .2s; }
  .skill-card:hover { border-color: #cfeafe; transform: translateY(-1px); box-shadow: 0 8px 20px rgba(29,175,247,.12); }

  .skill-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
  .skill-name { font-weight: 700; color: #0f172a; }
  .skill-value { font-weight: 800; color: #0f172a; }

  .hbar-track { width: 100%; height: 10px; border-radius: 999px; background: linear-gradient(90deg, #eef2f7 0%, #e6edf7 100%); overflow: hidden; border: 1px solid #e2e8f0; }
  .hbar-fill { height: 100%; width: 0; background: linear-gradient(90deg, #60a5fa 0%, #1DAFF7 100%); transition: width .45s ease; }

  .hbar-scale { display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; margin-top: 6px; }

  .cta-row { margin-top: 18px; display: flex; justify-content: center; gap: 10px; }
  .btn-primary, .btn-secondary { padding: 10px 16px; border-radius: 12px; font-weight: 700; border: 2px solid transparent; cursor: pointer; transition: all .2s; }
  .btn-primary { background: #1DAFF7; color: #fff; box-shadow: 0 6px 20px rgba(29,175,247,.25); }
  .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(29,175,247,.33); }
  .btn-secondary { background: #fff; color: #1DAFF7; border-color: #1DAFF7; }
  .btn-secondary:hover { background: #e6f6fe; }
</style>
