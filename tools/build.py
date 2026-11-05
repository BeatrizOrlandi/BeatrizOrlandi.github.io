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
    for key, label in [("github", "GitHub"), ("linkedin", "LinkedIn"), ("email", "E-mail")]:
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
    nav = ''.join(f'<a href="{home}#{anchor}">{label}</a>' for anchor, label in [("projetos", "Projetos"), ("sobre", "Sobre"), ("trajetoria", "Trajetória")])
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
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body data-page="{e(page)}">
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <header class="site-header wrap">
    <a class="brand" href="{home}" aria-label="{e(PROFILE['nome'])} — início"><span class="monogram" aria-hidden="true">bh.</span><span>{e(PROFILE['nome'])}<small>Engenharia de IA</small></span></a>
    <nav aria-label="Navegação principal">{nav}<a class="nav-cv" href="{prefix}curriculo.html">Currículo <span aria-hidden="true">↗</span></a></nav>
  </header>
  <main id="conteudo">{body}</main>
  <footer class="site-footer wrap"><div><a class="footer-name" href="{home}">{e(PROFILE['nome'])}<span>Engenheira de IA</span></a><p>Portfólio de estudos · Python, Databricks e IA.</p></div><div class="footer-links">{public_links()}<a href="{prefix}curriculo.html">Ver currículo ↗</a><a href="{home}#projetos">Explorar projetos ↑</a></div><p class="fineprint">© {date.fromisoformat(PROFILE['atualizacao_site']).year} {e(PROFILE['nome'])}. Estudos autorais com dados sintéticos ou fontes públicas planejadas.<br>Site atualizado em 05/11/2026 · evidências de execução de 28/10/2026.</p></footer>
</body>
</html>
'''


def metrics(items):
    return '<dl class="metrics">' + ''.join(f'<div><dt>{e(x["valor"])}</dt><dd>{e(x["rotulo"])}</dd></div>' for x in items) + '</dl>'


def project_card(p):
    return f'''<article class="project-card {'featured' if p['numero'] == '01' else ''}" data-project data-group="{e(p['grupo'])}" data-search="{e(' '.join([p['titulo'], p['subtitulo'], p['categoria'], *p['stack']]))}">
  <div class="card-meta"><span class="mono">{p['numero']} / {e(p['categoria'])}</span><span class="status {p['grupo']}">{e(p['status'])}</span></div>
  <h3><a href="projetos/{p['slug']}.html">{e(p['titulo'])}<span aria-hidden="true">↗</span></a></h3><p>{e(p['resumo'])}</p>
  {tags(p['stack'][:4])}<a class="text-link" href="projetos/{p['slug']}.html" aria-label="Ver estudo: {e(p['subtitulo'])}">Ler o estudo <span aria-hidden="true">→</span></a>
</article>'''


def trajectory():
    return '<ol class="timeline">' + ''.join(f'''<li><div class="timeline-date mono">{e(x['periodo'])}</div><div class="timeline-body"><h3>{e(x['empresa'])}</h3><p class="role">{e(x['cargo'])}</p>{f'<p>{e(x["descricao"])}</p>' if x['descricao'] else ''}</div></li>''' for x in PROFILE['experiencias']) + '</ol>'


def build_home():
    skills = ''.join(f'''<article class="skill"><span class="mono">0{i + 1}</span><h3>{e(x['titulo'])}</h3><p>{e(x['descricao'])}</p>{tags(x['tecnologias'])}</article>''' for i, x in enumerate(PROFILE['habilidades']))
    body = f'''
<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy"><p class="eyebrow"><span class="tiny-square" aria-hidden="true"></span> PYTHON / DADOS / IA</p><h1 id="hero-title">Beatriz<br>Helena</h1><p class="hero-role">Engenheira de IA</p><p class="hero-intro">Trabalho com Python, Databricks, LLMs, RAG e agentes. Aqui estão meus projetos de estudo, com código, arquitetura, testes e o que ainda falta implementar.</p><div class="actions"><a class="button primary" href="#projetos">Ver projetos <span aria-hidden="true">↘</span></a><a class="text-link" href="curriculo.html">Ver currículo →</a></div></div>
  <div class="system-panel"><div class="panel-label mono"><span class="notebook-name">● ● ● &nbsp; aurora.ipynb</span><span>LAB / 01</span></div><p class="panel-heading">Pipeline<br>de bibliotecas</p><p class="panel-caption mono">DADOS SINTÉTICOS / SETEMBRO 2026</p><ol class="system-flow"><li><span>01</span><div><strong>5.000 eventos</strong><small>Empréstimos, devoluções e renovações</small></div><b aria-hidden="true">↓</b></li><li><span>02</span><div><strong>Bronze → Silver → Gold</strong><small>Validação, deduplicação e agregações</small></div><b aria-hidden="true">↓</b></li><li><span>03</span><div><strong>8 checks + 3 boletins</strong><small>Publicação condicionada à qualidade</small></div></li></ol><a href="projetos/pipeline-dados-aurora.html">Abrir projeto do pipeline <span aria-hidden="true">↗</span></a></div>
