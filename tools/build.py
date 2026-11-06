"""Gera o site estático com Python 3, sem dependências de terceiros.

Uso, na raiz do pacote: python tools/build.py
As páginas geradas já acompanham a entrega; não é preciso executar para publicar.
"""
from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "conteudo/perfil.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "conteudo/projetos.json").read_text(encoding="utf-8"))


def e(value):
    return escape(str(value), quote=True)


def write(path, text):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(text.encode("utf-8"))


def tags(values):
    return '<ul class="tags" aria-label="Tecnologias">' + ''.join(f'<li>{e(v)}</li>' for v in values) + '</ul>'


def bullet(values):
    return '<ul class="prose-list">' + ''.join(f'<li>{e(v)}</li>' for v in values) + '</ul>'


def public_links():
    result = []
    for key, label in [("github", "GitHub"), ("whatsapp", "WhatsApp"), ("linkedin", "LinkedIn"), ("email", "E-mail")]:
        value = PROFILE["links"].get(key, "").strip()
        if not value:
            continue
        if key == "email":
            if not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", value):
                raise ValueError("E-mail inválido no perfil")
            href = "mailto:" + value
        else:
            if not value.startswith("https://"):
                raise ValueError("Links profissionais devem usar https://")
            href = value
        result.append(f'<a href="{e(href)}" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>')
    return ''.join(result)


def layout(title, description, body, prefix="", page="home", canonical_path="index.html"):
    home = prefix + "index.html"
    nav = ''.join(f'<a href="{home}#{anchor}">{label}</a>' for anchor, label in [
        ("experiencia", "Experiência"),
        ("arquitetura-ia", "Técnicas & Arquitetura"),
        ("projetos", "Projetos"),
    ])
    canonical = ""
    site_url = PROFILE.get("site_url", "").strip().rstrip("/")
    if site_url:
        if not site_url.startswith("https://"):
            raise ValueError("site_url deve usar https://")
        canonical = f'<link rel="canonical" href="{e(site_url)}/{e(canonical_path)}">'
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#163c3a">
  <meta name="description" content="{e(description)}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  {canonical}
  <title>{e(title)}</title>
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=bia6">
  <script src="{prefix}assets/site.js?v=bia6" defer></script>
</head>
<body data-page="{e(page)}">
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <header class="site-header wrap">
    <a class="brand" href="{home}" aria-label="{e(PROFILE['nome'])} — início"><span class="monogram" aria-hidden="true">bh.</span><span>{e(PROFILE['nome'])}<small>Engenharia de IA</small></span></a>
    <nav aria-label="Navegação principal">{nav}<a href="{prefix}documentacao/prompts.html">Prompts ↗</a><a class="nav-cv" href="{prefix}curriculo.html">Currículo <span aria-hidden="true">↗</span></a></nav>
  </header>
  <main id="conteudo">{body}</main>
  <footer class="site-footer wrap"><div><a class="footer-name" href="{home}">{e(PROFILE['nome'])}<span>Engenheira de IA</span></a><p>Engenharia de IA · Agentes, RAG, LLMs, Guardrails, Observabilidade e Dados.</p></div><div class="footer-links">{public_links()}<a href="{prefix}documentacao/prompts.html">Engenharia de Prompts ↗</a><a href="{prefix}curriculo.html">Ver currículo ↗</a><a href="{home}#experiencia">Experiência ↑</a></div><p class="fineprint">© {date.fromisoformat(PROFILE['atualizacao_site']).year} {e(PROFILE['nome'])}. Portfólio profissional e estudos de arquitetura de IA.</p></footer>
  <button type="button" class="chat-fab" data-chat-toggle aria-expanded="false" aria-controls="chat-assistant">
    <span class="chat-fab-dot" aria-hidden="true"></span>
    <span>Conversar com a BIA (IA) ✨</span>
  </button>
  <aside id="chat-assistant" class="chat-drawer" data-chat-drawer hidden aria-label="BIA — Assistente de IA da Beatriz Helena">
    <div class="chat-header">
      <div class="chat-header-info">
        <strong>BIA · Assistente de IA da Beatriz</strong>
        <small>Agente de IA · Arquitetura, Carreira &amp; Projetos</small>
      </div>
      <button type="button" class="chat-close" data-chat-close aria-label="Fechar chat">Fechar ✕</button>
    </div>
    <div class="chat-messages" data-chat-messages aria-live="polite">
      <div class="chat-bubble assistant">
        <p>Olá! Eu sou a <strong>BIA</strong> (<em>Beatriz Intelligence Assistant</em>), assistente de IA do portfólio da Beatriz Helena.</p>
        <p>Posso resumir a experiência profissional dela, explicar como ela estrutura arquiteturas de Agentes, RAG, Guardrails e Evals, ou já te passar o <strong>WhatsApp</strong> e <strong>e-mail</strong> direto. Como posso ajudar?</p>
      </div>
    </div>
    <div class="chat-chips" aria-label="Perguntas sugeridas">
      <button type="button" class="chat-chip" data-chat-prompt="Qual é a experiência profissional e stack principal da Beatriz?">Experiência &amp; Stack 💼</button>
      <button type="button" class="chat-chip" data-chat-prompt="Como a Beatriz arquiteta soluções de RAG, Agentes e Guardrails?">RAG, Agentes &amp; Guardrails 🧠</button>
      <button type="button" class="chat-chip" data-chat-prompt="Você tem o WhatsApp e contato da Beatriz?">WhatsApp &amp; Contato 📱</button>
      <button type="button" class="chat-chip" data-chat-prompt="Por que devo contratar a Beatriz para o meu time de IA?">Por que contratar? 💡</button>
    </div>
    <form class="chat-form" data-chat-form>
      <label class="sr-only" for="chat-input-field">Pergunte qualquer coisa para a BIA</label>
      <input id="chat-input-field" data-chat-input type="text" placeholder="Pergunte sobre experiência, RAG, agentes ou contato..." autocomplete="off">
      <button type="submit">Enviar</button>
    </form>
  </aside>
