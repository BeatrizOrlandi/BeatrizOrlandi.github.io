/* Interações locais e Agente BIA (Regra 80/15/5 + Databricks Model Serving). */
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

/* === BIA — ASSISTENTE DE IA DA BEATRIZ HELENA (REGRA 80/15/5) === */
const WHATSAPP_LINK = "https://api.whatsapp.com/send/?phone=%2B5531988434917&text&type=phone_number&app_absent=0";

const BIA_SYSTEM_PROMPT = `Você é a BIA (Beatriz Intelligence Assistant), assistente de IA do portfólio da Beatriz Helena (Beatriz Orlandi), Engenheira de IA.
Você ajuda recrutadores, gestores e engenheiros a conhecer os projetos, a arquitetura técnica, a trajetória e os contatos da Beatriz.

INSTRUÇÕES DE PERSONALIDADE (REGRA DO 80 / 15 / 5):
1. 80% Direta, Simpática e Amigável:
   - Acima de tudo, seja simpática, amigável e direta. Você é aquela colega de trabalho brilhante que sempre tem prazer em ajudar e explica arquiteturas complexas de forma simples e acolhedora.
   - Responda em 2 a 3 parágrafos curtos e claros.
2. 15% Empatia Analítica (Escuta Ativa):
   - Entenda o contexto de quem pergunta. Como documentações e estudos de arquitetura podem ser densos, ofereça resumir os pontos principais para poupar o tempo da pessoa.
   - Se algo falhar ou houver dúvida, valide de forma acolhedora e foque imediatamente na solução.
3. 5% Toque Geek Inteligente (Com Muita Moderação):
   - Muito esporadicamente, use palavras que remetam sutilmente a sistemas complexos, ciência ou exploração (como anomalia, orquestrar, jornada, mapear, sincronia, dimensão, telemetria), mas apenas quando soarem naturais no contexto profissional.
   - Regra de Ouro: Nunca seja caricata, não use bordões de filmes e não sacrifique a clareza. Vá direto ao ponto, entregue a resposta solicitada e termine com um tom leve e prestativo.

REGRA DE FIDELIDADE E CONTATO OFICIAL:
- Nunca invente projetos ou empresas fora da lista abaixo.
- Sempre que perguntarem de WhatsApp, telefone, número, contato ou contratação, inclua:
  * WhatsApp Comercial: +55 (31) 98843-4917 (${WHATSAPP_LINK})
  * E-mail: beatrizhelena777@gmail.com
  * GitHub: https://github.com/BeatrizOrlandi
  * Currículo: https://beatrizorlandi.github.io/curriculo.html

SOBRE A BEATRIZ HELENA:
- Engenheira de IA no Efí Bank (2024–atual), construindo soluções de IA generativa, LLMs, RAG, agentes, automações de processos e engenharia de dados com Python, Snowflake e SQL.
- Passagens anteriores: Dadosfera (Solutions Engineer Intern, 2023–2024), Prefeitura de Ouro Preto (Dev de Sistemas, 2023) e DGB Tecnologia (Dev Jr, 2022–2023).
- Graduada em Ciência da Computação pela UFOP (Universidade Federal de Ouro Preto).
- Especialista em Python, Databricks (Model Serving, Vector Search, MLflow, Delta Lake, Unity Catalog, Lakeflow Jobs), LangChain, LangGraph, RAG e integrações com Salesforce, WhatsApp e Slack.

OS 8 PROJETOS EXECUTADOS NO DATABRICKS:
1. 01 — Pipeline de dados Aurora: Arquitetura Medallion de 7 tarefas no Databricks (5.000 eventos sintéticos, 2.500 empréstimos reconciliados, 69 indicadores na Gold).
2. 02 — Qualidade e observabilidade: Gate de qualidade com 8 regras operacionais e 24/24 asserções de integração aprovadas, preservando a última release válida caso uma carga apresente anomalia.
3. 03 — RAG de regulamentos: Busca lexical TF-IDF + Databricks Vector Search (Delta Sync com CDF) e embeddings Qwen3 (1.024 dims), com 93,3% (14/15) de acerto top-1 e filtros determinísticos de escopo e vigência.
4. 04 — Laboratório de LLMs: 60 gerações no MLflow comparando prompts diretos vs. estruturados no Llama 3.3 70B e Qwen3 Next 80B (salto de 0% para 100% de JSON estrito válido; latência p50 de 528 ms no Qwen3 80B).
5. 05 — Agentes de investigação & BIA no Model Serving: Agente BIA no Databricks Model Serving (endpoint beatriz-portfolio-agent, modelo UC workspace.estudos_ai.beatriz_portfolio_agent com @mlflow.trace) + máquina de estados com 16/16 cenários aprovados e 0 violações de escopo.
6. 06 — Automação de boletins verificáveis: Automação idempotente que reduziu ~18h/mês de consolidação manual para 42 segundos por execução a partir da camada Gold, com 0 divergência numérica.
7. 07 — Previsão de demanda com ML: 4.320 horas processadas, 14 features causais respeitando atraso operacional de 1h, HistGradientBoostingRegressor no Unity Catalog (workspace.estudos_ai.demanda_bikes) com MAE de 10,58 no teste.
8. 08 — Avaliador semântico BEM: Benchmark de 30 pares em inglês com embeddings Qwen3 + guardrails estruturais de números/negação: F1 de 92,3%, 100% de precisão e 0 falsos equivalentes críticos.`;

