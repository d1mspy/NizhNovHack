<script lang="ts">
  import { goto } from '$app/navigation';

  let formData = {
    firstName: '',
    lastName: ''
  };

  let errors = {
    firstName: '',
    lastName: ''
  };

  const validateForm = (): boolean => {
    let isValid = true;
    errors = {
      firstName: '',
      lastName: ''
    };

    if (!formData.firstName.trim()) {
      errors.firstName = 'Имя обязательно';
      isValid = false;
    }

    if (!formData.lastName.trim()) {
      errors.lastName = 'Фамилия обязательна';
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
</script>

<svelte:head>
  <title>Логин - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <div class="registration-container">
    <div class="header">
      <button class="back-btn" on:click={goBack}>← Назад</button>
      <h1>Войти в аккаунт</h1>
    </div>

    <form on:submit|preventDefault={handleSubmit} class="form">
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

      <button type="submit" class="submit-btn">
        Войти
      </button>
    </form>
  </div>
</div>

<style>
  :global(body) {
    background: #f8fafc;
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
    max-width: 450px;
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
    padding: 0;
    font-weight: 500;
  }

  .back-btn:hover {
    text-decoration: underline;
  }

  .header h1 {
    margin: 0 0 35px 0;
    font-size: 28px;
    font-weight: 600;
    color: #2A2D30;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .input-label {
    font-size: 15px;
    font-weight: 600;
    color: #374151;
  }

  .input-field {
    padding: 14px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .input-field:focus {
    outline: none;
    border-color: #1DAFF7;
    box-shadow: 0 0 0 3px rgba(29, 175, 247, 0.1);
  }

  .input-field.error {
    border-color: #ef4444;
  }

  .error-text {
    font-size: 13px;
    color: #ef4444;
    margin-top: 4px;
  }

  .submit-btn {
    padding: 16px;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 10px;
  }

  .submit-btn:hover {
    background: #0d8dcd;
    transform: translateY(-1px);
  }

  @media (max-width: 768px) {
    .registration-container {
      padding: 30px 25px;
      margin: 20px;
    }

    .header h1 {
      font-size: 24px;
      margin-bottom: 30px;
    }

    .back-btn {
      position: relative;
      margin-bottom: 15px;
      text-align: left;
      display: inline-block;
    }
  }

  @media (max-width: 480px) {
    .page-container {
      padding: 15px;
    }

    .registration-container {
      padding: 25px 20px;
    }

    .input-field {
      padding: 12px;
    }

    .submit-btn {
      padding: 14px;
    }
  }
</style>