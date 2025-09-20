<script lang="ts">
  import { marked } from 'marked';
  import DOMPurify from 'dompurify';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  interface Message {
    id: number;
    text: string;
    isUser: boolean;
    timestamp: Date;
  }

  let messages: Message[] = [];
  let userInput = '';
  let isLoading = false;
  let nextId = 1;

  function renderMarkdown(raw: string): string {
    const withNewlines = raw.replace(/\\n/g, '\n');
    const html = marked.parse(withNewlines) as string; // без устаревших опций
    return DOMPurify.sanitize(html);
  }

  function goBack() {
    const id = get(page).params.id;
    goto(`/user/${id}`);
  }

  function scrollToBottom() {
    setTimeout(() => {
      const container = document.querySelector('.messages-container') as HTMLDivElement | null;
      if (container) container.scrollTop = container.scrollHeight;
    }, 0);
  }

  async function sendMessage() {
    if (!userInput.trim() || isLoading) return;

    const id = get(page).params.id;
    
    // 1) Добавляем сообщение пользователя
    const textToSend = userInput.trim();
    console.log('[chat] sendMessage start', { id, textToSend });
    const userMessage: Message = {
      id: nextId++,
      text: textToSend,
      isUser: true,
      timestamp: new Date()
    };
    messages = [...messages, userMessage];

    // 2) Готовим отправку
    userInput = '';
    isLoading = true;
    scrollToBottom();

    try {
      const res = await fetch(`/api/chat/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textToSend })
      });

      if (!res.ok) {
        const errText = await res.text().catch(() => '');
        throw new Error(errText || `Ошибка запроса: ${res.status}`);
      }

      // 3) Ответ — просто строка (возможны кавычки)
      const raw = (await res.text()).trim();
      const reply = raw.replace(/^"(.+)"$/, '$1');

      const aiResponse: Message = {
        id: nextId++,
        text: reply,      // markdown рендерится ниже через renderMarkdown
        isUser: false,
        timestamp: new Date()
      };

      messages = [...messages, aiResponse];
    } catch (e) {
      const err = e instanceof Error ? e.message : 'Неизвестная ошибка';
      const fallback: Message = {
        id: nextId++,
        text: `⚠️ Не удалось получить ответ: ${err}`,
        isUser: false,
        timestamp: new Date()
      };
      messages = [...messages, fallback];
    } finally {
      isLoading = false;
      scrollToBottom();
    }
  }


  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  function adjustTextareaHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
  }

  onMount(() => {
    const id = get(page).params.id;
    const key = `chatInit:${id}`;
    const greeting = sessionStorage.getItem(key);

    if (greeting) {
      messages = [
        ...messages,
        {
          id: nextId++,
          text: greeting,
          isUser: false,
          timestamp: new Date()
        }
      ];
      sessionStorage.removeItem(key); // чтобы не показывать повторно при F5/навигации назад
    }

    scrollToBottom();
  });
</script>


<svelte:head>
  <title>AI чат - HR Консультант</title>
</svelte:head>

<div class="page-container">
  <!-- Шапка чата -->
  <div class="chat-header">
    <button class="back-btn" on:click={goBack}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Назад
    </button>
    <div class="chat-title">
      <h1>Карьерный консультант</h1>
      <p class="chat-subtitle">AI помощник для вашего развития</p>
    </div>
    <div class="header-spacer"></div>
  </div>

  <!-- Контейнер сообщений -->
  <div class="messages-container">
    {#if messages.length === 0}
      <div class="empty-chat">
        <div class="empty-icon">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#1DAFF7">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2>Начните общение</h2>
        <p>Задайте вопрос о карьере, развитии или поиске работы</p>
      </div>
    {:else}
      {#each messages as message (message.id)}
        <div class="message {message.isUser ? 'user-message' : 'ai-message'}">
          <div class="message-avatar">
            {#if message.isUser}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="7" r="4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {:else}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 8V12L15 15M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {/if}
          </div>
          <div class="message-content">
            <div class="message-text markdown">
              {@html message.isUser ? renderMarkdown(message.text) : renderMarkdown(message.text)}
            </div>
            <div class="message-time">
              {message.timestamp.toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </div>
        </div>
      {/each}

      {#if isLoading}
        <div class="message ai-message">
          <div class="message-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 8V12L15 15M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>

  <!-- Поле ввода сообщения -->
  <div class="input-container">
    <div class="input-wrapper">
      <textarea
        bind:value={userInput}
        on:keydown={handleKeyPress}
        on:input={adjustTextareaHeight}
        placeholder="Напишите ваш вопрос"
        rows="1"
        class="message-input"
        disabled={isLoading}
      ></textarea>
      <button
        on:click={sendMessage}
        disabled={!userInput.trim() || isLoading}
        class="send-button"
        title="Отправить сообщение"
        aria-label="Отправить сообщение"
        type="button"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>

    </div>
  </div>
</div>

<style>
  :global(body) {
    background: #f8fafc;
    color: #2A2D30;
    line-height: 1.5;
    height: 100vh;
    overflow: hidden;
  }

  .page-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 100%;
    margin: 0 auto;
    background: white;
  }

  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    background: white;
    border-bottom: 1px solid #e2e8f0;
  }

  .back-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    background: none;
    border: none;
    color: #1DAFF7;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    padding: 6px 10px;
    border-radius: 6px;
  }

  .back-btn:hover {
    text-decoration: underline;
  }

  .chat-title {
    text-align: center;
    flex: 1;
  }

  .chat-title h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 600;
    color: #1f2937;
  }

  .chat-subtitle {
    margin: 2px 0 0 0;
    font-size: 12px;
    color: #64748b;
  }

  .header-spacer {
    width: 80px;
  }

  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 15px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: #f8fafc;
  }

  .empty-chat {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: #64748b;
    padding: 20px;
  }

  .empty-icon {
    margin-bottom: 15px;
    opacity: 0.6;
  }

  .empty-chat h2 {
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 600;
    color: #374151;
  }

  .empty-chat p {
    margin: 0;
    font-size: 14px;
  }

  .message {
    display: flex;
    gap: 10px;
    max-width: 85%;
  }

  .user-message {
    align-self: flex-end;
    flex-direction: row-reverse;
  }

  .ai-message {
    align-self: flex-start;
  }

  .message-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #f0f9ff;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 2px solid #1DAFF7;
    margin-top: 2px;
  }

  .user-message .message-avatar {
    background: #1DAFF7;
  }

  .user-message .message-avatar svg {
    color: white;
  }

  .ai-message .message-avatar {
    background: white;
    border-color: #e2e8f0;
  }

  .message-content {
    background: white;
    padding: 10px 14px;
    border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    max-width: 100%;
  }

  .user-message .message-content {
    background: #1DAFF7;
    color: white;
    border-bottom-right-radius: 4px;
  }

  .ai-message .message-content {
    background: white;
    border: 1px solid #e2e8f0;
    border-bottom-left-radius: 4px;
  }

  .message-text {
    font-size: 14px;
    line-height: 1.4;
    margin-bottom: 3px;
    word-wrap: break-word;
  }

  .message-time {
    font-size: 10px;
    opacity: 0.7;
    text-align: right;
  }

  .user-message .message-time {
    text-align: left;
  }

  .typing-indicator {
    display: flex;
    align-items: center;
    gap: 3px;
    padding: 6px 0;
  }

  .typing-indicator span {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #64748b;
    animation: typing 1.4s infinite ease-in-out;
  }

  .typing-indicator span:nth-child(1) { animation-delay: 0s; }
  .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
  .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

  .input-container {
    padding: 25px 35px;
    background: white;
    border-top: 1px solid #e2e8f0;
  }

  .input-wrapper {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 20px;
    padding: 8px 12px;
  }

  .input-wrapper:focus-within {
    border-color: #1DAFF7;
  }

  .message-input {
    flex: 1;
    border: none;
    outline: none;
    resize: none;
    font-size: 14px;
    font-family: inherit;
    line-height: 1.4;
    min-height: 20px;
    max-height: 100px;
    background: transparent;
    padding: 4px 0;
  }

  .message-input:disabled {
    opacity: 0.6;
  }

  .message-input::placeholder {
    color: #94a3b8;
  }

  .send-button {
    padding: 8px;
    background: #1DAFF7;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .send-button:hover:not(:disabled) {
    background: #0d8dcd;
  }

  .send-button:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
  }

  .send-button svg {
    width: 16px;
    height: 16px;
  }

  .markdown {
    white-space: normal; /* markdown сам управляет переносами */
    line-height: 1.55;
  }
  .markdown h1, .markdown h2, .markdown h3 {
    margin: 0.4em 0 0.3em;
    font-weight: 700;
  }
  .markdown h1 { font-size: 1.25rem; }
  .markdown h2 { font-size: 1.125rem; }
  .markdown h3 { font-size: 1rem; }
  .markdown p { margin: 0.4em 0; }
  .markdown ul, .markdown ol { margin: 0.4em 0 0.4em 1.2em; }
  .markdown li { margin: 0.2em 0; }
  .markdown strong { font-weight: 700; }
  .markdown code {
    background: #f3f4f6; border: 1px solid #e5e7eb; padding: 0.1em 0.3em; border-radius: 4px;
  }

  @keyframes typing {
    0%, 60%, 100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    30% {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>