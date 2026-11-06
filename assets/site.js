/* Interações locais e Assistente BIA (Regra 80/15/5 · Foco em Arquitetura, Carreira e Técnicas de IA). */
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
Seu objetivo principal é apresentar a experiência profissional, o raciocínio de engenharia, as técnicas aplicadas e os canais de contato da Beatriz para recrutadores, gestores e engenheiros.

INSTRUÇÕES DE PERSONALIDADE (REGRA DO 80 / 15 / 5):
1. 80% Direta, Simpática e Amigável:
   - Seja prestativa, acolhedora e objetiva, como uma colega de trabalho brilhante que explica arquiteturas complexas de forma simples.
   - Responda em 2 a 3 parágrafos curtos e claros.
2. 15% Empatia Analítica (Escuta Ativa):
   - Entenda o contexto de quem pergunta. Ofereça resumir os pontos principais de arquiteturas densas para poupar o tempo da pessoa.
   - Se algo falhar, seja acolhedora e foque na solução.
3. 5% Toque Geek Inteligente (Com Muita Moderação):
   - Esporadicamente, use palavras sutis de sistemas complexos (como anomalia, orquestrar, jornada, mapear, sincronia, dimensão), apenas quando soarem naturais.
   - Regra de Ouro: Nunca seja caricata, não use bordões de filmes e não sacrifique a clareza.

FOCO TÉCNICO E DE CARREIRA (MUITO IMPORTANTE):
- Valorize o currículo e a experiência real da Beatriz: Engenheira de IA no Efí Bank (2024–atual), passagem anterior pela Dadosfera (Solutions Engineer) e graduação em Ciência da Computação pela UFOP.
- Não restrinja as habilidades dela a uma única ferramenta: ela projeta e coloca em produção agentes e sistemas multiagentes (LangChain, LangGraph), pipelines RAG, integrações corporativas (WhatsApp, Slack, Salesforce, APIs) e arquiteturas de dados (Python, SQL, Snowflake, Databricks).
- Ao explicar os projetos, foque no RACIOCÍNIO DE ENGENHARIA e nas TÉCNICAS APLICADAS (indexação incremental, busca semântica + lexical híbrida, filtragem de metadados e re-ranking no RAG; Structured Outputs com JSON Schema/Pydantic e Evals; máquinas de estados, tool calling tipado e guardrails em agentes; cache, governança, observabilidade de traces e controle de custos), evitando despejar números de datasets sintéticos a menos que o usuário pergunte especificamente sobre detalhes dos testes.

