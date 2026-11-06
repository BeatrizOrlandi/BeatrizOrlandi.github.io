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
    nav = ''.join(f'<a href="{home}#{anchor}">{label}</a>' for anchor, label in [("impacto", "Impacto & IA"), ("projetos", "Projetos"), ("sobre", "Sobre"), ("trajetoria", "Trajetória")])
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
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=bia4">
  <script src="{prefix}assets/site.js?v=bia4" defer></script>
</head>
<body data-page="{e(page)}">
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <header class="site-header wrap">
    <a class="brand" href="{home}" aria-label="{e(PROFILE['nome'])} — início"><span class="monogram" aria-hidden="true">bh.</span><span>{e(PROFILE['nome'])}<small>Engenharia de IA</small></span></a>
    <nav aria-label="Navegação principal">{nav}<a href="{prefix}documentacao/prompts.html">Prompts ↗</a><a class="nav-cv" href="{prefix}curriculo.html">Currículo <span aria-hidden="true">↗</span></a></nav>
  </header>
  <main id="conteudo">{body}</main>
  <footer class="site-footer wrap"><div><a class="footer-name" href="{home}">{e(PROFILE['nome'])}<span>Engenheira de IA</span></a><p>Portfólio de Engenharia de IA · Python, Databricks, LLMs, RAG, Agentes e MLflow.</p></div><div class="footer-links">{public_links()}<a href="{prefix}documentacao/prompts.html">Catálogo de Prompts ↗</a><a href="{prefix}curriculo.html">Ver currículo ↗</a><a href="{home}#projetos">Explorar projetos ↑</a></div><p class="fineprint">© {date.fromisoformat(PROFILE['atualizacao_site']).year} {e(PROFILE['nome'])}. Projetos executados e validados no Databricks com código aberto no GitHub.<br>Site atualizado em 06/11/2026 · 8 de 8 projetos implementados e auditados.</p></footer>
  <button type="button" class="chat-fab" data-chat-toggle aria-expanded="false" aria-controls="chat-assistant">
    <span class="chat-fab-dot" aria-hidden="true"></span>
    <span>Falar com a BIA (IA) ✨</span>
  </button>
  <aside id="chat-assistant" class="chat-drawer" data-chat-drawer hidden aria-label="BIA — Agente de IA da Beatriz Helena">
    <div class="chat-header">
      <div class="chat-header-info">
        <strong>BIA · Agente de IA da Beatriz 🤖✨</strong>
        <small>Databricks Model Serving · LLM Conversacional</small>
      </div>
      <button type="button" class="chat-close" data-chat-close aria-label="Fechar chat">Fechar ✕</button>
    </div>
    <div class="chat-messages" data-chat-messages aria-live="polite">
      <div class="chat-bubble assistant">
        <p>Olá, viajante! 🖖 Eu sou a <strong>BIA</strong> (<em>Beatriz Intelligence Assistant</em>), a IA oficial do portfólio da Beatriz Helena — tipo o J.A.R.V.I.S. dela, só que movida a café, Python e Databricks!</p>
        <p>Pode mandar qualquer pergunta aberta: qual é o projeto mais legal, detalhes de arquitetura, referências geeks ou pegar o <strong>WhatsApp</strong> e <strong>e-mail</strong> dela!</p>
      </div>
    </div>
    <div class="chat-chips" aria-label="Perguntas sugeridas">
      <button type="button" class="chat-chip" data-chat-prompt="Qual é o projeto mais legal da Beatriz?">Qual o mais legal? 🚀</button>
      <button type="button" class="chat-chip" data-chat-prompt="Você tem o WhatsApp e contato da Beatriz?">WhatsApp &amp; Contato 📱</button>
      <button type="button" class="chat-chip" data-chat-prompt="Por que devo contratar a Beatriz para o meu time de IA?">Por que contratar? 💡</button>
      <button type="button" class="chat-chip" data-chat-prompt="Me explica como funciona o RAG e Vector Search dela?">Arquitetura RAG 🧠</button>
    </div>
    <form class="chat-form" data-chat-form>
      <label class="sr-only" for="chat-input-field">Pergunte qualquer coisa para a BIA</label>
      <input id="chat-input-field" data-chat-input type="text" placeholder="Pergunte qualquer coisa para a BIA..." autocomplete="off">
      <button type="submit">Enviar</button>
    </form>
  </aside>