</body>
</html>
'''


def metrics(items):
    return '<dl class="metrics">' + ''.join(f'<div><dt>{e(x["valor"])}</dt><dd>{e(x["rotulo"])}</dd></div>' for x in items) + '</dl>'


def project_card(p):
    # Home page card focuses strictly on engineering problem, reasoning, and techniques (no synthetic metrics or heavy banners)
    decisions_preview = '<ul class="card-techniques">' + ''.join(f'<li>{e(d)}</li>' for d in p['decisoes'][:2]) + '</ul>'
    return f'''<article class="project-card" data-project data-group="{e(p['grupo'])}" data-search="{e(' '.join([p['titulo'], p['subtitulo'], p['categoria'], *p['stack']]))}">
  <div class="card-meta"><span class="mono">{p['numero']} / {e(p['categoria'])}</span><span class="status {p['grupo']}">{e(p['status'])}</span></div>
  <h3><a href="projetos/{p['slug']}.html">{e(p['titulo'])}<span aria-hidden="true">↗</span></a></h3>
  <p>{e(p['resumo'])}</p>
  {decisions_preview}
  {tags(p['stack'])}
  <a class="text-link" href="projetos/{p['slug']}.html" aria-label="Ver arquitetura e detalhes: {e(p['titulo'])}">Ver arquitetura, raciocínio e implementação <span aria-hidden="true">→</span></a>
</article>'''


def trajectory():
    return '<ol class="timeline">' + ''.join(f'''<li><div class="timeline-date mono">{e(x['periodo'])}</div><div class="timeline-body"><h3>{e(x['empresa'])}</h3><p class="role">{e(x['cargo'])}</p>{f'<p>{e(x["descricao"])}</p>' if x['descricao'] else ''}</div></li>''' for x in PROFILE['experiencias']) + '</ol>'


def build_home():
    skills = ''.join(f'''<article class="skill"><span class="mono">0{i + 1}</span><h3>{e(x['titulo'])}</h3><p>{e(x['descricao'])}</p>{tags(x['tecnologias'])}</article>''' for i, x in enumerate(PROFILE['habilidades']))
    body = f'''
