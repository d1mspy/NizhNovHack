<script lang="ts">
  import { goto } from '$app/navigation';

  const goToHRPage = async (): Promise<void> => {
    try {
      await goto('/vacancy');
    } catch (error) {
      console.error('Navigation error:', error);
      window.location.href = '/vacancy';
    }
  };

  const goToEmployeePage = async (): Promise<void> => {
    try {
      await goto('/employee');
    } catch (error) {
      console.error('Navigation error:', error);
      window.location.href = '/employee';
    }
  };
</script>

<svelte:head>
  <title>Выбор роли - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <div class="role-selection">
    <h1>Выберите роль</h1>
    <p class="subtitle">Для продолжения выберите вашу роль в системе</p>
    
    <div class="buttons-container">
      <button class="role-btn hr-btn" on:click={goToHRPage}>
        <div class="btn-content">
          <span class="btn-icon">👔</span>
          <span class="btn-text">HR</span>
        </div>
      </button>
      
      <button class="role-btn employee-btn" on:click={goToEmployeePage}>
        <div class="btn-content">
          <span class="btn-icon">👤</span>
          <span class="btn-text">Работник</span>
        </div>
      </button>
    </div>
  </div>
</div>

<style>
  :global(body) {
    color: #333;
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

  .role-selection {
    text-align: center;
    background: white;
    padding: 50px 40px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
    max-width: 500px;
    width: 100%;
  }

  .role-selection h1 {
    margin: 0 0 10px 0;
    font-size: 28px;
    font-weight: 600;
    color: #333;
  }

  .subtitle {
    margin: 0 0 40px 0;
    color: #666;
    font-size: 16px;
  }

  .buttons-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .role-btn {
    padding: 30px;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
  }

  .role-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    border-color: #1DAFF7;
  }

  .hr-btn:hover {
    background: linear-gradient(135deg, #e8f4ff 0%, #d4e7ff 100%);
  }

  .employee-btn:hover {
    background: linear-gradient(135deg, #f0fff4 0%, #e0ffe8 100%);
  }

  .btn-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .btn-icon {
    font-size: 32px;
    margin-bottom: 5px;
  }

  .btn-text {
    font-size: 20px;
    font-weight: 600;
    color: #333;
  }

  @media (max-width: 768px) {
    .role-selection {
      padding: 30px 20px;
      margin: 20px;
    }

    .role-selection h1 {
      font-size: 24px;
    }

    .role-btn {
      padding: 25px 20px;
    }

    .btn-icon {
      font-size: 28px;
    }

    .btn-text {
      font-size: 18px;
    }
  }

  @media (max-width: 480px) {
    .page-container {
      padding: 10px;
    }

    .role-selection {
      padding: 25px 15px;
    }

    .buttons-container {
      gap: 15px;
    }

    .role-btn {
      padding: 20px 15px;
    }
  }
</style>