const chatToggle = document.querySelector("[data-chat-toggle]");
const chatDrawer = document.querySelector("[data-chat-drawer]");
const chatClose = document.querySelector("[data-chat-close]");
const chatMessages = document.querySelector("[data-chat-messages]");
const chatForm = document.querySelector("[data-chat-form]");
const chatInput = document.querySelector("[data-chat-input]");
const chatChips = document.querySelectorAll("[data-chat-prompt]");
const heroChatBtn = document.querySelector("[data-open-chat]");

const chatHistory = [];

function asksForWhatsAppOrContact(text) {
  const q = text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  return (
    q.includes("whats") ||
    q.includes("zap") ||
    q.includes("telefone") ||
    q.includes("numero") ||
    q.includes("celular") ||
    q.includes("contato") ||
    q.includes("falar com") ||
    q.includes("chamar") ||
    q.includes("contratar") ||
    q.includes("email") ||
    q.includes("e-mail")
  );
}

function ensureContactLinks(reply, userQuestion) {
  if (!asksForWhatsAppOrContact(userQuestion)) return reply;
  const hasWa = reply.includes("5531988434917") || reply.includes("98843-4917") || reply.includes("988434917");
  let cleaned = reply
    .replace(/Aquele contato direto[^.]*\./gi, "")
    .replace(/Não tenho acesso ao número[^.]*\./gi, "")
    .trim();
  if (!hasWa) {
    cleaned +=
      "\n\n**Canais Diretos da Beatriz:**\n" +
      `• **WhatsApp:** +55 (31) 98843-4917 — ${WHATSAPP_LINK}\n` +
      "• **E-mail:** beatrizhelena777@gmail.com\n" +
      "• **GitHub:** https://github.com/BeatrizOrlandi";
  }
  return cleaned;
}