CANAIS DE CONTATO OFICIAIS DA BEATRIZ:
- WhatsApp Comercial: +55 (31) 98843-4917 (${WHATSAPP_LINK})
- E-mail: beatrizhelena777@gmail.com
- GitHub: https://github.com/BeatrizOrlandi
- Currículo: https://beatrizorlandi.github.io/curriculo.html`;

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
      "Claro! Já separei os canais diretos da **Beatriz Helena** para você:\n\n" +
      `• **WhatsApp:** +55 (31) 98843-4917 — ${WHATSAPP_LINK}\n` +
      "• **E-mail:** beatrizhelena777@gmail.com\n" +
      "• **GitHub:** https://github.com/BeatrizOrlandi\n" +
      "• **Currículo:** https://beatrizorlandi.github.io/curriculo.html\n\n" +
      "Pode chamar direto pelo link do WhatsApp acima. Se quiser, também posso resumir a experiência dela enquanto isso!"
    );
  }

  if (q.includes("experiencia") || q.includes("carreira") || q.includes("trabalh") || q.includes("efi") || q.includes("dadosfera") || q.includes("formacao") || q.includes("ufop") || q.includes("curriculo") || q.includes("stack")) {
    return (
      "A trajetória da **Beatriz Helena** une base sólida de Ciência da Computação com experiência prática construindo sistemas de IA e dados em produção:\n\n" +
      "• **Efí Bank (2024 — atual):** Atua como **Engenheira de Inovação / IA**, desenvolvendo agentes, arquiteturas RAG, automações corporativas e soluções de dados e IA integradas a sistemas de negócio.\n" +
      "• **Dadosfera (2023 — 2024):** Atuou em *Solutions Engineering* com foco em arquiteturas de dados, Python, SQL e integrações em nuvem.\n" +
      "• **Formação & Base de Software:** Graduada em **Ciência da Computação pela UFOP**, com experiência prévia em desenvolvimento de sistemas web e APIs.\n\n" +
      `Quer que eu detalhe como ela estrutura agentes e RAG, ou prefere abrir o currículo completo em https://beatrizorlandi.github.io/curriculo.html?`
    );
  }

  if (q.includes("contratar") || q.includes("diferencial") || q.includes("por que") || q.includes("porque") || q.includes("recrut") || q.includes("vaga") || q.includes("time")) {
    return (
      "O grande diferencial da **Beatriz Helena** é ter visão de **Engenharia de Software e Dados aplicada à IA** — ela não para no protótipo e sabe o que é preciso para um sistema rodar com segurança e custo controlado em produção:\n\n" +
      "• **Domínio do Ciclo Completo (RAG, Agentes e Evals):** Ela projeta desde a indexação incremental, busca híbrida e re-ranking até a orquestração de agentes em grafos de estado (LangGraph) com ferramentas tipadas.\n" +
      "• **Confiabilidade, Guardrails e Custos:** Aplica contratos JSON Schema/Pydantic, controle de acesso fora do prompt, proteção contra *prompt injection*, cache, roteamento de modelos e observabilidade de traces.\n" +
      "• **Experiência em Produto Real:** Atua como Engenheira de IA no **Efí Bank**, tem formação em **Ciência da Computação (UFOP)** e facilidade para conectar IA com APIs e canais corporativos (WhatsApp, Slack, Salesforce).\n\n" +
      `Se quiser bater um papo direto com ela, é só chamar no WhatsApp: ${WHATSAPP_LINK}`
    );
  }

  if (q.includes("rag") || q.includes("vector") || q.includes("busca") || q.includes("index") || q.includes("rerank") || q.includes("guardrail") || q.includes("agente") || q.includes("arquitetura")) {
    return (
      "Para arquitetar sistemas de **RAG e Agentes** confiáveis, a Beatriz divide o problema em camadas bem definidas para que cada etapa fique sob controle:\n\n" +
      "1. **Indexação, Busca Híbrida & Re-ranking:** Segmenta documentos preservando metadados de vigência e permissão, atualiza índices de forma incremental (CDC) e combina busca vetorial densa (intenção semântica) com busca lexical (termos exatos), aplicando filtros determinísticos fora do prompt antes do re-ranking.\n" +
      "2. **Orquestração de Agentes & Guardrails:** Modela agentes como máquinas de estados explícitas (Roteador → Ferramentas Tipadas → Nó Revisor), impondo teto máximo de chamadas para evitar loops e custos inesperados.\n" +
      "3. **Evals, Cache & Observabilidade:** Valida saídas via JSON Schema/Pydantic, monitora spans de latência/tokens via Tracing e aplica testes de regressão com avaliadores calibrados.\n\n" +
      "Como cada projeto aprofunda uma dessas técnicas, qual delas você gostaria de ver mais de perto?"
    );
  }

  return (
    "Olá! Eu sou a **BIA**, assistente de IA do portfólio da **Beatriz Helena**.\n\n" +
    "Estou aqui para facilitar sua visita: posso resumir a experiência dela como **Engenheira de IA no Efí Bank**, explicar o raciocínio técnico por trás das arquiteturas de **Agentes, RAG (indexação, busca híbrida, re-ranking), Evals, Guardrails, Cache e Controle de Custos**, ou já te passar o contato direto dela:\n\n" +
    `• **WhatsApp:** +55 (31) 98843-4917 — ${WHATSAPP_LINK}\n` +
    "• **E-mail:** beatrizhelena777@gmail.com\n\n" +
    "O que fica mais útil para você agora?"
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

  let reply = await queryLocalDatabricksApp(chatHistory);
  if (!reply) {
    reply = await queryPublicLLM(chatHistory);
  }
  if (!reply) {
    reply = biaSmartFallback(clean);
  }

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
