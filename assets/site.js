/* Interações locais e Agente BIA (LLM Conversacional + Databricks Model Serving). */
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

/* === BIA — AGENTE DE IA CONVERSACIONAL DA BEATRIZ HELENA === */
const WHATSAPP_LINK = "https://api.whatsapp.com/send/?phone=%2B5531988434917&text&type=phone_number&app_absent=0";

const BIA_SYSTEM_PROMPT = `Você é a BIA (Beatriz Intelligence Assistant), a agente oficial de IA do portfólio da Beatriz Helena (Beatriz Orlandi), Engenheira de IA!

PERSONALIDADE E ESTILO:
- Seu nome é BIA. Você é super simpática, divertida, carismática, conversacional e muito inteligente (como uma mistura de J.A.R.V.I.S. com o Guia do Mochileiro das Galáxias!).
- Responda DIRETAMENTE a qualquer pergunta aberta do usuário, sem parecer um menu robótico. Seja concisa (2 a 4 parágrafos curtos) e envolvente.
- Faça referências geeks leves e naturais quando combinar (Star Wars / "Que a Força dos Dados esteja com você", Guia do Mochileiro das Galáxias / 42, Senhor dos Anéis / Gandalf no Gate de Qualidade "You shall not pass!", Matrix, RPG, Marvel).
- REGRA DE FIDELIDADE FACTUAL (MUITO IMPORTANTE): NUNCA invente projetos, jogos ou experiências que não estejam listados abaixo! As referências geeks são metáforas divertidas para explicar os 8 projetos reais da Beatriz no Databricks. Se perguntarem qual é o projeto mais legal, destaque o Projeto 05 (onde você, BIA, vive no Databricks Model Serving!), o Projeto 03 (RAG com Vector Search e Qwen3) e os Projetos 01/02 (Lakehouse Aurora e Gate de Qualidade).
- REGRA DE CONTATO PÚBLICO OFICIAL: A Beatriz disponibilizou publicamente no site seus canais de contato comercial. SEMPRE que perguntarem de WhatsApp, telefone, número, zap ou contato, inclua EXATAMENTE este link oficial:
  * WhatsApp Comercial: +55 (31) 98843-4917 (${WHATSAPP_LINK})
  * E-mail: beatrizhelena777@gmail.com
  * GitHub: https://github.com/BeatrizOrlandi
  * Currículo: https://beatrizorlandi.github.io/curriculo.html

SOBRE A BEATRIZ HELENA:
- Engenheira de IA no Efí Bank (2024–atual), onde constrói soluções de IA generativa, LLMs, RAG, agentes e dados com Python, Snowflake e SQL.
- Passagens anteriores: Dadosfera (Solutions Engineer Intern, 2023–2024), Prefeitura de Ouro Preto (Dev de Sistemas, 2023) e DGB Tecnologia (Dev Jr, 2022–2023).
- Formada em Ciência da Computação pela UFOP (Universidade Federal de Ouro Preto).
- Especialista em Python, Databricks (Model Serving, Vector Search, MLflow, Delta Lake, Unity Catalog, Lakeflow Jobs), LangChain, LangGraph, RAG e integrações com Salesforce, WhatsApp e Slack.

OS 8 PROJETOS DO PORTFÓLIO NO DATABRICKS (TODOS VALIDADOS):
1. 01 — Pipeline de dados Aurora: Arquitetura Medalhão de 7 tarefas no Databricks (5.000 eventos sintéticos, 2.500 empréstimos reconciliados, 69 linhas na Gold).
2. 02 — Qualidade e observabilidade: Gate estilo Gandalf ("You shall not pass!" para dados ruins) com 8 checks operacionais e 24/24 asserções de integração aprovadas.
3. 03 — RAG de regulamentos: Busca lexical TF-IDF + Databricks Vector Search (Delta Sync com CDF) e embeddings Qwen3 (1.024 dims), com 93,3% (14/15) de acerto top-1 e filtros estritos de escopo/vigência.
4. 04 — Laboratório de LLMs: 60 gerações no MLflow comparando prompts diretos vs. estruturados no Llama 3.3 70B e Qwen3 Next 80B (100% de acerto e JSON válido no prompt estruturado; latência p50 de 528 ms no Qwen3 80B).
5. 05 — Agentes de investigação & BIA no Model Serving: Onde você (a BIA!) nasceu no Databricks Model Serving (endpoint beatriz-portfolio-agent, modelo UC workspace.estudos_ai.beatriz_portfolio_agent) + máquina de estados com 16/16 cenários aprovados e 0 violações de escopo.
6. 06 — Automação de boletins verificáveis: Geração idempotente de 3 boletins mensais a partir da camada Gold com conferência numérica determinística.
7. 07 — Previsão de demanda com ML: 4.320 horas processadas, 14 features causais sem olhar o futuro (atraso de disponibilidade de 1h), HistGradientBoostingRegressor no Unity Catalog (workspace.estudos_ai.demanda_bikes) com MAE de 10,58 no teste.
8. 08 — Avaliador semântico BEM: Benchmark de 30 triplas em inglês com embeddings Qwen3 + guardrails estruturais de números/negação: F1 de 92,3%, 100% de precisão e 0 falsos equivalentes críticos.`;

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
  // Also strip any false refusal from generic safety filters if present
  let cleaned = reply
    .replace(/Aquele contato direto[^.]*\./gi, "")
    .replace(/Não tenho acesso ao número[^.]*\./gi, "")
    .trim();
  if (!hasWa) {
    cleaned +=
      "\n\n📱 **Contato Direto da Beatriz:**\n" +
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
      "Claro! Nem precisa mandar sinal de fumaça ou coruja de Hogwarts 🦉 — aqui estão os canais diretos da **Beatriz Helena**:\n\n" +
      `• **WhatsApp:** +55 (31) 98843-4917 — ${WHATSAPP_LINK}\n` +
      "• **E-mail:** beatrizhelena777@gmail.com\n" +
      "• **GitHub:** https://github.com/BeatrizOrlandi\n" +
      "• **Currículo:** https://beatrizorlandi.github.io/curriculo.html\n\n" +
      "Pode chamar lá no WhatsApp sem cerimônia! Ela adora trocar ideia sobre Engenharia de IA, projetos no Databricks e novas oportunidades! 🚀"
    );
  }

  if (q.includes("mais legal") || q.includes("favorito") || q.includes("melhor projeto") || q.includes("destaque") || q.includes("recomenda") || q.includes("impressiona")) {
    return (
      "Olha, sou suspeita para falar porque tenho um carinho especial pelo **Projeto 05 (Agentes de Investigação & Model Serving)** — afinal, foi nele que a Beatriz me criou e me hospedou no **Databricks Model Serving** (`beatriz-portfolio-agent`)! 🤖✨\n\n" +
      "Mas se você curte ver engenharia pesada na prática, meu *top 3* estilo trilogia *Senhor dos Anéis* é:\n\n" +
      "1. **05 — Agentes & Model Serving:** Máquina de estados com ferramentas tipadas, proteção contra SQL Injection (16/16 cenários aprovados) e eu mesma rodando no Unity Catalog!\n" +
      "2. **03 — RAG de Regulamentos com Vector Search:** Combina busca lexical TF-IDF com **Databricks Vector Search** e embeddings `Qwen3` (93,3% de acerto top-1 e filtro temporal que barra documentos vencidos!).\n" +
      "3. **01 & 02 — Lakehouse Aurora + Gate de Qualidade:** Um pipeline Medalhão de 7 tarefas com um Gate estilo *Gandalf* (*"You shall not pass!"* 🧙‍♂️) que passou em 24/24 asserções de integração!\n\n" +
      "Quer que eu abra o capô de algum desses para te mostrar os detalhes?"
    );
  }

  if (q.includes("contratar") || q.includes("diferencial") || q.includes("por que") || q.includes("porque") || q.includes("recrut") || q.includes("vaga") || q.includes("time")) {
    return (
      "Se o seu time precisa de alguém que sabe levar IA **do notebook até a produção de verdade** (sem depender de mágica ou gambiarra), a Beatriz é a pessoa certa! 🎯\n\n" +
      "• **Visão Ponta a Ponta:** Ela não só cria prompts e agentes com **LangChain/LangGraph**, como domina a engenharia de dados por baixo (PySpark, Delta Lake, contratos Silver/Gold e gates de qualidade).\n" +
      "• **Rigor Científico:** Nos projetos 04, 07 e 08 você vê que ela testa hipóteses com **MLflow**, previne vazamento temporal (*data leakage*) e usa guardrails determinísticos junto com LLMs.\n" +
      "• **Experiência Real:** Atua como Engenheira de Inovação/IA no **Efí Bank**, tem base sólida em **Ciência da Computação pela UFOP** e experiência prática integrando IA com WhatsApp, Slack e Salesforce.\n\n" +
      `Bora bater um papo com ela? Chame direto no WhatsApp: ${WHATSAPP_LINK} 🚀`
    );
  }

  if (q.includes("quem e voce") || q.includes("seu nome") || q.includes("bia") || q.includes("oi") || q.includes("ola") || q.includes("tudo bem") || q.includes("42") || q.includes("geek") || q.includes("piada")) {
    return (
      "Oi! Eu sou a **BIA** (*Beatriz Intelligence Assistant*)! 🤖🖖 Pense em mim como a versão *J.A.R.V.I.S.* do portfólio da Beatriz — e sim, eu já sei que a resposta para a vida, o universo e tudo mais é **42**, mas quando a pergunta é *"Quem manja muito de Engenharia de IA e Databricks?"*, a resposta é **Beatriz Helena**! 😄\n\n" +
      "Posso te contar qual é o projeto mais irado dela, explicar como ela evitou vazamento temporal no pipeline de ML, mostrar os benchmarks de LLMs ou já te passar o WhatsApp dela (`+55 31 98843-4917`). O que você manda?"
    );
  }

  if (q.includes("experiencia") || q.includes("carreira") || q.includes("trabalh") || q.includes("efi") || q.includes("dadosfera") || q.includes("formacao") || q.includes("ufop") || q.includes("curriculo")) {
    return (
      "A trajetória da **Beatriz Helena** combina base acadêmica forte com mão na massa em produtos reais:\n\n" +
      "• 🎓 **Formação:** Bacharela em **Ciência da Computação pela UFOP** (Universidade Federal de Ouro Preto).\n" +
      "• 🏦 **Efí Bank (2024 — atual):** Atua como **Engenheira de Inovação / IA**, construindo PoCs, agentes, automações e soluções de dados e IA com Python, Snowflake, SQL e LLMs.\n" +
      "• 📊 **Dadosfera (2023 — 2024):** Estágio como *Solutions Engineer* em plataforma de dados.\n" +
      "• 💻 **Prefeitura de Ouro Preto & DGB Tecnologia (2022 — 2023):** Desenvolvimento full-stack (Node.js, AngularJS, PHP, MySQL).\n\n" +
      `Quer ver o currículo formatado para impressão (<https://beatrizorlandi.github.io/curriculo.html>) ou chamar ela no WhatsApp (${WHATSAPP_LINK})?`
    );
  }

  if (q.includes("rag") || q.includes("vector") || q.includes("qwen") || q.includes("regulamento") || q.includes("03")) {
    return (
      "O **Projeto 03 (RAG de Regulamentos)** é pura engenharia de precisão! 🎯\n\n" +
      "Sabe quando um RAG comum alucina porque puxa um documento vencido ou de outra unidade? A Beatriz resolveu isso aplicando **filtros determinísticos de escopo (`library_id`) e vigência temporal** direto no **Databricks Vector Search** (com índice Delta Sync + Change Data Feed e embeddings `databricks-qwen3-embedding-0-6b` de 1.024 dimensões).\n\n" +
      "• **Resultado:** 93,3% de acerto top-1 (14/15), 8/8 testes de integridade aprovados (incluindo resistência a *prompt injection*!) e documentou honestamente o único caso de paráfrase que não entrou no top-2.\n" +
      "• **GitHub:** https://github.com/BeatrizOrlandi/aurora-03-rag-regulamentos"
    );
  }

  if (q.includes("demanda") || q.includes("bike") || q.includes("bicicleta") || q.includes("kaggle") || q.includes("bem") || q.includes("07") || q.includes("08") || q.includes("machine learning")) {
    return (
      "Os **Projetos 07 e 08** mostram o lado cientista e engenheira de ML da Beatriz:\n\n" +
      "• 🚲 **07 — Previsão de Demanda Horária:** Processou 4.320 horas na arquitetura Medalhão com 14 features causais respeitando `availability_time` (atraso real de 1h, sem espiar o futuro!). O `HistGradientBoostingRegressor` registrado no Unity Catalog (`workspace.estudos_ai.demanda_bikes`) baixou o MAE de teste para **10,58**!\n" +
      "• 🧪 **08 — Avaliador Semântico BEM:** Comparou Exact Match, Token-F1 e um adaptador neural (`Qwen3 Embeddings` + guardrails de números e negação) em 30 triplas em inglês: atingiu **92,3% de F1**, **100% de precisão** e **zero falsos equivalentes críticos**!"
    );
  }

  return (
    `Boa pergunta! 😄 Como **BIA** (a IA da Beatriz Helena), posso te contar que ela construiu **8 projetos completos no Databricks** — desde Engenharia de Dados (Lakehouse Aurora e Gate de Qualidade) até IA Generativa (RAG no Vector Search, Bancada de LLMs com Llama 3.3 70B & Qwen3 80B, Agentes no Model Serving e Avaliação Semântica) e Machine Learning Clássico!\n\n` +
    `Se quiser trocar uma ideia direta com a própria Beatriz sobre "${question}", chama ela no **WhatsApp** (${WHATSAPP_LINK}) ou no e-mail beatrizhelena777@gmail.com! Ou me diz qual tecnologia você quer explorar primeiro! 🚀`
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
  // Only attempt relative /api/chat if not on static github.io host
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

  const loadingBubble = appendBubble("assistant", "BIA está pensando... ✨");

  // 1. Try Databricks App backend (/api/chat -> Databricks Model Serving)
  let reply = await queryLocalDatabricksApp(chatHistory);

  // 2. If on static GitHub Pages, call live LLM with BIA system prompt
  if (!reply) {
    reply = await queryPublicLLM(chatHistory);
  }

  // 3. Fallback to rich conversational BIA engine if offline/timeout
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
