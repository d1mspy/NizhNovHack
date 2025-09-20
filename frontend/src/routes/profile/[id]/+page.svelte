<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  // Данные пользователя из localStorage
  let userData = {
    firstName: '',
    lastName: '',
    gender: '',
    birthDate: '',
    position: '',
    education: '',
    experienceYears: '',
    experienceMonths: '',
    experienceDescription: '',
    hardSkills: '',
    careerPreferences: ''
  };

  onMount(() => {
    // Загружаем данные из localStorage
    const savedUserData = localStorage.getItem('userProfileData');
    if (savedUserData) {
      userData = { ...userData, ...JSON.parse(savedUserData) };
    }

    // Загружаем данные регистрации
    const registrationData = localStorage.getItem('registrationData');
    if (registrationData) {
      const regData = JSON.parse(registrationData);
      userData.firstName = regData.firstName || '';
      userData.lastName = regData.lastName || '';
      userData.gender = regData.gender || '';
      userData.birthDate = regData.birthDate || '';
      userData.position = regData.position || '';
    }
  });

  function saveProfile() {
    // Сохраняем все данные в localStorage
    localStorage.setItem('userProfileData', JSON.stringify(userData));
    
    // Показываем сообщение об успешном сохранении
    alert('Данные успешно сохранены!');
  }

  function goBack() {
    goto('/');
  }

  // Функция для расчета возраста из даты рождения
  const calculateAge = (birthDate: string): string => {
    if (!birthDate) return '';
    
    const birth = new Date(birthDate);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    
    return `${age} лет`;
  };

  // Форматирование даты рождения
  const formatBirthDate = (date: string): string => {
    if (!date) return '';
    return new Date(date).toLocaleDateString('ru-RU');
  };
</script>

