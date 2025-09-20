<script lang="ts">
  import { goto } from '$app/navigation';

  let formData = {
    firstName: '',
    lastName: '',
    gender: '',
    birthDate: '',
    position: ''
  };

  let errors = {
    firstName: '',
    lastName: '',
    gender: '',
    birthDate: '',
    position: ''
  };

  const validateForm = (): boolean => {
    let isValid = true;
    errors = {
      firstName: '',
      lastName: '',
      gender: '',
      birthDate: '',
      position: ''
    };

    if (!formData.firstName.trim()) {
      errors.firstName = 'Имя обязательно';
      isValid = false;
    }

    if (!formData.lastName.trim()) {
      errors.lastName = 'Фамилия обязательна';
      isValid = false;
    }

    if (!formData.gender) {
      errors.gender = 'Выберите пол';
      isValid = false;
    }

    if (!formData.birthDate) {
      errors.birthDate = 'Дата рождения обязательна';
      isValid = false;
    } else {
      const birthDate = new Date(formData.birthDate);
      const today = new Date();
      const age = today.getFullYear() - birthDate.getFullYear();
    }

    if (!formData.position.trim()) {
      errors.position = 'Должность обязательна';
      isValid = false;
    }

    return isValid;
  };

  const handleSubmit = async (): Promise<void> => {
    if (validateForm()) {
      // Здесь можно добавить сохранение данных или API запрос
      console.log('Данные формы:', formData);
      
      try {
        await goto('/user');
      } catch (error) {
        console.error('Navigation error:', error);
      }
    }
  };

  const goBack = (): void => {
    goto('/');
  };

  function goToLogin() {
    goto('/login');
  }
</script>

<svelte:head>
  <title>Регистрация - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <div class="registration-container">
    <div class="header">
      <button class="back-btn" on:click={goBack}>← Назад</button>
      <h1>Регистрация</h1>
    </div>

    <form on:submit|preventDefault={handleSubmit} class="form">
      <div class="form-row">
        <div class="input-group">
          <label for="firstName" class="input-label">Имя *</label>
          <input
            id="firstName"
            type="text"
            bind:value={formData.firstName}
            class="input-field {errors.firstName ? 'error' : ''}"
            placeholder="Введите ваше имя"
          />
          {#if errors.firstName}
            <span class="error-text">{errors.firstName}</span>
          {/if}
        </div>

        <div class="input-group">
          <label for="lastName" class="input-label">Фамилия *</label>
          <input
            id="lastName"
            type="text"
            bind:value={formData.lastName}
            class="input-field {errors.lastName ? 'error' : ''}"
            placeholder="Введите вашу фамилию"
          />
          {#if errors.lastName}
            <span class="error-text">{errors.lastName}</span>
          {/if}
        </div>
      </div>

      <div class="form-row">
        <div class="input-group">
          <label for="gender" class="input-label">Пол *</label>
          <select
            id="gender"
            bind:value={formData.gender}
            class="input-field {errors.gender ? 'error' : ''}"
          >
            <option value="">Выберите пол</option>
            <option value="male">Мужской</option>
            <option value="female">Женский</option>
          </select>
          {#if errors.gender}
            <span class="error-text">{errors.gender}</span>
          {/if}
        </div>

        <div class="input-group">
          <label for="birthDate" class="input-label">Дата рождения *</label>
          <input
            id="birthDate"
            type="date"
            bind:value={formData.birthDate}
            class="input-field {errors.birthDate ? 'error' : ''}"
          />
          {#if errors.birthDate}
            <span class="error-text">{errors.birthDate}</span>
          {/if}
        </div>
      </div>

      <div class="input-group">
        <label for="position" class="input-label">Текущая позиция в компании *</label>
        <input
          id="position"
          type="text"
          bind:value={formData.position}
          class="input-field {errors.position ? 'error' : ''}"
          placeholder="Например: Менеджер по персоналу"
        />
        {#if errors.position}
          <span class="error-text">{errors.position}</span>
        {/if}
      </div>

      <button class="login-btn" on:click={goToLogin}>Уже есть аккаунт? Войдите</button>

      <button type="submit" class="submit-btn">
        Зарегистрироваться
      </button>
    </form>
  </div>
</div>

<style>
  :global(body) {
    color: #2A2D30;
    line-height: 1.5;
  }

  .page-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  }

  .registration-container {
    background: white;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
    max-width: 500px;
    width: 100%;
  }

  .header {
    text-align: center;
    margin-bottom: 30px;
    position: relative;
  }

  .back-btn {
    position: absolute;
    left: 0;
    top: 0;
    background: none;
    border: none;
    color: #1DAFF7;
    cursor: pointer;
    font-size: 16px;
  }

  .back-btn:hover {
    text-decoration: underline;
  }

  .header h1 {
    margin-bottom: 35px;
    font-size: 28px;
    font-weight: 600;
    color: #2A2D30;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .input-label {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 2px;
  }

  .input-field {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.2s ease;
    font-family: inherit;
  }

  .input-field:focus {
    outline: none;
    border-color: #1DAFF7;
  }

  .input-field.error {
    border-color: #ff4444;
  }

  .error-text {
    font-size: 12px;
    color: #ff4444;
    margin-top: 2px;
  }

  select.input-field {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 16px;
    padding-right: 40px;
  }

  .login-btn {
    text-align: left;
    margin-bottom: -15px;
    background: none;
    border: none;
    color: #1DAFF7;
    cursor: pointer;
    font-size: 16px;
  }

  .login-btn:hover {
    text-decoration: underline;
  }

  .submit-btn {
    padding: 15px;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    margin-top: 10px;
  }

  .submit-btn:hover {
    background: #0d8dcd;
  }

  @media (max-width: 768px) {
    .registration-container {
      padding: 30px 20px;
      margin: 20px;
    }

    .form-row {
      grid-template-columns: 1fr;
      gap: 20px;
    }

    .header h1 {
      font-size: 24px;
    }

    .back-btn {
      position: relative;
      margin-bottom: 15px;
      text-align: left;
    }
  }

  @media (max-width: 480px) {
    .page-container {
      padding: 10px;
    }

    .registration-container {
      padding: 25px 15px;
    }
  }
</style>