/* Interações locais e Assistente de IA do Portfólio (Databricks Model Serving + Fallback Inteligente). */
"use strict";

const controls = document.querySelector("[data-project-controls]");
if (controls) {
  const cards = [...document.querySelectorAll("[data-project]")];
  const buttons = [...document.querySelectorAll("[data-filter]")];
  const input = document.querySelector("[data-search-input]");
  const count = document.querySelector("[data-filter-count]");
  const empty = document.querySelector("[data-empty]");
  let selected = "todos";
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const applyFilters = () => {
    const query = normalize(input.value.trim());
    let shown = 0;
    for (const card of cards) {
      const matches = (selected === "todos" || card.dataset.group === selected) &&
        normalize(card.dataset.search).includes(query);
      card.hidden = !matches;
      if (matches) shown += 1;
    }
    count.textContent = `${shown} de ${cards.length} projetos`;
    empty.hidden = shown > 0;
    for (const button of buttons) {
      const active = button.dataset.filter === selected;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    }
  };
  for (const button of buttons) {
    button.addEventListener("click", () => { selected = button.dataset.filter; applyFilters(); });
  }
  input.addEventListener("input", applyFilters);
  controls.hidden = false;
  count.hidden = false;
  applyFilters();
}

const printButton = document.querySelector("[data-print]");
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener("click", () => window.print());
}

/* === ASSISTENTE DE IA DO PORTFÓLIO === */
const chatToggle = document.querySelector("[data-chat-toggle]");
const chatDrawer = document.querySelector("[data-chat-drawer]");
const chatClose = document.querySelector("[data-chat-close]");
const chatMessages = document.querySelector("[data-chat-messages]");
const chatForm = document.querySelector("[data-chat-form]");
const chatInput = document.querySelector("[data-chat-input]");
const chatChips = document.querySelectorAll("[data-chat-prompt]");
const heroChatBtn = document.querySelector("[data-open-chat]");

const chatHistory = [];