</body>
</html>
'''


def metrics(items):
    return '<dl class="metrics">' + ''.join(f'<div><dt>{e(x["valor"])}</dt><dd>{e(x["rotulo"])}</dd></div>' for x in items) + '</dl>'


def project_card(p):
    img_html = f'<a class="card-media" href="projetos/{p["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="{e(p["imagem"])}" alt="" loading="lazy" width="800" height="380"></a>' if p.get("imagem") else ""
    res_strip = ""
    if p.get("resultados"):
        res_strip = '<div class="card-kpis">' + ''.join(f'<span><strong>{e(r["valor"])}</strong> <small>{e(r["rotulo"])}</small></span>' for r in p["resultados"][:2]) + '</div>'
    return f'''<article class="project-card {'featured' if p['numero'] == '01' else ''}" data-project data-group="{e(p['grupo'])}" data-search="{e(' '.join([p['titulo'], p['subtitulo'], p['categoria'], *p['stack']]))}">
  {img_html}
  <div class="card-meta"><span class="mono">{p['numero']} / {e(p['categoria'])}</span><span class="status {p['grupo']}">{e(p['status'])}</span></div>
  <h3><a href="projetos/{p['slug']}.html">{e(p['titulo'])}<span aria-hidden="true">↗</span></a></h3><p>{e(p['resumo'])}</p>
  {res_strip}
  {tags(p['stack'][:4])}<a class="text-link" href="projetos/{p['slug']}.html" aria-label="Ver estudo: {e(p['subtitulo'])}">Ver arquitetura, código e métricas <span aria-hidden="true">→</span></a>
</article>'''


def trajectory():
    return '<ol class="timeline">' + ''.join(f'''<li><div class="timeline-date mono">{e(x['periodo'])}</div><div class="timeline-body"><h3>{e(x['empresa'])}</h3><p class="role">{e(x['cargo'])}</p>{f'<p>{e(x["descricao"])}</p>' if x['descricao'] else ''}</div></li>''' for x in PROFILE['experiencias']) + '</ol>'


def build_home():
    skills = ''.join(f'''<article class="skill"><span class="mono">0{i + 1}</span><h3>{e(x['titulo'])}</h3><p>{e(x['descricao'])}</p>{tags(x['tecnologias'])}</article>''' for i, x in enumerate(PROFILE['habilidades']))
    impl_count = sum(1 for p in PROJECTS if p['grupo'] == 'implementado')
    plan_count = sum(1 for p in PROJECTS if p['grupo'] == 'planejado')
    body = f'''
<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy"><p class="eyebrow"><span class="tiny-square" aria-hidden="true"></span> PYTHON / DATABRICKS / LLMS / AGENTES EM PRODUÇÃO</p><h1 id="hero-title">Beatriz<br>Helena</h1><p class="hero-role">Engenheira de IA · Efí Bank</p><p class="hero-intro">Construo sistemas de IA generativa, pipelines Lakehouse, automações que economizam horas reais, prompts estruturados avaliados com MLflow e agentes em produção no Databricks Model Serving.</p><div class="actions"><a class="button primary" href="#projetos">Explorar 8 projetos <span aria-hidden="true">↘</span></a><button type="button" class="button secondary" data-open-chat>Conversar com a BIA (minha IA) ✨</button><a class="text-link" href="documentacao/prompts.html">Ver engenharia de prompts →</a></div></div>
  <div class="system-panel"><div class="panel-label mono"><span class="notebook-name">● ● ● &nbsp; bia_agent_serving.py</span><span>PROD / MODEL SERVING</span></div><p class="panel-heading">Ecossistema<br><span>Aurora &amp; BIA</span></p><p class="panel-caption mono">8 PROJETOS EXECUTADOS NO DATABRICKS · UNITY CATALOG</p><ol class="system-flow"><li><span>01</span><div><strong>Prompts &amp; LLMs (100% JSON)</strong><small>60 gerações no MLflow · Qwen3 80B (528 ms) &amp; Llama 3.3 70B</small></div><b aria-hidden="true">↓</b></li><li><span>02</span><div><strong>Automações (18h/mês → 42s)</strong><small>Pipeline Medallion, Gate 24/24 e Boletins Idempotentes</small></div><b aria-hidden="true">↓</b></li><li><span>03</span><div><strong>Agente BIA + RAG (93,3% Top-1)</strong><small>Model Serving ativo, MLflow Tracing e Vector Search</small></div></li></ol><a href="projetos/agentes-investigacao.html">Ver arquitetura do Agente BIA e Orquestração <span aria-hidden="true">↗</span></a></div>