<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy">
    <p class="eyebrow"><span class="tiny-square" aria-hidden="true"></span> ENGENHARIA DE IA · AGENTES, RAG, LLMS &amp; DADOS</p>
    <h1 id="hero-title">Beatriz<br>Helena</h1>
    <p class="hero-role">Engenheira de IA · Efí Bank</p>
    <p class="hero-intro">Desenvolvo soluções de IA Generativa de ponta a ponta — da concepção arquitetural à operação em produção. Atuo na construção de agentes de IA, pipelines RAG (indexação, busca semântica/híbrida e re-ranking), avaliação sistemática (Evals), guardrails, controle de custos e integrações corporativas.</p>
    <div class="actions">
      <a class="button primary" href="#experiencia">Experiência &amp; Currículo <span aria-hidden="true">↘</span></a>
      <button type="button" class="button secondary" data-open-chat>Conversar com a BIA (minha IA) ✨</button>
      <a class="text-link" href="#arquitetura-ia">Ver técnicas e arquitetura →</a>
    </div>
  </div>
  <div class="system-panel">
    <div class="panel-label mono"><span class="notebook-name">● ● ● &nbsp; ai_engineering_stack.py</span><span>ARQUITETURA EM PRODUÇÃO</span></div>
    <p class="panel-heading">Engenharia<br><span>de Sistemas de IA</span></p>
    <p class="panel-caption mono">DO CONTEXTO BRUTO À DECISÃO GOVERNADA</p>
    <ol class="system-flow">
      <li><span>01</span><div><strong>RAG, Indexação &amp; Re-ranking</strong><small>Chunking semântico, busca vetorial + lexical e filtros de governança</small></div><b aria-hidden="true">↓</b></li>
      <li><span>02</span><div><strong>Orquestração de Agentes &amp; Tools</strong><small>Grafos de estado, roteamento de intenção, memória e APIs</small></div><b aria-hidden="true">↓</b></li>
      <li><span>03</span><div><strong>Guardrails, Evals, Cache &amp; Custos</strong><small>Contratos JSON Schema, observabilidade de traces e eficiência</small></div></li>
    </ol>
    <a href="#arquitetura-ia">Explorar raciocínio de engenharia e padrões aplicados <span aria-hidden="true">↗</span></a>
  </div>
</section>

<div class="expertise-strip"><div class="wrap"><span>Agentes &amp; LangGraph</span><span>RAG, Busca Híbrida &amp; Re-ranking</span><span>Prompt Engineering &amp; Evals</span><span>Guardrails, Cache &amp; Custos</span><span>Python, SQL &amp; Dados</span><span>Integrações (WhatsApp, Slack, CRM)</span></div></div>

<section id="experiencia" class="section wrap" aria-labelledby="career-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">01 / CURRÍCULO &amp; TRAJETÓRIA PROFISSIONAL</p>
      <h2 id="career-title">Experiência, formação<br>e visão de produção</h2>
    </div>
    <a class="button secondary" href="curriculo.html">Abrir currículo para impressão ↗</a>
  </div>

  <div class="about-layout" style="margin-bottom: 52px;">
    <div>
      <p class="eyebrow">PERFIL PROFISSIONAL</p>
      <h3 style="font-size: 1.75rem; line-height: 1.25;">Engenharia de Software, Dados e IA Generativa conectadas ao negócio</h3>
    </div>
    <div class="about-copy" style="padding-top: 0;">
      {''.join(f'<p>{e(x)}</p>' for x in PROFILE['sobre'])}
      <p class="about-detail">{e(PROFILE['resumo'])}</p>
    </div>
  </div>

  <div class="skills-grid" style="margin-bottom: 64px;">{skills}</div>

  <div class="career-layout">
    {trajectory()}
    <aside class="education">
      <p class="eyebrow">FORMAÇÃO ACADÊMICA</p>
      <div class="education-mark" aria-hidden="true">↗</div>
      <h3>{e(PROFILE['formacao']['curso'])}</h3>
      <p>{e(PROFILE['formacao']['instituicao'])}</p>
      <span class="mono">BASE SÓLIDA EM ALGORITMOS, ENGENHARIA DE SOFTWARE, DADOS E IA</span>
    </aside>
  </div>

  <figure class="case-diagram" style="margin-top: 64px; margin-bottom: 0;">
    <img src="assets/arquitetura-corporativa-ia.svg" alt="Arquitetura de referência para sistemas de IA em produção: Canais, Guardrails, Orquestração de Agentes, Cache, RAG Híbrido e Observabilidade" width="960" height="360" loading="lazy">
    <figcaption class="mono">REPRESENTAÇÃO ARQUITETURAL · PADRÃO DE INTEGRAÇÃO DE AGENTES, RAG HÍBRIDO, GUARDRAILS E CONTROLE DE CUSTOS EM AMBIENTES CORPORATIVOS</figcaption>
  </figure>