</section>
<div class="expertise-strip"><div class="wrap"><span>Python</span><span>Databricks</span><span>LLMs & RAG</span><span>LangChain / LangGraph</span><span>MLflow</span><span>APIs</span></div></div>
<section id="projetos" class="section wrap" aria-labelledby="projects-title"><div class="section-heading"><div><p class="eyebrow">01 / PROJETOS SELECIONADOS</p><h2 id="projects-title">Projetos</h2></div><p>Oito estudos com requisitos, arquitetura e planejamento técnico. Os projetos executados incluem resultados e limitações.</p></div><p class="scope-note">O Observatório Aurora conecta seis estudos em um cenário fictício de bibliotecas. As trilhas de ML e modelo pré-treinado exploram fontes públicas em projetos independentes.</p>
<div class="project-toolbar" hidden data-project-controls><div class="filters" role="group" aria-label="Filtrar projetos por implementação"><button type="button" class="active" data-filter="todos" aria-pressed="true">Todos <span>08</span></button><button type="button" data-filter="implementado" aria-pressed="false">Com implementação <span>04</span></button><button type="button" data-filter="planejado" aria-pressed="false">Planejados <span>04</span></button></div><label class="search"><span class="sr-only">Buscar projeto ou tecnologia</span><input data-search-input type="search" placeholder="Buscar projeto ou tecnologia" autocomplete="off"></label></div><p class="filter-count mono" data-filter-count aria-live="polite" hidden>8 projetos</p>
<div class="project-grid">{''.join(project_card(p) for p in PROJECTS)}</div><p data-empty hidden class="empty-state">Nenhum projeto corresponde à busca. Tente outra tecnologia ou selecione Todos.</p><noscript><p>Todos os projetos estão disponíveis acima. Os filtros funcionam com JavaScript habilitado.</p></noscript>
<p class="method-note"><strong>Sobre os resultados:</strong> métricas e estados refletem as execuções de 28/10/2026 no laboratório. “Planejado” identifica design e requisitos; “recuperação validada” não implica geração por LLM.</p></section>
<section class="evidence-section"><div class="wrap evidence-layout"><div><p class="eyebrow">DATABRICKS / EXECUÇÕES DE 28.10.2026</p><h2>Resultados<br>do laboratório</h2><p>Resumo das execuções com dados sintéticos. Cada estudo apresenta o conjunto avaliado, os testes realizados e os erros encontrados.</p><a class="text-link" href="projetos/rag-regulamentos.html">Ver avaliação e caso de falha →</a></div>{metrics([{'valor':'5.000','rotulo':'eventos sintéticos no pipeline'}, {'valor':'24/24','rotulo':'asserções de integração aprovadas'}, {'valor':'14/15','rotulo':'perguntas com documento esperado no top-1 vetorial'}])}</div></section>
<section id="sobre" class="section wrap" aria-labelledby="about-title"><div class="about-layout"><div><p class="eyebrow">02 / SOBRE MIM</p><h2 id="about-title">Sobre mim</h2></div><div class="about-copy">{''.join(f'<p>{e(x)}</p>' for x in PROFILE['sobre'])}</div></div><div class="skills-grid">{skills}</div></section>
<section id="trajetoria" class="section wrap trajectory-section" aria-labelledby="career-title"><div class="section-heading"><div><p class="eyebrow">03 / TRAJETÓRIA</p><h2 id="career-title">Experiência<br>e formação</h2></div><a class="button secondary" href="curriculo.html">Currículo para impressão ↗</a></div><div class="career-layout">{trajectory()}<aside class="education"><p class="eyebrow">FORMAÇÃO</p><div class="education-mark" aria-hidden="true">↗</div><h3>{e(PROFILE['formacao']['curso'])}</h3><p>{e(PROFILE['formacao']['instituicao'])}</p><span class="mono">COMPUTAÇÃO / DADOS / IA</span></aside></div></section>
'''
    write("index.html", layout(f"{PROFILE['nome']} — Engenharia de IA", "Portfólio de Beatriz Helena: IA generativa, RAG, agentes, dados e MLflow. Estudos de caso, decisões técnicas e currículo.", body))


def build_projects():
    for index, p in enumerate(PROJECTS):
        next_p = PROJECTS[(index + 1) % len(PROJECTS)]
        outcome = metrics(p['resultados']) if p['resultados'] else '<p class="plan-callout"><strong>Design e requisitos disponíveis.</strong> Esta trilha ainda não tem resultados de execução. O planejamento detalha os critérios de aceite futuros.</p>'
        evidence = f'<a class="text-link" href="../evidencias/{p["evidencia"]}" download>Baixar evidência resumida (JSON) ↓</a>' if p['evidencia'] else ''
        body = f'''<div class="wrap case-breadcrumb"><a href="../index.html#projetos">← Todos os projetos</a><span class="mono">ESTUDO {p['numero']} / 08</span></div><article class="case wrap"><header class="case-hero"><div><p class="eyebrow">{e(p['categoria'])}</p><h1>{e(p['titulo'])}</h1><p class="case-summary">{e(p['resumo'])}</p>{tags(p['stack'])}</div><aside class="case-meta"><span class="status {p['grupo']}">{e(p['status'])}</span><dl><dt>PROJETO</dt><dd>{e(p['subtitulo'])}</dd><dt>CONTEXTO</dt><dd>{'Estudo autoral · bibliotecas fictícias' if p['numero'] < '07' else 'Estudo autoral · fonte pública planejada'}</dd><dt>EVIDÊNCIAS</dt><dd>{'Execuções de 28/10/2026' if p['grupo'] == 'implementado' else 'Planejamento e critérios de aceite'}</dd><dt>REPOSITÓRIO</dt><dd><a href="{e(p.get('repo_url', ''))}" rel="noopener noreferrer">Ver no GitHub ↗</a></dd></dl></aside></header>