</section>
<div class="expertise-strip"><div class="wrap"><span>Python &amp; PySpark</span><span>Databricks &amp; Unity Catalog</span><span>LLMs &amp; Prompt Engineering</span><span>Vector Search &amp; RAG</span><span>LangGraph &amp; Model Serving</span><span>MLflow 3 Tracing</span></div></div>

<section id="impacto" class="section wrap pillars-section" aria-labelledby="pillars-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">00 / ENGENHARIA DE IA ORIENTADA A RESULTADOS</p>
      <h2 id="pillars-title">Quatro pilares em produção</h2>
    </div>
    <p>Evidências práticas de experimentação rigorosa com LLMs, automação de processos, ferramentas deployadas e impacto mensurável.</p>
  </div>
  <div class="pillars-grid">
    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">PILAR 01 / LLMS &amp; PROMPTS</span><span class="pillar-badge">100% JSON Estrito</span></div>
      <h3>Prompts bem estruturados e experimentação com LLMs</h3>
      <p>Bancada experimental executada no Databricks comparando prompts diretos contra contratos JSON estritos com validação <code>Pydantic</code> e defesa contra <em>prompt injection</em> em múltiplos Foundation Models (<strong>Meta Llama 3.3 70B</strong> e <strong>Qwen3 Next 80B Instruct</strong>).</p>
      <ul class="pillar-metrics">
        <li><strong>0% → 100%</strong> de conformidade estrita ao schema JSON após estruturação contratual do prompt.</li>
        <li><strong>528 ms vs. 1.588 ms</strong> de latência mediana (p50) medida em 60 execuções rastreadas no MLflow.</li>
      </ul>
      <div class="pillar-links">
        <a href="documentacao/prompts.html">Catálogo de Prompts &amp; Contratos ↗</a>
        <a href="projetos/laboratorio-llms.html">Estudo 04: Laboratório LLMs →</a>
      </div>
    </article>

    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">PILAR 02 / AUTOMAÇÃO REAL</span><span class="pillar-badge">18h/mês → 42s</span></div>
      <h3>Automações que economizaram horas reais em processos</h3>
      <p>Substituição de fluxos manuais de extração, consolidação de planilhas e conferência numérica por pipelines idempotentes acoplados ao Gate de Qualidade na camada Gold — além de automações corporativas em produção na <strong>Efí Bank</strong> integrando Python, Snowflake, WhatsApp, Slack e Salesforce.</p>
      <ul class="pillar-metrics">
        <li><strong>~18 horas/mês economizadas</strong> na geração e auditoria mensal de relatórios multiunidade (reduzido para <strong>42 segundos</strong> por execução).</li>
        <li><strong>Zero retrabalho ou duplicação</strong> garantido por chave de idempotência SHA e conferência numérica automática.</li>
      </ul>
      <div class="pillar-links">
        <a href="projetos/boletins-verificaveis.html">Estudo 06: Automação de Boletins ↗</a>
        <a href="projetos/pipeline-dados-aurora.html">Estudo 01: Pipeline Medallion →</a>
      </div>
    </article>

    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">PILAR 03 / FERRAMENTAS DEPLOYADAS</span><span class="pillar-badge">Model Serving + App + AI/BI</span></div>
      <h3>Ferramentas internas deployadas, dashboards e agentes</h3>
      <p>Soluções vivas e operacionais construídas sobre o Databricks: a <strong>BIA</strong> (<code>MLflow ResponsesAgent</code> servida no endpoint <code>beatriz-portfolio-agent</code> com <code>@mlflow.trace</code>), aplicação web em <strong>Databricks Apps (FastAPI)</strong>, <strong>Painel Executivo AI/BI Lakeview</strong> e máquina de estados de investigação.</p>
      <ul class="pillar-metrics">
        <li><strong>Agente BIA em produção</strong> respondendo em tempo real neste portfólio com telemetria de spans no MLflow.</li>
        <li><strong>16/16 cenários aprovados</strong> na máquina de estados operacional (bloqueio de escopo, SQL injection e timeout).</li>
      </ul>
      <div class="pillar-links">
        <a href="projetos/agentes-investigacao.html">Estudo 05: Agentes &amp; Model Serving ↗</a>
        <a href="https://github.com/BeatrizOrlandi/aurora-05-agentes-investigacao/tree/main/dashboards" rel="noopener noreferrer">Artefato Dashboard AI/BI (JSON) →</a>
      </div>
    </article>

    <article class="pillar-card">
      <div class="pillar-top"><span class="mono">PILAR 04 / IMPACTO MENSURÁVEL</span><span class="pillar-badge">8/8 Projetos Validados</span></div>
      <h3>Soluções em produção com resultados mensuráveis</h3>
      <p>Arquiteturas desenhadas para uso real com SLAs, prevenção de vazamento entre unidades, controle de qualidade que preserva a última versão íntegra e benchmarks reprodutíveis com tabelas Delta e evidências públicas.</p>
      <ul class="pillar-metrics">
        <li><strong>93,3% Top-1 Accuracy (14/15)</strong> na recuperação vetorial/híbrida com Databricks Vector Search e filtros de vigência.</li>
        <li><strong>MAE 10,58</strong> em previsão horária causal (vs. 48,81 do baseline) e <strong>92,3% F1</strong> no avaliador semântico BEM com <strong>0 falsos positivos críticos</strong>.</li>
      </ul>
      <div class="pillar-links">
        <a href="projetos/rag-regulamentos.html">Estudo 03: Vector Search RAG ↗</a>
        <a href="projetos/pipeline-ml-demanda.html">Estudo 07: Previsão ML Causal →</a>
      </div>
    </article>
  </div>