</section>

<section id="arquitetura-ia" class="section wrap pillars-section" aria-labelledby="pillars-title" style="border-top: 1px solid var(--line);">
  <div class="section-heading">
    <div>
      <p class="eyebrow">02 / RACIOCÍNIO DE ENGENHARIA &amp; TÉCNICAS APLICADAS</p>
      <h2 id="pillars-title">Como projeto sistemas de IA</h2>
    </div>
    <p>Mais importante do que o modelo escolhido é a engenharia ao redor dele: indexação, recuperação, guardrails, avaliação contínua, cache, governança e controle de custos.</p>
  </div>
  <div class="pillars-grid">
    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">TÉCNICA 01 / RETRIEVAL &amp; CONTEXTO</span><span class="pillar-badge">Indexação · Busca Híbrida · Re-ranking</span></div>
      <h3>RAG, Indexação Incremental e Busca Semântica</h3>
      <p>A qualidade da geração depende diretamente da precisão do contexto recuperado. Estruturo pipelines RAG tratando ingestão, representação e filtragem antes mesmo de chamar o LLM:</p>
      <ul class="pillar-metrics">
        <li><strong>Chunking &amp; Indexação Incremental (CDC/CDF):</strong> segmentação preservando hierarquia documental e metadados temporais, reindexando apenas documentos alterados para reduzir custo de embeddings.</li>
        <li><strong>Busca Híbrida &amp; Re-ranking:</strong> combinação de busca vetorial densa (captura de intenção e paráfrases) com busca lexical (BM25/TF-IDF para códigos, siglas e termos exatos), seguida de filtragem determinística de permissão/vigência e re-ranking de relevância.</li>
      </ul>
      <div class="pillar-links">
        <a href="projetos/rag-regulamentos.html">Ver arquitetura de RAG e Busca Híbrida →</a>
      </div>
    </article>

    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">TÉCNICA 02 / PROMPTS &amp; AVALIAÇÃO</span><span class="pillar-badge">Structured Outputs · LLM Eval</span></div>
      <h3>Engenharia de Prompts, Contratos e Evals</h3>
      <p>Prompts em produção são contratos de software, não textos improvisados. Aplico engenharia sistemática para garantir saídas determinísticas e medir regressões a cada mudança:</p>
      <ul class="pillar-metrics">
        <li><strong>Structured Outputs (JSON Schema / Pydantic):</strong> imposição de schemas tipados, separação por delimitadores entre instruções de sistema e entradas do usuário, e regras explícitas de abstenção quando faltar evidência.</li>
        <li><strong>Bancada de Avaliação (Evals):</strong> datasets congelados com casos de borda, validação sintática/estrutural automatizada e avaliadores semânticos calibrados (evitando falsos positivos em números e negações).</li>
      </ul>
      <div class="pillar-links">
        <a href="documentacao/prompts.html">Catálogo de Prompts Estruturados ↗</a>
        <a href="projetos/laboratorio-llms.html">Ver estudo de LLM Eval →</a>
      </div>
    </article>

    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">TÉCNICA 03 / AGENTES &amp; SEGURANÇA</span><span class="pillar-badge">State Graphs · Guardrails</span></div>
      <h3>Orquestração de Agentes, Tool Calling e Guardrails</h3>
      <p>Agentes autônomos exigem limites claros de atuação. Desenho fluxos baseados em máquinas de estados (como LangGraph) onde o modelo decide o caminho, mas o runtime governa as permissões:</p>
      <ul class="pillar-metrics">
        <li><strong>Roteamento &amp; Ferramentas Tipadas:</strong> separação entre nós de roteamento, execução de ferramentas somente-leitura com argumentos validados e nó revisor que confere se a resposta possui lastro nas evidências.</li>
        <li><strong>Guardrails em Camadas:</strong> autorização de escopo fora do prompt (prevenindo vazamento cross-tenant), bloqueio de injeção de comandos/SQL e degradação graciosa em caso de timeout de APIs externas.</li>
      </ul>
      <div class="pillar-links">
        <a href="projetos/agentes-investigacao.html">Ver arquitetura de Agentes e Guardrails →</a>
      </div>
    </article>

    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">TÉCNICA 04 / EFICIÊNCIA &amp; MLOps</span><span class="pillar-badge">Cache · Governança · Custos</span></div>
      <h3>Cache, Observabilidade, Governança e Controle de Custos</h3>
      <p>Colocar IA em produção exige previsibilidade financeira, baixa latência e auditoria completa de cada decisão tomada pelo sistema:</p>
      <ul class="pillar-metrics">
        <li><strong>Controle de Custos &amp; Cache:</strong> teto rígido de <code>max_tokens</code> e de chamadas de ferramentas por sessão, cache por hash de requisição/semântica e roteamento inteligente para modelos mais leves e rápidos quando a tarefa permite.</li>
        <li><strong>Tracing, Linhagem &amp; Idempotência:</strong> instrumentação de spans por etapa (latência, inputs, outputs), versionamento de modelos e dados, e chaves de idempotência para evitar reprocessamentos duplicados.</li>
      </ul>
      <div class="pillar-links">
        <a href="projetos/qualidade-observabilidade.html">Ver estudo de Qualidade e Governança →</a>
      </div>
    </article>
  </div>