<nav class="case-nav" aria-label="Conteúdo deste estudo"><a href="#problema">Problema</a><a href="#arquitetura">Arquitetura</a><a href="#resultados">Resultados e limites</a><a href="#material">Material técnico</a></nav>
<section id="problema" class="case-section two-column"><div><p class="eyebrow">01 / O PROBLEMA</p><h2>Problema</h2></div><div class="prose"><p>{e(p['problema'])}</p><h3>Escopo entregue</h3><p>{e(p['entrega'])}</p></div></section>
<section id="arquitetura" class="case-section"><p class="eyebrow">02 / ARQUITETURA</p><h2>Fluxo do projeto</h2><ol class="architecture" aria-label="Etapas da arquitetura">{''.join(f'<li><span class="mono">{i+1:02d}</span><strong>{e(v)}</strong></li>' for i,v in enumerate(p['fluxo']))}</ol><div class="two-column decisions"><h3>Decisões técnicas</h3>{bullet(p['decisoes'])}</div></section>
<section id="resultados" class="case-section"><p class="eyebrow">03 / RESULTADOS E LIMITES</p><h2>{'O que foi medido' if p['resultados'] else 'Como será avaliado'}</h2>{outcome}<p class="prose validation-copy">{e(p['validacao'])}</p><div class="two-column"><div><h3>Limites conhecidos</h3>{bullet(p['limites'])}</div><div><h3>Próximo incremento</h3>{bullet(p['proximos'])}</div></div>{evidence}</section>
<section id="material" class="case-section"><p class="eyebrow">04 / MATERIAL TÉCNICO</p><div class="section-heading"><h2>Planejamento e exemplos</h2><a class="button secondary" href="../documentacao/{p['slug']}.html">Ler planejamento completo ↗</a></div><div class="code-panel"><div><h3>{e(p['exemplo']['titulo'])}</h3><span class="mono">{e(p['exemplo']['linguagem'])} / {'EXCERTO CONCEITUAL' if p['grupo'] == 'implementado' else 'PROPOSTA NÃO EXECUTADA'}</span></div><pre><code>{e(p['exemplo']['codigo'])}</code></pre></div><div class="material-links"><a href="{e(p.get('repo_url', ''))}" rel="noopener noreferrer">Repositório do projeto no GitHub ↗</a><a href="../documentacao/fontes/{p['slug']}.md" download>Planejamento em Markdown ↓</a>{'<a href="../documentacao/prompts.html">Ver exemplos de prompts estruturados →</a>' if p['numero'] in ('03','04','05') else ''}</div></section>
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
        body = f'''<article class="wrap document"><a class="text-link" href="../projetos/{p['slug']}.html">← Voltar ao estudo</a><header><p class="eyebrow">DOCUMENTAÇÃO / ESTUDO {p['numero']}</p><h1>Planejamento técnico</h1><p class="case-summary">{e(p['subtitulo'])}</p><span class="status {p['grupo']}">{e(p['status'])}</span><p class="scope-note">O plano reúne requisitos e etapas futuras. O estudo de caso distingue as partes executadas. As quantidades de experimentos, métricas e critérios de aceite propostos não indicam resultados já obtidos.</p><a class="button secondary" href="fontes/{p['slug']}.md" download>Baixar Markdown ↓</a></header><div class="markdown">{markdown(source)}</div></article>'''
        write(f"documentacao/{p['slug']}.html", layout(f"Planejamento: {p['subtitulo']} — {PROFILE['nome']}", f"Requisitos, arquitetura, stack, MLflow e critérios de aceite: {p['subtitulo']}.", body, "../", "documento", f"documentacao/{p['slug']}.html"))
    prompt_source = (ROOT / 'documentacao/fontes/prompts.md').read_text(encoding='utf-8')
    body = '<article class="wrap document"><a class="text-link" href="../projetos/laboratorio-llms.html">← Laboratório de LLMs</a><header><p class="eyebrow">DESIGN DE PROMPTS</p><h1>Prompts estruturados</h1><p class="case-summary">Exemplos propostos para experimentos futuros, sem desempenho medido.</p></header><div class="markdown">' + markdown(prompt_source) + '</div></article>'
    write('documentacao/prompts.html', layout('Prompts estruturados — Beatriz Helena', 'Exemplos de prompts, contratos de saída e avaliação planejada.', body, '../', 'documento', 'documentacao/prompts.html'))