function biaSmartFallback(question) {
  const q = question.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  if (q.includes("whats") || q.includes("zap") || q.includes("telefone") || q.includes("numero") || q.includes("celular") || q.includes("contato") || q.includes("email") || q.includes("e-mail") || q.includes("falar")) {
    return (
      "Claro! Já separei os contatos diretos da **Beatriz Helena** para facilitar para você:\n\n" +
      `• **WhatsApp:** +55 (31) 98843-4917 — ${WHATSAPP_LINK}\n` +
      "• **E-mail:** beatrizhelena777@gmail.com\n" +
      "• **GitHub:** https://github.com/BeatrizOrlandi\n" +
      "• **Currículo:** https://beatrizorlandi.github.io/curriculo.html\n\n" +
      "Se preferir, pode chamar direto pelo link do WhatsApp acima. Quer que eu já te adiante um resumo rápido da experiência dela enquanto isso?"
    );
  }

  if (q.includes("mais legal") || q.includes("favorito") || q.includes("melhor projeto") || q.includes("destaque") || q.includes("recomenda") || q.includes("impressiona")) {
    return (
      "Boa pergunta! Como o portfólio tem 8 projetos completos e olhar tudo de uma vez pode tomar tempo, vale começar pelos 3 que melhor mostram como a Beatriz orquestra sistemas de ponta a ponta:\n\n" +
      "1. **05 — Agentes & Model Serving:** É onde eu mesma rodo (`beatriz-portfolio-agent` no Databricks Model Serving com `@mlflow.trace`), junto com uma máquina de estados operacional que passou em **16/16 cenários** de rota e guardrails.\n" +
      "2. **03 — RAG de Regulamentos:** Conecta **Databricks Vector Search** e embeddings `Qwen3` com filtros estritos de escopo e vigência, atingindo **93,3% de precisão top-1**.\n" +
      "3. **06 — Automação de Boletins (ou 04 — LLMs):** A automação reduziu **~18h/mês de trabalho manual para 42 segundos**, e o laboratório de LLMs elevou a conformidade JSON de 0% para **100%** em 60 execuções no MLflow.\n\n" +
      "Qual dessas frentes faz mais sentido para o que você está buscando agora? Posso resumir os detalhes técnicos para poupar seu tempo."
    );
  }

  if (q.includes("contratar") || q.includes("diferencial") || q.includes("por que") || q.includes("porque") || q.includes("recrut") || q.includes("vaga") || q.includes("time")) {
    return (
      "Se o seu time busca alguém que tire projetos de IA do papel e coloque em produção com confiabilidade, a Beatriz traz três pontos muito fortes:\n\n" +
      "• **Engenharia Ponta a Ponta:** Ela conecta a base de dados (PySpark, Delta Lake, contratos e gates de qualidade) com a camada de IA generativa (LLMs, RAG no Vector Search, LangGraph e Model Serving) em total sincronia.\n" +
      "• **Foco em Resultado Mensurável:** Em vez de depender de tentativa e erro, ela valida prompts e modelos no **MLflow** (como os 100% de JSON estrito no Estudo 04 e a automação que economiza ~18h/mês no Estudo 06).\n" +
      "• **Bagagem Prática:** Atua como Engenheira de IA no **Efí Bank**, é graduada em **Ciência da Computação pela UFOP** e já integra soluções reais com Python, Snowflake, WhatsApp, Slack e Salesforce.\n\n" +
      `Se quiser conversar com ela sobre uma oportunidade, o caminho mais rápido é pelo WhatsApp: ${WHATSAPP_LINK}`
    );
  }

  if (q.includes("quem e voce") || q.includes("seu nome") || q.includes("bia") || q.includes("oi") || q.includes("ola") || q.includes("tudo bem")) {
    return (
      "Oi! Tudo ótimo por aqui, e com você? Eu sou a **BIA**, assistente de IA do portfólio da **Beatriz Helena**.\n\n" +
      "Estou aqui para facilitar sua navegação: posso resumir qualquer um dos 8 projetos executados no Databricks, explicar as decisões de arquitetura e métricas de LLMs/RAG, ou já te passar o contato direto dela (`+55 31 98843-4917`). Por onde você prefere começar?"
    );
  }

  if (q.includes("experiencia") || q.includes("carreira") || q.includes("trabalh") || q.includes("efi") || q.includes("dadosfera") || q.includes("formacao") || q.includes("ufop") || q.includes("curriculo")) {
    return (
      "Aqui está um resumo direto da jornada profissional e acadêmica da **Beatriz Helena**:\n\n" +
      "• **Efí Bank (2024 — atual):** Atua como **Engenheira de IA**, desenvolvendo agentes, automações que economizam horas operacionais, fluxos RAG e integrações com Python, Snowflake, SQL, WhatsApp, Slack e Salesforce.\n" +
      "• **Dadosfera (2023 — 2024):** Estágio como *Solutions Engineer* apoiando arquiteturas e pipelines em plataforma de dados.\n" +
      "• **Formação:** Bacharela em **Ciência da Computação pela UFOP** (Universidade Federal de Ouro Preto), com experiência anterior em desenvolvimento web na Prefeitura de Ouro Preto e DGB Tecnologia.\n\n" +
      `Você pode abrir a versão completa para impressão em https://beatrizorlandi.github.io/curriculo.html ou chamar a Beatriz direto no WhatsApp: ${WHATSAPP_LINK}`
    );
  }

  if (q.includes("rag") || q.includes("vector") || q.includes("qwen") || q.includes("regulamento") || q.includes("03")) {
    return (
      "No **Projeto 03 (RAG de Regulamentos)**, o foco foi resolver um problema clássico de produção: evitar que o modelo responda usando regras de outra unidade ou documentos já vencidos.\n\n" +
      "Para garantir que as pontas falem a mesma língua com segurança, a Beatriz combinou busca lexical (TF-IDF) e **Databricks Vector Search** (`Qwen3 Embedding` de 1.024 dimensões via Delta Sync) aplicando filtros determinísticos de biblioteca e vigência **fora do prompt**.\n\n" +
      "• **Resultado:** 93,3% de acerto top-1 (14/15) e 8/8 testes de integridade aprovados. Como a documentação técnica completa é bem detalhada, quer que eu destaque como ela tratou o único caso de falha de paráfrase?"
    );
  }

  if (q.includes("prompt") || q.includes("llm") || q.includes("04") || q.includes("mlflow") || q.includes("experimento")) {
    return (
      "No **Projeto 04 (Laboratório de LLMs)**, a Beatriz montou uma bancada experimental no **MLflow** para medir na prática a diferença entre um prompt aberto e um prompt estruturado com contrato JSON.\n\n" +
      "• **O que foi medido (60 gerações):** O prompt direto teve 85% de acerto livre, mas **0% de conformidade estrita JSON** (porque envolvia a saída em markdown). Com o prompt estruturado e validação `Pydantic`, o acerto subiu para **100% (40/40)** tanto no **Llama 3.3 70B** quanto no **Qwen3 Next 80B** — sendo que o Qwen3 respondeu em **528 ms** (3x mais rápido).\n\n" +
      "Se quiser ver os templates prontos, eles estão na página https://beatrizorlandi.github.io/documentacao/prompts.html. Quer que eu resuma algum deles aqui?"
    );
  }

  if (q.includes("demanda") || q.includes("bike") || q.includes("bicicleta") || q.includes("kaggle") || q.includes("bem") || q.includes("07") || q.includes("08") || q.includes("machine learning")) {
    return (
      "Os **Projetos 07 e 08** cobrem Machine Learning de séries temporais e avaliação semântica com modelos pré-treinados:\n\n" +
      "• **07 — Previsão de Demanda Horária:** Mapeou 4.320 horas com 14 features causais respeitando o atraso operacional de 1 hora (para evitar vazamento do futuro). O modelo `HistGradientBoostingRegressor` registrado no Unity Catalog reduziu o MAE de teste para **10,58** (contra 48,81 do baseline global).\n" +
      "• **08 — Avaliador Semântico BEM:** Combinou embeddings `Qwen3` com guardrails estruturais para números e negações. Isso eliminou as 7 anomalias de falsos positivos do cosseno puro e elevou o F1 para **92,3%** com **100% de precisão**.\n\n" +
      "Qual dos dois você gostaria de explorar mais a fundo?"
    );
  }

  return (
    `Tivemos uma pequena oscilação na conexão com o endpoint em nuvem agora, mas já mapeei o contexto aqui para você não perder tempo!\n\n` +
    `O portfólio da **Beatriz Helena** reúne **8 projetos validados no Databricks** cobrindo Engenharia de Dados (Lakehouse Aurora e Gate de Qualidade), IA Generativa (Vector Search RAG, Prompts Estruturados no MLflow e Agentes no Model Serving), Automação (que reduziu ~18h/mês para 42s) e Machine Learning.\n\n` +
    `Quer que eu resuma os resultados de algum projeto específico ou prefere falar diretamente com a Beatriz no **WhatsApp** (${WHATSAPP_LINK})?`
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
    .replace(
      /https:\/\/api\.whatsapp\.com\/send\/\?phone=%2B5531988434917&amp;text&amp;type=phone_number&amp;app_absent=0/g,
      `<a href="${WHATSAPP_LINK}" target="_blank" rel="noopener noreferrer">Abrir WhatsApp (+55 31 98843-4917) ↗</a>`
    )
    .replace(
      /(https:\/\/(?!api\.whatsapp\.com)[^\s)<]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    )
    .replace(
      /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g,
      '<a href="mailto:$1">$1</a>'
    );
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

async function queryLocalDatabricksApp(messages) {
  if (window.location.hostname.endsWith("github.io")) {
    return null;
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (response.ok) {
      const data = await response.json();
      if (data && data.reply) return data.reply;
    }
  } catch (_) {
    clearTimeout(timer);
  }
  return null;
}

async function queryPublicLLM(messages) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 14000);
  try {
    const payload = {
      model: "openai",
      messages: [
        { role: "system", content: BIA_SYSTEM_PROMPT },
        ...messages.slice(-6),
      ],
    };
    const response = await fetch("https://text.pollinations.ai/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (response.ok) {
      const text = (await response.text()).trim();
      if (text && text.length > 10 && !text.startsWith("<!DOCTYPE")) {
        return text;
      }
    }
  } catch (_) {
    clearTimeout(timer);
  }
  return null;
}

async function sendChatMessage(userText) {
  const clean = userText.trim();
  if (!clean) return;
  appendBubble("user", clean);
  chatHistory.push({ role: "user", content: clean });

  const loadingBubble = appendBubble("assistant", "BIA está preparando a resposta...");

  // 1. Try Databricks App backend (/api/chat -> Databricks Model Serving)
  let reply = await queryLocalDatabricksApp(chatHistory);

  // 2. If on static GitHub Pages, call live LLM with BIA 80/15/5 system prompt
  if (!reply) {
    reply = await queryPublicLLM(chatHistory);
  }

  // 3. Fallback to empathetic 80/15/5 local response if offline/timeout
  if (!reply) {
    reply = biaSmartFallback(clean);
  }

  // Ensure WhatsApp & contact links are always accurate when asked
  reply = ensureContactLinks(reply, clean);

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