</section>

<section id="projetos" class="section wrap" aria-labelledby="projects-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">03 / ESTUDOS DE ARQUITETURA &amp; IMPLEMENTAÇÃO</p>
      <h2 id="projects-title">Projetos técnicos</h2>
    </div>
    <p>Oito implementações práticas detalhando o problema de engenharia, a arquitetura adotada, as decisões de trade-off e o código-fonte. Clique em qualquer projeto para ver os diagramas, testes e detalhes de execução.</p>
  </div>
  <div class="project-toolbar" hidden data-project-controls>
    <div class="filters" role="group" aria-label="Filtrar projetos">
      <button type="button" class="active" data-filter="todos" aria-pressed="true">Todos <span>{len(PROJECTS):02d}</span></button>
    </div>
    <label class="search"><span class="sr-only">Buscar projeto ou técnica</span><input data-search-input type="search" placeholder="Buscar técnica (ex: RAG, agentes, eval, cache...)" autocomplete="off"></label>
  </div>
  <p class="filter-count mono" data-filter-count aria-live="polite" hidden>{len(PROJECTS)} projetos</p>
  <div class="project-grid">{''.join(project_card(p) for p in PROJECTS)}</div>
  <p data-empty hidden class="empty-state">Nenhum projeto corresponde à busca. Tente outra tecnologia ou técnica.</p>
</section>
'''
    write("index.html", layout(f"{PROFILE['nome']} — Engenheira de IA", "Portfólio e currículo de Beatriz Helena, Engenheira de IA: Agentes, RAG, Busca Semântica, Re-ranking, Prompt Engineering, Evals, Guardrails e Dados.", body))


def build_projects():
    for index, p in enumerate(PROJECTS):
        next_p = PROJECTS[(index + 1) % len(PROJECTS)]
        outcome = metrics(p['resultados']) if p['resultados'] else ''
        evidence = f'<a class="text-link" href="../evidencias/{p["evidencia"]}" download>Baixar artefato de execução (JSON) ↓</a>' if p['evidencia'] else ''

        # Only show diagram + photo suggestion slot on the selected projects where visual evidence adds real value
        foto_info = p.get("sugestao_foto")
        visual_section = ""
        if foto_info:
            diagram_html = f'''<figure class="case-diagram">
  <img src="../{e(p["imagem"])}" alt="Diagrama técnico de arquitetura: {e(p["titulo"])}" width="800" height="340">
  <figcaption class="mono">REPRESENTAÇÃO ARQUITETURAL · FLUXO TÉCNICO E MECANISMOS DE CONTROLE</figcaption>