def build_cv():
    skills = ''.join(f'<li><strong>{e(x["titulo"])}:</strong> {e(x["descricao"])}</li>' for x in PROFILE['habilidades'])
    body = f'''<article class="wrap resume"><div class="resume-actions"><a href="index.html">← Voltar ao portfólio</a><button type="button" class="button primary" data-print hidden>Imprimir / salvar como PDF ↓</button></div><header class="resume-header"><p class="eyebrow">CURRÍCULO PROFISSIONAL</p><h1>{e(PROFILE['nome'])}</h1><p class="resume-title">{e(PROFILE['titulo'])}</p><div class="footer-links">{public_links()}</div></header><section><h2>Perfil</h2>{''.join(f'<p>{e(x)}</p>' for x in PROFILE['sobre'])}<p>{e(PROFILE['resumo'])}</p></section><section><h2>Habilidades</h2><ul class="prose-list">{skills}</ul></section><section><h2>Experiência</h2>{trajectory()}</section><section><h2>Formação</h2><h3>{e(PROFILE['formacao']['curso'])}</h3><p>{e(PROFILE['formacao']['instituicao'])}</p></section><section><h2>Projetos de estudo</h2><p>Observatório Aurora: pipeline de dados, qualidade, recuperação RAG e boletins com MVPs ou componentes validados no Databricks. Laboratório de LLMs, agentes, pipeline ML e avaliador BEM com planejamento técnico disponível.</p><p><a href="index.html#projetos">Ver os oito estudos de caso e seus estados →</a></p></section></article>'''
    write('curriculo.html', layout(f'Currículo — {PROFILE["nome"]}', f'Currículo de {PROFILE["nome"]}, {PROFILE["titulo"]}.', body, page='curriculo', canonical_path='curriculo.html'))


if __name__ == '__main__':
    assert len(PROJECTS) == 8 and len({p['slug'] for p in PROJECTS}) == 8
    build_home()
    build_projects()
    build_docs()
    build_cv()
    write('404.html', layout('Página não encontrada — Beatriz Helena', 'Volte ao início do portfólio.', '<section class="wrap document"><p class="eyebrow">404</p><h1>Página não encontrada</h1><p>Esta página não foi encontrada.</p><a class="button primary" href="index.html">Abrir o portfólio →</a></section>', page='404'))
    print('Site gerado: início, currículo, 8 estudos, 8 planejamentos, prompts e 404.')