</section>

<section id="projetos" class="section wrap" aria-labelledby="projects-title"><div class="section-heading"><div><p class="eyebrow">01 / ARQUITETURAS, CÓDIGO E EVIDÊNCIAS</p><h2 id="projects-title">Projetos executados</h2></div><p>Oito projetos completos implementados e validados no Databricks, com diagramas de arquitetura, repositórios públicos no GitHub e métricas auditáveis.</p></div><p class="scope-note">O ecossistema Observatório Aurora conecta seis sistemas integrados (Engenharia de Dados, Qualidade, Vector Search RAG, LLMs, Agentes no Model Serving e Automação). Os estudos 07 e 08 expandem o portfólio com Machine Learning de séries temporais e avaliação semântica com modelos pré-treinados.</p>
<div class="project-toolbar" hidden data-project-controls><div class="filters" role="group" aria-label="Filtrar projetos por implementação"><button type="button" class="active" data-filter="todos" aria-pressed="true">Todos <span>{len(PROJECTS):02d}</span></button><button type="button" data-filter="implementado" aria-pressed="false">Implementados no Databricks <span>{impl_count:02d}</span></button>{f'<button type="button" data-filter="planejado" aria-pressed="false">Planejados <span>{plan_count:02d}</span></button>' if plan_count else ''}</div><label class="search"><span class="sr-only">Buscar projeto ou tecnologia</span><input data-search-input type="search" placeholder="Buscar projeto ou tecnologia" autocomplete="off"></label></div><p class="filter-count mono" data-filter-count aria-live="polite" hidden>{len(PROJECTS)} projetos</p>
<div class="project-grid">{''.join(project_card(p) for p in PROJECTS)}</div><p data-empty hidden class="empty-state">Nenhum projeto corresponde à busca. Tente outra tecnologia ou selecione Todos.</p><noscript><p>Todos os projetos estão disponíveis acima. Os filtros funcionam com JavaScript habilitado.</p></noscript>
<p class="method-note"><strong>Rigor experimental e transparência:</strong> cada projeto inclui código-fonte completo no GitHub, arquivo JSON de evidências públicas, tabelas no Unity Catalog, experimentos no MLflow e documentação explícita dos limites conhecidos.</p></section>
<section class="evidence-section"><div class="wrap evidence-layout"><div><p class="eyebrow">DATABRICKS / MÉTRICAS CONSOLIDADAS EM PRODUÇÃO</p><h2>Resultados<br>verificáveis</h2><p>Todos os oito projetos possuem execução real registrada em tabelas Delta e experimentos MLflow, cobrindo qualidade de dados, RAG, LLMs, agentes, automação e Machine Learning.</p><a class="text-link" href="documentacao/prompts.html">Inspecionar contratos de prompts e ablação LLM →</a></div>{metrics([{'valor':'100%','rotulo':'JSON válido em prompts estruturados (60 runs MLflow)'}, {'valor':'18h → 42s','rotulo':'economia mensal na automação de boletins'}, {'valor':'16/16','rotulo':'rotas e guardrails aprovados no agente'}])}</div></section>
<section id="sobre" class="section wrap" aria-labelledby="about-title"><div class="about-layout"><div><p class="eyebrow">02 / SOBRE MIM</p><h2 id="about-title">Sobre mim</h2></div><div class="about-copy">{''.join(f'<p>{e(x)}</p>' for x in PROFILE['sobre'])}</div></div><div class="skills-grid">{skills}</div></section>
<section id="trajetoria" class="section wrap trajectory-section" aria-labelledby="career-title"><div class="section-heading"><div><p class="eyebrow">03 / TRAJETÓRIA</p><h2 id="career-title">Experiência<br>e formação</h2></div><a class="button secondary" href="curriculo.html">Currículo para impressão ↗</a></div><div class="career-layout">{trajectory()}<aside class="education"><p class="eyebrow">FORMAÇÃO</p><div class="education-mark" aria-hidden="true">↗</div><h3>{e(PROFILE['formacao']['curso'])}</h3><p>{e(PROFILE['formacao']['instituicao'])}</p><span class="mono">COMPUTAÇÃO / DADOS / IA</span></aside></div></section>
'''
    write("index.html", layout(f"{PROFILE['nome']} — Engenharia de IA", "Portfólio de Beatriz Helena: IA generativa, prompts estruturados, RAG, agentes no Databricks Model Serving, automações e MLflow.", body))


def build_projects():
    for index, p in enumerate(PROJECTS):
        next_p = PROJECTS[(index + 1) % len(PROJECTS)]
        outcome = metrics(p['resultados']) if p['resultados'] else '<p class="plan-callout"><strong>Design e requisitos disponíveis.</strong> Esta trilha ainda não tem resultados de execução. O planejamento detalha os critérios de aceite futuros.</p>'
        evidence = f'<a class="text-link" href="../evidencias/{p["evidencia"]}" download>Baixar evidência resumida (JSON) ↓</a>' if p['evidencia'] else ''
        diagram = f'<figure class="case-diagram"><img src="../{e(p["imagem"])}" alt="Diagrama técnico de arquitetura e resultados: {e(p["titulo"])}" width="800" height="380"><figcaption class="mono">FIGURA {p["numero"]} · ARQUITETURA EXECUTADA E MÉTRICAS AUDITADAS NO DATABRICKS</figcaption></figure>' if p.get("imagem") else ''
        body = f'''<div class="wrap case-breadcrumb"><a href="../index.html#projetos">← Todos os projetos</a><span class="mono">ESTUDO {p['numero']} / 08</span></div><article class="case wrap"><header class="case-hero"><div><p class="eyebrow">{e(p['categoria'])}</p><h1>{e(p['titulo'])}</h1><p class="case-summary">{e(p['resumo'])}</p>{tags(p['stack'])}</div><aside class="case-meta"><span class="status {p['grupo']}">{e(p['status'])}</span><dl><dt>PROJETO</dt><dd>{e(p['subtitulo'])}</dd><dt>CONTEXTO</dt><dd>{'Ecossistema autoral Aurora · Databricks' if p['numero'] < '07' else 'Benchmark autoral reproduzível · Databricks'}</dd><dt>EVIDÊNCIAS</dt><dd>{'Execução validada no Databricks + MLflow' if p['grupo'] == 'implementado' else 'Planejamento e critérios de aceite'}</dd><dt>REPOSITÓRIO</dt><dd><a href="{e(p.get('repo_url', ''))}" rel="noopener noreferrer">Ver código no GitHub ↗</a></dd></dl></aside></header>
{diagram}
<nav class="case-nav" aria-label="Conteúdo deste estudo"><a href="#problema">Problema</a><a href="#arquitetura">Arquitetura</a><a href="#resultados">Resultados e limites</a><a href="#material">Material técnico</a></nav>
<section id="problema" class="case-section two-column"><div><p class="eyebrow">01 / O PROBLEMA</p><h2>Problema</h2></div><div class="prose"><p>{e(p['problema'])}</p><h3>Escopo entregue em produção</h3><p>{e(p['entrega'])}</p></div></section>
<section id="arquitetura" class="case-section"><p class="eyebrow">02 / ARQUITETURA</p><h2>Fluxo do projeto</h2><ol class="architecture" aria-label="Etapas da arquitetura">{''.join(f'<li><span class="mono">{i+1:02d}</span><strong>{e(v)}</strong></li>' for i,v in enumerate(p['fluxo']))}</ol><div class="two-column decisions"><h3>Decisões técnicas</h3>{bullet(p['decisoes'])}</div></section>
<section id="resultados" class="case-section"><p class="eyebrow">03 / RESULTADOS E LIMITES</p><h2>{'O que foi medido' if p['resultados'] else 'Como será avaliado'}</h2>{outcome}<p class="prose validation-copy">{e(p['validacao'])}</p><div class="two-column"><div><h3>Limites conhecidos</h3>{bullet(p['limites'])}</div><div><h3>Próximo incremento</h3>{bullet(p['proximos'])}</div></div>{evidence}</section>
<section id="material" class="case-section"><p class="eyebrow">04 / MATERIAL TÉCNICO</p><div class="section-heading"><h2>Especificação e contratos</h2><a class="button secondary" href="../documentacao/{p['slug']}.html">Ler documentação completa ↗</a></div><div class="code-panel"><div><h3>{e(p['exemplo']['titulo'])}</h3><span class="mono">{e(p['exemplo']['linguagem'])} / {'CONTRATO IMPLEMENTADO' if p['grupo'] == 'implementado' else 'PROPOSTA NÃO EXECUTADA'}</span></div><pre><code>{e(p['exemplo']['codigo'])}</code></pre></div><div class="material-links"><a href="{e(p.get('repo_url', ''))}" rel="noopener noreferrer">Repositório do projeto no GitHub ↗</a><a href="../documentacao/fontes/{p['slug']}.md" download>Especificação em Markdown ↓</a>{'<a href="../documentacao/prompts.html">Ver catálogo de prompts estruturados →</a>' if p['numero'] in ('03','04','05','06') else ''}</div></section>
<a class="next-project" href="{next_p['slug']}.html"><span class="mono">PRÓXIMO ESTUDO / {next_p['numero']}</span><strong>{e(next_p['titulo'])}</strong><span aria-hidden="true">↗</span></a></article>'''
        write(f"projetos/{p['slug']}.html", layout(f"{p['subtitulo']} — {PROFILE['nome']}", p['resumo'], body, "../", "projeto", f"projetos/{p['slug']}.html"))


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
        body = f'''<article class="wrap document"><a class="text-link" href="../projetos/{p['slug']}.html">← Voltar ao estudo</a><header><p class="eyebrow">DOCUMENTAÇÃO TÉCNICA / ESTUDO {p['numero']}</p><h1>Especificação e arquitetura</h1><p class="case-summary">{e(p['subtitulo'])}</p><span class="status {p['grupo']}">{e(p['status'])}</span><p class="scope-note">Documento de arquitetura, contratos de dados, desenho experimental no MLflow e critérios de aceite verificados para o projeto {e(p['subtitulo'])}.</p><a class="button secondary" href="fontes/{p['slug']}.md" download>Baixar Markdown ↓</a></header><div class="markdown">{markdown(source)}</div></article>'''
        write(f"documentacao/{p['slug']}.html", layout(f"Documentação: {p['subtitulo']} — {PROFILE['nome']}", f"Requisitos, arquitetura, stack, MLflow e critérios de aceite: {p['subtitulo']}.", body, "../", "documento", f"documentacao/{p['slug']}.html"))
    prompt_source = (ROOT / 'documentacao/fontes/prompts.md').read_text(encoding='utf-8')
    body = '<article class="wrap document"><a class="text-link" href="../projetos/laboratorio-llms.html">← Voltar ao Laboratório de LLMs</a><header><p class="eyebrow">ENGENHARIA DE PROMPTS &amp; EXPERIMENTAÇÃO MLFLOW</p><h1>Prompts estruturados em produção</h1><p class="case-summary">Contratos JSON estritos, ablação entre Foundation Models (Llama 3.3 70B vs. Qwen3 80B), defesa contra prompt injection e system prompt do Agente BIA.</p><span class="status implementado">Validado no MLflow · 60 execuções</span></header><div class="markdown">' + markdown(prompt_source) + '</div></article>'
    write('documentacao/prompts.html', layout('Prompts estruturados e Experimentação LLM — Beatriz Helena', 'Catálogo de prompts estruturados, contratos JSON, guardrails e resultados medidos no MLflow.', body, '../', 'documento', 'documentacao/prompts.html'))


def build_cv():
    skills = ''.join(f'<li><strong>{e(x["titulo"])}:</strong> {e(x["descricao"])}</li>' for x in PROFILE['habilidades'])
    body = f'''<article class="wrap resume"><div class="resume-actions"><a href="index.html">← Voltar ao portfólio</a><button type="button" class="button primary" data-print hidden>Imprimir / salvar como PDF ↓</button></div><header class="resume-header"><p class="eyebrow">CURRÍCULO PROFISSIONAL</p><h1>{e(PROFILE['nome'])}</h1><p class="resume-title">{e(PROFILE['titulo'])}</p><div class="footer-links">{public_links()}</div></header><section><h2>Perfil</h2>{''.join(f'<p>{e(x)}</p>' for x in PROFILE['sobre'])}<p>{e(PROFILE['resumo'])}</p></section><section><h2>Habilidades</h2><ul class="prose-list">{skills}</ul></section><section><h2>Experiência</h2>{trajectory()}</section><section><h2>Formação</h2><h3>{e(PROFILE['formacao']['curso'])}</h3><p>{e(PROFILE['formacao']['instituicao'])}</p></section><section><h2>Projetos em produção e estudos validados</h2><p>Ecossistema Aurora &amp; BIA no Databricks: 8 projetos implementados cobrindo pipeline Medallion (5.000 eventos), gate de qualidade (24/24 asserções), RAG com Vector Search (93,3% top-1), ablação de prompts LLM (100% JSON válido), Agente BIA no Model Serving com MLflow Tracing, automação de boletins (18h/mês → 42s), previsão horária ML (MAE 10,58) e avaliador semântico BEM (92,3% F1).</p><p><a href="index.html#projetos">Ver os oito estudos de caso, arquiteturas e repositórios →</a></p></section></article>'''
    write('curriculo.html', layout(f'Currículo — {PROFILE["nome"]}', f'Currículo de {PROFILE["nome"]}, {PROFILE["titulo"]}.', body, page='curriculo', canonical_path='curriculo.html'))


if __name__ == '__main__':
    assert len(PROJECTS) == 8 and len({p['slug'] for p in PROJECTS}) == 8
    build_home()
    build_projects()
    build_docs()
    build_cv()
    write('404.html', layout('Página não encontrada — Beatriz Helena', 'Volte ao início do portfólio.', '<section class="wrap document"><p class="eyebrow">404</p><h1>Página não encontrada</h1><p>Esta página não foi encontrada.</p><a class="button primary" href="index.html">Abrir o portfólio →</a></section>', page='404'))
    print('Site gerado: início, currículo, 8 estudos, 8 planejamentos, prompts e 404.')
