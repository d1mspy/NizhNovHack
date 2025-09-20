<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { get } from 'svelte/store';

  function goToProfile() {
    const id = get(page).params.id;
    goto(`/profile/${id}`);
  }

  function goToCareerConsultant() {
    goto('/career-chat');
  }

  function goToCareerProspects() {
    goto('/career-prospects');
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
      <h1>Добро пожаловать!</h1>
      <p class="welcome-subtitle">Выберите интересующий вас раздел</p>
    </div>

    <div class="buttons-container">
      <button class="feature-btn" on:click={goToCareerConsultant}>
        <div class="feature-content">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="feature-text">
            <span class="feature-title">Карьерный консультант</span>
            <span class="feature-description">Персональные рекомендации по развитию карьеры</span>
          </div>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" class="arrow-icon">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </button>

      <button class="feature-btn" on:click={goToCareerProspects}>
        <div class="feature-content">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="feature-text">
            <span class="feature-title">Карьерные перспективы</span>
            <span class="feature-description">Анализ возможностей роста и развития</span>
          </div>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" class="arrow-icon">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </button>
    </div>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f8fafc;
    color: #333;
    line-height: 1.5;
  }

  .page-container {
    max-width: 650px;
    margin: 0 auto;
    padding: 80px 30px 50px 30px;
    position: relative;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .profile-btn {
    position: fixed;
    top: 25px;
    left: 25px;
    padding: 14px 20px;
    background: white;
    color: #1DAFF7;
    border: 2px solid #1DAFF7;
    border-radius: 12px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(29, 175, 247, 0.25);
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 1000;
  }

  .profile-btn:hover {
    background: #1DAFF7;
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(29, 175, 247, 0.35);
  }

  .profile-btn:active {
    transform: translateY(0);
  }

  .profile-btn svg {
    width: 22px;
    height: 22px;
    flex-shrink: 0;
  }

  .main-content {
    display: flex;
    flex-direction: column;
    gap: 50px;
    align-items: center;
    padding-top: 30px;
  }

  .welcome-section {
    text-align: center;
    max-width: 500px;
  }

  .welcome-section h1 {
    margin: 0 0 16px 0;
    font-size: 42px;
    font-weight: 700;
    color: #1f2937;
    background: #1DAFF7;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .welcome-subtitle {
    margin: 0;
    font-size: 20px;
    color: #64748b;
    line-height: 1.6;
    font-weight: 400;
  }

  .buttons-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    max-width: 520px;
  }

  .feature-btn {
    width: 100%;
    padding: 30px;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
  }

  .feature-btn:hover {
    border-color: #1DAFF7;
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(29, 175, 247, 0.2);
  }

  .feature-btn:active {
    transform: translateY(0);
  }

  .feature-content {
    display: flex;
    align-items: center;
    gap: 20px;
    width: 100%;
  }

  .feature-btn svg:first-child {
    color: #1DAFF7;
    flex-shrink: 0;
  }

  .feature-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .feature-title {
    font-size: 22px;
    font-weight: 600;
    color: #1f2937;
  }

  .feature-description {
    font-size: 16px;
    color: #64748b;
    line-height: 1.5;
  }

  .arrow-icon {
    color: #cbd5e1;
    transition: color 0.3s ease;
    flex-shrink: 0;
  }

  .feature-btn:hover .arrow-icon {
    color: #1DAFF7;
  }

  @media (max-width: 768px) {
    .page-container {
      padding: 70px 20px 40px 20px;
    }

    .profile-btn {
      top: 20px;
      left: 20px;
      padding: 12px 18px;
      font-size: 15px;
    }

    .profile-btn svg {
      width: 20px;
      height: 20px;
    }

    .main-content {
      gap: 40px;
    }

    .welcome-section h1 {
      font-size: 36px;
    }

    .welcome-subtitle {
      font-size: 18px;
    }

    .feature-btn {
      padding: 25px;
    }

    .feature-title {
      font-size: 20px;
    }

    .feature-description {
      font-size: 15px;
    }
  }

  @media (max-width: 480px) {
    .page-container {
      padding: 65px 16px 35px 16px;
    }

    .profile-btn {
      top: 16px;
      left: 16px;
      padding: 10px 16px;
      font-size: 14px;
    }

    .welcome-section h1 {
      font-size: 32px;
    }

    .welcome-subtitle {
      font-size: 16px;
    }

    .feature-content {
      gap: 16px;
    }

    .feature-btn {
      padding: 22px;
    }

    .feature-btn svg:first-child {
      width: 28px;
      height: 28px;
    }

    .arrow-icon {
      width: 18px;
      height: 18px;
    }
  }
</style>