function knowledgeBaseReply(question) {
  const q = question.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  if (q.includes("contato") || q.includes("email") || q.includes("e-mail") || q.includes("falar") || q.includes("contratar") || q.includes("recrut") || q.includes("linkedin") || q.includes("github")) {
    return (
      "Você pode entrar em contato diretamente com a **Beatriz Helena** pelos canais oficiais:\n\n" +
      "• **E-mail:** beatrizhelena777@gmail.com\n" +
      "• **GitHub:** https://github.com/BeatrizOrlandi\n" +
      "• **Currículo para impressão/PDF:** https://beatrizorlandi.github.io/curriculo.html\n\n" +
      "Ela atua como **Engenheira de IA** e está aberta a conversas sobre oportunidades, projetos de IA Generativa, Engenharia de Dados e Databricks!"
    );
  }

  if (q.includes("experiencia") || q.includes("carreira") || q.includes("trabalh") || q.includes("efi") || q.includes("dadosfera") || q.includes("formacao") || q.includes("ufop") || q.includes("quem e") || q.includes("sobre")) {
    return (
      "**Beatriz Helena** é **Engenheira de IA** formada em **Ciência da Computação pela UFOP** (Universidade Federal de Ouro Preto).\n\n" +
      "**Trajetória Profissional:**\n" +
      "• **Efí Bank (2024 — atual):** Engenheira de Inovação / IA — desenvolvimento de protótipos, PoCs e soluções de dados e IA com Python, Snowflake, SQL e LLMs.\n" +
      "• **Dadosfera (2023 — 2024):** Estágio em Solutions Engineer.\n" +
      "• **Prefeitura de Ouro Preto (2023):** Estágio em Desenvolvimento de Sistemas (Node.js, AngularJS, MySQL).\n" +
      "• **DGB Tecnologia (2022 — 2023):** Desenvolvedora Júnior.\n\n" +
      "Para falar com ela, envie um e-mail para beatrizhelena777@gmail.com!"
    );
  }

  if (q.includes("rag") || q.includes("vector") || q.includes("qwen") || q.includes("regulamento") || q.includes("03")) {
    return (
      "No **Estudo 03 — Pipeline RAG de Regulamentos**, a Beatriz construiu e validou no Databricks:\n\n" +
      "• **Baseline Lexical (TF-IDF):** 16/16 testes aprovados.\n" +
      "• **Índice Vetorial (Databricks Vector Search):** Delta Sync com Change Data Feed e embeddings nativos `databricks-qwen3-embedding-0-6b` (1.024 dimensões).\n" +
      "• **Governança de Escopo:** Filtros estritos de biblioteca (`library_id`) e vigência (`valid_from_day <= ref <= valid_to_day`) aplicados no código.\n" +
      "• **Resultados:** 93,3% de precisão top-1 (14/15 casos) e 8/8 verificações de integridade aprovadas.\n" +
      "• **Código no GitHub:** https://github.com/BeatrizOrlandi/aurora-03-rag-regulamentos"
    );
  }

  if (q.includes("pipeline") || q.includes("lakehouse") || q.includes("aurora") || q.includes("bronze") || q.includes("silver") || q.includes("gold") || q.includes("qualidade") || q.includes("01") || q.includes("02")) {
    return (
      "Os **Estudos 01 e 02 (Lakehouse Aurora & Qualidade)** demonstram engenharia de dados ponta a ponta no Databricks:\n\n" +
      "• **Arquitetura Medalhão (7 tarefas):** Origem sintética determinística (5.000 eventos) → Bronze → Silver + Quarentena → Gold (69 linhas agregadas, 2.500 empréstimos reconciliados) → Gate de Qualidade → Publicação por ponteiro → Boletins.\n" +
      "• **Qualidade e Observabilidade:** 8 regras críticas/alertas e **24/24 asserções de integração aprovadas** (reprocessamento idempotente, duplicidades, atraso dentro/fora da janela, conflito de payload e preservação da última release válida).\n" +
      "• **Repositórios:** https://github.com/BeatrizOrlandi/aurora-01-pipeline-dados e https://github.com/BeatrizOrlandi/aurora-02-qualidade-observabilidade"
    );
  }

  if (q.includes("agente") || q.includes("serving") || q.includes("llm") || q.includes("langgraph") || q.includes("mlflow") || q.includes("04") || q.includes("05")) {
    return (
      "Na frente de **Agentes e LLMs (Estudos 04 e 05)**:\n\n" +
      "• Este próprio assistente foi empacotado como um **`MLflow ResponsesAgent`**, registrado no Unity Catalog (`workspace.estudos_ai.beatriz_portfolio_agent`) e implantado no **Databricks Model Serving** (`beatriz-portfolio-agent`) consumindo o `databricks-meta-llama-3-3-70b-instruct`!\n" +
      "• Além disso, os estudos cobrem orquestração com ferramentas tipadas (`consultar_metricas`, `buscar_regulamento`, `salvar_rascunho`), avaliação determinística + LLM Judge e rastreabilidade com MLflow Tracing.\n" +
      "• **Repositório:** https://github.com/BeatrizOrlandi/aurora-05-agentes-investigacao"
    );
  }

  if (q.includes("projeto") || q.includes("portfolio") || q.includes("estudo") || q.includes("databricks") || q.includes("habilidade") || q.includes("stack") || q.includes("tecnologia")) {
    return (
      "O portfólio da **Beatriz Helena** reúne **8 projetos no Databricks** (todos com repositórios públicos em https://github.com/BeatrizOrlandi):\n\n" +
      "1. **01 — Pipeline de dados Aurora** (MVP validado · PySpark, Delta Lake, Jobs)\n" +
      "2. **02 — Qualidade e observabilidade** (MVP validado · 8 checks e 24 testes de integração)\n" +
      "3. **03 — RAG de regulamentos** (Recuperação validada · Vector Search + Qwen3 + TF-IDF)\n" +
      "4. **04 — Experimentos com LLMs** (Avaliação de prompts e modelos com MLflow)\n" +
      "5. **05 — Agentes de investigação & Model Serving** (ResponsesAgent no Model Serving + design multiagente)\n" +
      "6. **06 — Automação de boletins** (MVP validado · geração idempotente a partir da Gold)\n" +
      "7. **07 — Previsão de demanda com ML** (Features causais e splits temporais)\n" +
      "8. **08 — Avaliador semântico BEM (Kaggle)**\n\n" +
      "Sobre qual deles você gostaria de saber mais? Ou prefere os dados de contato (beatrizhelena777@gmail.com)?"
    );
  }

  return (
    "Sou o **Agente de IA da Beatriz Helena** (hospedado via Databricks Model Serving `beatriz-portfolio-agent`).\n\n" +
    "A Beatriz é **Engenheira de IA** (Efí Bank, graduada em Ciência da Computação pela UFOP), especialista em **Python, Databricks, LLMs, RAG, LangChain/LangGraph e MLflow**.\n\n" +
    "• **Projetos validados:** Lakehouse Aurora (Bronze/Silver/Gold), Gate de Qualidade (24 asserções), RAG com Databricks Vector Search (93,3% top-1), Automação de Boletins e Agente no Model Serving.\n" +
    "• **Contato direto:** beatrizhelena777@gmail.com | **GitHub:** https://github.com/BeatrizOrlandi"
  );
}