<svelte:head>
  <title>Профиль - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <!-- Кнопка назад -->
  <button class="back-btn" on:click={goBack}>
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    Назад
  </button>

  <div class="profile-content">
    <!-- Заголовок -->
    <h1 class="profile-title">Мой профиль</h1>

    <div class="profile-layout">
      <!-- Левая колонка - Основная информация -->
      <div class="main-info-card">
        <div class="avatar-section">
          <div class="avatar-placeholder">
            <!-- Здесь будет ваша картинка -->
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#1DAFF7">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="7" r="4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="user-name">{userData.firstName} {userData.lastName}</h2>
        </div>

        <div class="basic-info">
          <h3 class="info-section-title">Основная информация</h3>
          <div class="info-grid">
            {#if userData.gender}
              <div class="info-item">
                <span class="info-label">Пол:</span>
                <span class="info-value">{userData.gender === 'male' ? 'Мужской' : 'Женский'}</span>
              </div>
            {/if}
            {#if userData.birthDate}
              <div class="info-item">
                <span class="info-label">Дата рождения:</span>
                <span class="info-value">{formatBirthDate(userData.birthDate)}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Возраст:</span>
                <span class="info-value">{calculateAge(userData.birthDate)}</span>
              </div>
            {/if}
            {#if userData.position}
              <div class="info-item">
                <span class="info-label">Должность:</span>
                <span class="info-value">{userData.position}</span>
              </div>
            {/if}
          </div>
        </div>
      </div>

      <!-- Правая колонка - Дополнительная информация -->
      <div class="additional-info-card">
        <h3 class="form-title">Дополнительная информация</h3>

        <form on:submit|preventDefault={saveProfile} class="profile-form">
          <!-- Образование -->
          <div class="form-group">
            <label for="education" class="form-label">Образование</label>
            <input
              id="education"
              type="text"
              bind:value={userData.education}
              placeholder="Например: Высшее техническое, МГУ"
              class="form-input"
            />
          </div>

          <!-- Опыт работы -->
          <div class="form-group">
            <label class="form-label">Опыт работы</label>
            <div class="experience-container">
              <div class="experience-inputs">
                <div class="experience-input-group">
                  <input
                    type="number"
                    bind:value={userData.experienceYears}
                    min="0"
                    max="50"
                    placeholder="0"
                    class="experience-input"
                  />
                  <span class="experience-label">лет</span>
                </div>
                <div class="experience-input-group">
                  <input
                    type="number"
                    bind:value={userData.experienceMonths}
                    min="0"
                    max="11"
                    placeholder="0"
                    class="experience-input"
                  />
                  <span class="experience-label">месяцев</span>
                </div>
              </div>
              <div class="experience-total">
                Всего: <strong>{Math.floor((Number(userData.experienceYears) || 0) + (Number(userData.experienceMonths) || 0) / 12).toFixed(1)}</strong> лет
              </div>
            </div>
          </div>

          <!-- Описание опыта -->
          <div class="form-group">
            <label for="experienceDescription" class="form-label">Описание опыта</label>
            <textarea
              id="experienceDescription"
              bind:value={userData.experienceDescription}
              placeholder="Опишите ваш профессиональный опыт, ключевые проекты и достижения..."
              rows="4"
              class="form-textarea"
            />
          </div>

          <!-- Хард скиллы -->
          <div class="form-group">
            <label for="hardSkills" class="form-label">Хард скиллы (технологии)</label>
            <textarea
              id="hardSkills"
              bind:value={userData.hardSkills}
              placeholder="Перечислите технологии через запятую: JavaScript, React, Python, SQL..."
              rows="3"
              class="form-textarea"
            />
            <div class="input-hint">Указывайте технологии через запятую</div>
          </div>

          <!-- Карьерные предпочтения -->
          <div class="form-group">
            <label for="careerPreferences" class="form-label">Карьерные предпочтения</label>
            <textarea
              id="careerPreferences"
              bind:value={userData.careerPreferences}
              placeholder="Какие направления развития вас интересуют? Какие цели в карьере?"
              rows="3"
              class="form-textarea"
            />
          </div>

          <!-- Кнопка сохранения -->
          <button type="submit" class="save-btn">
            Сохранить изменения
          </button>
        </form>
      </div>
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
    max-width: 1400px;
    margin: 0 auto;
    padding: 70px 40px 40px 40px;
    position: relative;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .back-btn {
    position: absolute;
    top: 30px;
    left: 40px;
    padding: 12px 20px;
    background: white;
    color: #1DAFF7;
    border: 2px solid #1DAFF7;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 1000;
  }

  .back-btn:hover {
    background: #1DAFF7;
    transform: translateY(-2px);
  }

  .back-btn svg {
    width: 18px;
    height: 18px;
  }

  .profile-content {
    display: flex;
    flex-direction: column;
    gap: 35px;
  }

  .profile-title {
    margin: 0 0 20px 0;
    font-size: 42px;
    font-weight: 700;
    color: #1f2937;
    text-align: center;
  }

  .profile-layout {
    display: grid;
    grid-template-columns: 380px 1fr;
    gap: 35px;
    align-items: start;
  }

  .main-info-card {
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
    height: fit-content;
    position: sticky;
    top: 35px;
  }

  .additional-info-card {
    background: white;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
  }

  .avatar-section {
    text-align: center;
    margin-bottom: 35px;
    padding-bottom: 30px;
    border-bottom: 2px solid #f1f5f9;
  }

  .avatar-placeholder {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: #f0f9ff;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid #1DAFF7;
    margin: 0 auto 25px auto;
  }

  .avatar-placeholder svg {
    width: 70px;
    height: 70px;
  }

  .user-name {
    margin: 0;
    font-size: 32px;
    font-weight: 600;
    color: #1f2937;
    line-height: 1.3;
  }

  .basic-info {
    margin-top: 25px;
  }

  .info-section-title {
    margin: 0 0 25px 0;
    font-size: 22px;
    font-weight: 600;
    color: #1f2937;
    padding-bottom: 12px;
    border-bottom: 2px solid #1DAFF7;
  }

  .info-grid {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
  }

  .info-item:last-child {
    border-bottom: none;
  }

  .info-label {
    font-size: 15px;
    font-weight: 600;
    color: #64748b;
    flex-shrink: 0;
  }

  .info-value {
    font-size: 16px;
    color: #1f2937;
    font-weight: 500;
    text-align: right;
    word-break: break-word;
  }

  .form-title {
    margin: 0 0 35px 0;
    font-size: 28px;
    font-weight: 600;
    color: #1f2937;
    text-align: center;
  }

  .profile-form {
    display: flex;
    flex-direction: column;
    gap: 28px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .form-label {
    font-size: 17px;
    font-weight: 600;
    color: #374151;
  }

  .form-input {
    padding: 16px;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    font-size: 16px;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .form-input:focus {
    outline: none;
    border-color: #1DAFF7;
    box-shadow: 0 0 0 3px rgba(29, 175, 247, 0.1);
  }

  .form-textarea {
    padding: 16px;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    font-size: 16px;
    resize: vertical;
    min-height: 130px;
    transition: all 0.2s ease;
    font-family: inherit;
    line-height: 1.5;
  }

  .form-textarea:focus {
    outline: none;
    border-color: #1DAFF7;
    box-shadow: 0 0 0 3px rgba(29, 175, 247, 0.1);
  }

  .experience-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .experience-inputs {
    display: flex;
    gap: 20px;
    align-items: center;
  }

  .experience-input-group {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #f8fafc;
    padding: 12px 16px;
    border-radius: 10px;
    border: 2px solid #e2e8f0;
    transition: all 0.2s ease;
  }

  .experience-input-group:focus-within {
    border-color: #1DAFF7;
    background: white;
  }

  .experience-input {
    width: 70px;
    padding: 8px 12px;
    border: none;
    background: transparent;
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
    text-align: center;
  }

  .experience-input:focus {
    outline: none;
  }

  .experience-label {
    font-size: 14px;
    color: #64748b;
    font-weight: 500;
    min-width: 60px;
  }

  .experience-total {
    font-size: 15px;
    color: #64748b;
    padding: 10px 15px;
    background: #f0f9ff;
    border-radius: 8px;
    border-left: 3px solid #1DAFF7;
  }

  .input-hint {
    font-size: 14px;
    color: #6b7280;
    margin-top: 6px;
    font-style: italic;
  }

  .save-btn {
    padding: 18px;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 15px;
  }

  .save-btn:hover {
    background: #0d8dcd;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(29, 175, 247, 0.3);
  }

  @media (max-width: 1200px) {
    .page-container {
      max-width: 1100px;
      padding: 60px 30px 35px 30px;
    }
    
    .profile-layout {
      grid-template-columns: 340px 1fr;
      gap: 30px;
    }
  }

  @media (max-width: 1024px) {
    .page-container {
      max-width: 900px;
    }
    
    .profile-layout {
      grid-template-columns: 320px 1fr;
      gap: 25px;
    }
  }

  @media (max-width: 900px) {
    .page-container {
      padding: 60px 25px 35px 25px;
    }
    
    .profile-layout {
      grid-template-columns: 1fr;
      gap: 30px;
    }
    
    .main-info-card {
      position: static;
      order: 1;
    }
    
    .additional-info-card {
      order: 2;
    }
  }

  @media (max-width: 768px) {
    .page-container {
      padding: 60px 20px 30px 20px;
    }

    .profile-title {
      font-size: 36px;
    }

    .main-info-card,
    .additional-info-card {
      padding: 30px;
    }

    .experience-inputs {
      flex-direction: column;
      align-items: stretch;
      gap: 15px;
    }

    .experience-input-group {
      justify-content: space-between;
    }
  }

  @media (max-width: 480px) {
    .page-container {
      padding: 55px 15px 25px 15px;
    }

    .back-btn {
      left: 15px;
      padding: 10px 16px;
    }

    .main-info-card,
    .additional-info-card {
      padding: 25px;
    }

    .form-input,
    .form-textarea {
      padding: 14px;
    }

    .save-btn {
      padding: 16px;
      font-size: 16px;
    }
  }
</style>