</figure>''' if p.get("imagem") else ""

            photo_file = ROOT / foto_info["arquivo"]
            if photo_file.is_file():
                photo_box = f'''<figure class="case-photo">
  <img src="../{e(foto_info["arquivo"])}" alt="Captura de tela da implementação: {e(p["titulo"])}" loading="lazy">
  <figcaption class="mono">CAPTURA DA IMPLEMENTAÇÃO · {e(p["titulo"].upper())}</figcaption>
</figure>'''
            else:
                photo_box = f'''<aside class="photo-slot" aria-label="Espaço reservado para captura de tela do projeto">
  <div class="photo-slot-header">
    <span class="mono">ESPAÇO RESERVADO PARA IMAGEM / SCREENSHOT</span>
    <code>{e(foto_info["arquivo"])}</code>
  </div>
  <p><strong>Sugestão de captura para anexar aqui:</strong> {e(foto_info["o_que_mostrar"])}</p>
  <p class="photo-slot-where"><strong>Onde tirar o print:</strong> {e(foto_info["onde_tirar"])}</p>
</aside>'''
            visual_section = diagram_html + photo_box

        body = f'''<div class="wrap case-breadcrumb"><a href="../index.html#projetos">← Voltar aos projetos</a><span class="mono">PROJETO {p['numero']} / 08</span></div><article class="case wrap"><header class="case-hero"><div><p class="eyebrow">{e(p['categoria'])}</p><h1>{e(p['titulo'])}</h1><p class="case-summary">{e(p['resumo'])}</p>{tags(p['stack'])}</div><aside class="case-meta"><span class="status {p['grupo']}">{e(p['status'])}</span><dl><dt>FOCO TÉCNICO</dt><dd>{e(p['subtitulo'])}</dd><dt>REPOSITÓRIO</dt><dd><a href="{e(p.get('repo_url', ''))}" rel="noopener noreferrer">Ver código no GitHub ↗</a></dd></dl></aside></header>
{visual_section}
<nav class="case-nav" aria-label="Conteúdo deste estudo"><a href="#problema">Problema &amp; Escopo</a><a href="#arquitetura">Arquitetura &amp; Raciocínio</a><a href="#resultados">Validação &amp; Trade-offs</a><a href="#material">Contratos &amp; Código</a></nav>
<section id="problema" class="case-section two-column"><div><p class="eyebrow">01 / CONTEXTO E DESAFIO</p><h2>Problema de engenharia</h2></div><div class="prose"><p>{e(p['problema'])}</p><h3>Solução implementada</h3><p>{e(p['entrega'])}</p></div></section>
<section id="arquitetura" class="case-section"><p class="eyebrow">02 / ARQUITETURA E RACIOCÍNIO TÉCNICO</p><h2>Etapas e decisões de projeto</h2><ol class="architecture" aria-label="Etapas da arquitetura">{''.join(f'<li><span class="mono">{i+1:02d}</span><strong>{e(v)}</strong></li>' for i,v in enumerate(p['fluxo']))}</ol><div class="two-column decisions"><h3>Decisões de engenharia, governança e eficiência</h3>{bullet(p['decisoes'])}</div></section>
<section id="resultados" class="case-section"><p class="eyebrow">03 / VALIDAÇÃO, TESTES E TRADE-OFFS</p><h2>Verificação da implementação</h2>{outcome}<p class="prose validation-copy">{e(p['validacao'])}</p><div class="two-column"><div><h3>Trade-offs e limites conhecidos</h3>{bullet(p['limites'])}</div><div><h3>Evoluções arquiteturais</h3>{bullet(p['proximos'])}</div></div>{evidence}</section>
<section id="material" class="case-section"><p class="eyebrow">04 / MATERIAL TÉCNICO</p><div class="section-heading"><h2>Contratos e especificação</h2><a class="button secondary" href="../documentacao/{p['slug']}.html">Ler especificação detalhada ↗</a></div><div class="code-panel"><div><h3>{e(p['exemplo']['titulo'])}</h3><span class="mono">{e(p['exemplo']['linguagem'])} / CONTRATO TÉCNICO</span></div><pre><code>{e(p['exemplo']['codigo'])}</code></pre></div><div class="material-links"><a href="{e(p.get('repo_url', ''))}" rel="noopener noreferrer">Repositório completo no GitHub ↗</a><a href="../documentacao/fontes/{p['slug']}.md" download>Especificação em Markdown ↓</a>{'<a href="../documentacao/prompts.html">Ver catálogo de prompts estruturados →</a>' if p['numero'] in ('03','04','05','06') else ''}</div></section>
<a class="next-project" href="{next_p['slug']}.html"><span class="mono">PRÓXIMO PROJETO / {next_p['numero']}</span><strong>{e(next_p['titulo'])}</strong><span aria-hidden="true">↗</span></a></article>'''
        write(f"projetos/{p['slug']}.html", layout(f"{p['titulo']} — {PROFILE['nome']}", p['resumo'], body, "../", "projeto", f"projetos/{p['slug']}.html"))


def inline(text):
    """Subconjunto de Markdown controlado; não aceita HTML do arquivo fonte."""
    parts = re.split(r'(`[^`]+`|\[[^\]]+\]\([^\s)]+\))', text)
    rendered = []
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            rendered.append('<code>' + e(part[1:-1]) + '</code>')
            continue
        link = re.fullmatch(r'\[([^\]]+)\]\(([^\s)]+)\)', part)
        if link:
            label, target = link.groups()
            if target.startswith(('https://', 'http://', '#')) or not re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                rendered.append(f'<a href="{e(target)}">{e(label)}</a>')
            else:
                rendered.append(e(label))
            continue
        safe = e(part)
        safe = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', safe)
        rendered.append(safe)
    return ''.join(rendered)


def markdown(source):
    lines = source.splitlines()
    result = []
    pos = 0
    while pos < len(lines):
        line = lines[pos]
        if not line.strip() or line.strip().startswith('<!--'):
            pos += 1
            continue
        if line.startswith('```'):
            language = line[3:].strip()
            code = []
            pos += 1
            while pos < len(lines) and not lines[pos].startswith('```'):
                code.append(lines[pos]); pos += 1
            result.append(f'<details class="source-design"><summary>Definição do diagrama (Mermaid)</summary><pre><code>{e(chr(10).join(code))}</code></pre></details>' if language == 'mermaid' else f'<pre><code>{e(chr(10).join(code))}</code></pre>')
            pos += 1
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            level = min(len(heading[1]) + 1, 6)
            result.append(f'<h{level}>{inline(heading[2])}</h{level}>'); pos += 1
            continue
        if line.startswith('|') and pos + 1 < len(lines) and re.match(r'^\|[\s:|\-]+\|\s*$', lines[pos+1]):
            cells = lambda x: [y.strip() for y in x.strip().strip('|').split('|')]
            headers = cells(line)
            pos += 2
            rows = []
            while pos < len(lines) and lines[pos].startswith('|'):
                rows.append(cells(lines[pos])); pos += 1
            result.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Tabela técnica"><table><thead><tr>' + ''.join(f'<th scope="col">{inline(x)}</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(x)}</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>')
            continue
        if re.match(r'^\s*[-*]\s+', line) or re.match(r'^\d+\.\s+', line):
            ordered = bool(re.match(r'^\d+\.\s+', line))
            pattern = r'^\d+\.\s+' if ordered else r'^\s*[-*]\s+'
            items = []
            while pos < len(lines) and re.match(pattern, lines[pos]):
                items.append(re.sub(pattern, '', lines[pos])); pos += 1
            tag = 'ol' if ordered else 'ul'
            result.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue
        paragraphs = [line]
        pos += 1
        while pos < len(lines) and lines[pos].strip() and not re.match(r'^(#|```|\||[-*] |\d+\. )', lines[pos]):
            paragraphs.append(lines[pos]); pos += 1
        result.append('<p>' + inline(' '.join(paragraphs)) + '</p>')
    return '\n'.join(result)


def build_docs():
    for p in PROJECTS:
        source_path = ROOT / 'documentacao/fontes' / (p['slug'] + '.md')
        source = source_path.read_text(encoding='utf-8')
        body = f'''<article class="wrap document"><a class="text-link" href="../projetos/{p['slug']}.html">← Voltar ao projeto</a><header><p class="eyebrow">DOCUMENTAÇÃO TÉCNICA / PROJETO {p['numero']}</p><h1>Especificação e arquitetura</h1><p class="case-summary">{e(p['subtitulo'])}</p><span class="status {p['grupo']}">{e(p['status'])}</span><p class="scope-note">Documento de arquitetura, contratos de dados, desenho experimental e critérios de aceite do projeto {e(p['titulo'])}.</p><a class="button secondary" href="fontes/{p['slug']}.md" download>Baixar Markdown ↓</a></header><div class="markdown">{markdown(source)}</div></article>'''
        write(f"documentacao/{p['slug']}.html", layout(f"Documentação: {p['titulo']} — {PROFILE['nome']}", f"Requisitos, arquitetura, stack e critérios técnicos: {p['titulo']}.", body, "../", "documento", f"documentacao/{p['slug']}.html"))
    prompt_source = (ROOT / 'documentacao/fontes/prompts.md').read_text(encoding='utf-8')
    body = '<article class="wrap document"><a class="text-link" href="../projetos/laboratorio-llms.html">← Voltar ao estudo de LLMs</a><header><p class="eyebrow">ENGENHARIA DE PROMPTS &amp; GUARDRAILS</p><h1>Prompts estruturados e contratos</h1><p class="case-summary">Contratos JSON Schema, defesa contra prompt injection, grounding para RAG, revisão de evidências de agentes e calibração de persona (Regra 80/15/5).</p></header><div class="markdown">' + markdown(prompt_source) + '</div></article>'
    write('documentacao/prompts.html', layout('Prompts estruturados e Contratos LLM — Beatriz Helena', 'Catálogo de prompts estruturados, contratos JSON, guardrails e avaliação sistemática.', body, '../', 'documento', 'documentacao/prompts.html'))


def build_cv():
    skills = ''.join(f'<li><strong>{e(x["titulo"])}:</strong> {e(x["descricao"])}</li>' for x in PROFILE['habilidades'])
    body = f'''<article class="wrap resume"><div class="resume-actions"><a href="index.html">← Voltar ao portfólio</a><button type="button" class="button primary" data-print hidden>Imprimir / salvar como PDF ↓</button></div><header class="resume-header"><p class="eyebrow">CURRÍCULO PROFISSIONAL</p><h1>{e(PROFILE['nome'])}</h1><p class="resume-title">{e(PROFILE['titulo'])}</p><div class="footer-links">{public_links()}</div></header><section><h2>Perfil</h2>{''.join(f'<p>{e(x)}</p>' for x in PROFILE['sobre'])}<p>{e(PROFILE['resumo'])}</p></section><section><h2>Habilidades e Domínio Técnico</h2><ul class="prose-list">{skills}</ul></section><section><h2>Experiência Profissional</h2>{trajectory()}</section><section><h2>Formação Acadêmica</h2><h3>{e(PROFILE['formacao']['curso'])}</h3><p>{e(PROFILE['formacao']['instituicao'])}</p></section><section><h2>Arquitetura e Projetos Técnicos</h2><p>Implementações práticas cobrindo arquitetura Medallion e ingestão incremental, gates de qualidade e observabilidade, RAG com busca híbrida e re-ranking, engenharia de prompts com Structured Outputs e Evals, orquestração de agentes com guardrails e tracing, automação idempotente e Machine Learning de séries temporais sem vazamento temporal.</p><p><a href="index.html#projetos">Ver os oito projetos técnicos e suas arquiteturas →</a></p></section></article>'''
    write('curriculo.html', layout(f'Currículo — {PROFILE["nome"]}', f'Currículo de {PROFILE["nome"]}, {PROFILE["titulo"]}.', body, page='curriculo', canonical_path='curriculo.html'))


if __name__ == '__main__':
    assert len(PROJECTS) == 8 and len({p['slug'] for p in PROJECTS}) == 8
    build_home()
    build_projects()
    build_docs()
    build_cv()
    write('404.html', layout('Página não encontrada — Beatriz Helena', 'Volte ao início do portfólio.', '<section class="wrap document"><p class="eyebrow">404</p><h1>Página não encontrada</h1><p>Esta página não foi encontrada.</p><a class="button primary" href="index.html">Abrir o portfólio →</a></section>', page='404'))
    print('Site gerado: início, currículo, 8 estudos, 8 planejamentos, prompts e 404.')