function formatMessageHTML(text) {
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  const withBold = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  const withCode = withBold.replace(/`([^`]+)`/g, "<code>$1</code>");
  const withLinks = withCode
    .replace(/(https:\/\/[^\s)<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>')
    .replace(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g, '<a href="mailto:$1">$1</a>');
  return withLinks
    .split("\n\n")
    .map((p) => `<p>${p.replace(/\n/g, "<br>")}</p>`)
    .join("");
}

function appendBubble(role, text) {
  if (!chatMessages) return null;
  const div = document.createElement("div");
  div.className = `chat-bubble ${role}`;
  div.innerHTML = formatMessageHTML(text);
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return div;
}

async function sendChatMessage(userText) {
  const clean = userText.trim();
  if (!clean) return;
  appendBubble("user", clean);
  chatHistory.push({ role: "user", content: clean });

  const loadingBubble = appendBubble("assistant", "Consultando o agente da Beatriz...");

  let reply = null;
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 6500);
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: chatHistory }),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (response.ok) {
      const data = await response.json();
      if (data && data.reply) {
        reply = data.reply;
      }
    }
  } catch (_) {
    // No static GitHub Pages host, /api/chat is not present; use instant knowledge base engine
  }

  if (!reply) {
    await new Promise((r) => setTimeout(r, 320));
    reply = knowledgeBaseReply(clean);
  }

  chatHistory.push({ role: "assistant", content: reply });
  if (loadingBubble) {
    loadingBubble.innerHTML = formatMessageHTML(reply);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

function openChat() {
  if (!chatDrawer || !chatToggle) return;
  chatDrawer.hidden = false;
  chatToggle.setAttribute("aria-expanded", "true");
  if (chatInput) chatInput.focus();
}

function closeChat() {
  if (!chatDrawer || !chatToggle) return;
  chatDrawer.hidden = true;
  chatToggle.setAttribute("aria-expanded", "false");
}

if (chatToggle && chatDrawer) {
  chatToggle.hidden = false;
  chatToggle.addEventListener("click", () => {
    if (chatDrawer.hidden) openChat();
    else closeChat();
  });
}
if (heroChatBtn) {
  heroChatBtn.addEventListener("click", (e) => {
    e.preventDefault();
    openChat();
  });
}
if (chatClose) {
  chatClose.addEventListener("click", closeChat);
}
if (chatForm && chatInput) {
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const val = chatInput.value;
    chatInput.value = "";
    sendChatMessage(val);
  });
}
for (const chip of chatChips) {
  chip.addEventListener("click", () => {
    const prompt = chip.getAttribute("data-chat-prompt");
    if (prompt) {
      openChat();
      sendChatMessage(prompt);
    }
  });
}
