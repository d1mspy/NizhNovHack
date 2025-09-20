<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  type Sex = 'male' | 'female' | '';
  interface UserData {
    firstName: string;
    lastName: string;
    gender: Sex;
    birthDate: string; // YYYY-MM-DD
    position: string;
    education: string;
    experienceYears: number;
    experienceMonths: number;
    experienceDescription: string;
    hardSkills: string;          // textarea (CSV)
    careerPreferences: string;   // локальное поле, на бэк не шлём
  }

  let userData: UserData = {
    firstName: '',
    lastName: '',
    gender: '',
    birthDate: '',
    position: '',
    education: '',
    experienceYears: 0,
    experienceMonths: 0,
    experienceDescription: '',
    hardSkills: '',
    careerPreferences: ''
  };

  let loading = false;   // загрузка профиля
  let saving  = false;   // сохранение профиля
  let errorMsg = '';     // текст ошибки (загрузка/сохранение)

  const toCsv = (arr: string[] | null | undefined) =>
    (arr ?? []).join(', ');

  const fromCsv = (text: string): string[] =>
    text
      .split(/[,\n;]+/g)
      .map((s) => s.trim())
      .filter(Boolean);

  const toISOyyyyMMdd = (d: string) => {
    // ожидается вход типа 'YYYY-MM-DD' или валидная дата
    if (!d) return '';
    // если уже YYYY-MM-DD — вернём как есть
    if (/^\d{4}-\d{2}-\d{2}$/.test(d)) return d;
    const date = new Date(d);
    if (Number.isNaN(date.getTime())) return '';
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  };

  const loadUser = async (id: string) => {
    loading = true;
    errorMsg = '';
    try {
      const res = await fetch(`/api/user/${id}`, { method: 'GET' });
      if (!res.ok) {
        const t = await res.text().catch(() => '');
        throw new Error(t || `Ошибка загрузки профиля: ${res.status}`);
      }
      const data = await res.json() as {
        id: string;
        first_name: string;
        last_name: string;
        sex: 'male' | 'female';
        birth_date: string;
        current_position: string;
        education?: string | null;
        experience_years?: number | null;
        experience_months?: number | null;
        experience_total_months?: number | null; // служебное
        experience_description?: string | null;
        hard_skills?: string[] | null;
        created_at?: string;
        updated_at?: string;
      };

      // Маппинг в локальное состояние (camelCase):
      userData = {
        firstName: data.first_name ?? '',
        lastName: data.last_name ?? '',
        gender: (data.sex ?? '') as Sex,
        birthDate: toISOyyyyMMdd(data.birth_date ?? ''),
        position: data.current_position ?? '',
        education: data.education ?? '',
        experienceYears: data.experience_years ?? 0,
        experienceMonths: data.experience_months ?? 0,
        experienceDescription: data.experience_description ?? '',
        hardSkills: toCsv(data.hard_skills),
        careerPreferences: userData.careerPreferences // не приходит с бэка
      };

      // обновим localStorage как кэш
      localStorage.setItem('userProfileData', JSON.stringify(userData));
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Неизвестная ошибка';
      errorMsg = msg;
      console.error('Load user error:', e);
    } finally {
      loading = false;
    }
  };

  onMount(() => {
    const id = $page.params.id;

    // 1) локальный кэш (покажем сразу)
    const savedUserData = localStorage.getItem('userProfileData');
    if (savedUserData) {
      try {
        const parsed = JSON.parse(savedUserData) as Partial<UserData>;
        userData = { ...userData, ...parsed };
      } catch { /* ignore */ }
    }

    // 2) «подтягиваем» стартовые данные регистрации (если есть)
    const registrationData = localStorage.getItem('registrationData');
    if (registrationData) {
      try {
        const regData = JSON.parse(registrationData) as Partial<UserData>;
        userData.firstName = regData.firstName ?? userData.firstName;
        userData.lastName = regData.lastName ?? userData.lastName;
        userData.gender = (regData.gender as Sex) ?? userData.gender;
        userData.birthDate = regData.birthDate ?? userData.birthDate;
        userData.position = regData.position ?? userData.position;
      } catch { /* ignore */ }
    }

    // 3) авторитетная загрузка с бэка
    if (id) loadUser(id);
  });

  async function saveProfile() {
    const id = $page.params.id;
    if (!id) return;

    saving = true;
    errorMsg = '';

    // Маппинг в snake_case payload
    const payload = {
      first_name: userData.firstName.trim(),
      last_name: userData.lastName.trim(),
      sex: userData.gender || undefined, // '' -> undefined (можно опустить)
      birth_date: toISOyyyyMMdd(userData.birthDate) || undefined,
      current_position: userData.position.trim() || undefined,
      education: userData.education.trim() || undefined,
      experience_years: Number.isFinite(userData.experienceYears) ? userData.experienceYears : 0,
      experience_months: Number.isFinite(userData.experienceMonths) ? userData.experienceMonths : 0,
      experience_description: userData.experienceDescription.trim() || undefined,
      hard_skills: fromCsv(userData.hardSkills) // массив строк
      // не отправляем: id, experience_total_months, created_at, updated_at
    };

    try {
      const res = await fetch(`/api/user/update/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const t = await res.text().catch(() => '');
        throw new Error(t || `Ошибка сохранения профиля: ${res.status}`);
      }

      // на успех — обновим кэш
      localStorage.setItem('userProfileData', JSON.stringify(userData));
      alert('Данные успешно сохранены!');
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Неизвестная ошибка';
      errorMsg = msg;
      console.error('Save user error:', e);
    } finally {
      saving = false;
    }
  }

  function goBack() {
    const id = $page.params.id;
    goto(`/user/${id}`);
  }

  // Возраст по дате рождения (для отображения)
  const calculateAge = (birthDate: string): string => {
    if (!birthDate) return '';
    const birth = new Date(birthDate);
    if (Number.isNaN(birth.getTime())) return '';
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) age--;
    return `${age} лет`;
  };

  const formatBirthDate = (date: string): string => {
    if (!date) return '';
    const d = new Date(date);
    return Number.isNaN(d.getTime()) ? '' : d.toLocaleDateString('ru-RU');
  };

  const totalExperienceYears = () =>
    (userData.experienceYears || 0) + (userData.experienceMonths || 0) / 12;
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

        {#if loading}
          <div class="experience-total" role="status">Загружаем профиль…</div>
        {/if}

        {#if errorMsg}
          <div class="error-banner" role="alert">{errorMsg}</div>
        {/if}

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
            <fieldset class="experience-container" aria-describedby="exp-hint">
              <legend class="form-label">Опыт работы</legend>

              <div class="experience-inputs">
                <div class="experience-input-group">
                  <input
                    id="exp-years"
                    type="number"
                    bind:value={userData.experienceYears}
                    min="0"
                    max="50"
                    placeholder="0"
                    class="experience-input"
                    aria-label="Опыт работы в годах"
                  />
                  <span class="experience-label">лет</span>
                </div>

                <div class="experience-input-group">
                  <input
                    id="exp-months"
                    type="number"
                    bind:value={userData.experienceMonths}
                    min="0"
                    max="11"
                    placeholder="0"
                    class="experience-input"
                    aria-label="Опыт работы в месяцах"
                  />
                  <span class="experience-label">месяцев</span>
                </div>
              </div>

              <div id="exp-hint" class="experience-total">
                Всего: <strong>{totalExperienceYears().toFixed(1)}</strong> лет
              </div>
            </fieldset>
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
            ></textarea>
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
            ></textarea>
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
            ></textarea>
          </div>

          <!-- Кнопка сохранения -->
          <button type="submit" class="save-btn" disabled={saving || loading}>
            {saving ? 'Сохраняем…' : 'Сохранить изменения'}
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
    color: white;
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
  }

  .experience-container {
    border: 0;
    padding: 0;
    margin: 0;
    display: flex;
    display: flex;
    flex-direction: column;
    gap: 15px;
    min-inline-size: auto;
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

  
  .error-banner {
    margin: 10px 0 20px;
    padding: 12px 16px;
    border-left: 4px solid #ef4444;
    background: #fee2e2;
    color: #991b1b;
    border-radius: 8px;
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