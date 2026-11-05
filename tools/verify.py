"""Verifica o pacote estático sem dependências: links, HTML e conteúdo público."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.issues = set(), [], []
        self.headings = 0
        self.lang = None
        self.viewport = False
        self.title = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if 'id' in data:
            if data['id'] in self.ids:
                self.issues.append('ID repetido: ' + data['id'])
            self.ids.add(data['id'])
        if tag == 'html':
            self.lang = data.get('lang')
        if tag == 'h1':
            self.headings += 1
        if tag == 'title':
            self.title = True
        if tag == 'meta' and data.get('name') == 'viewport':
            self.viewport = True
        for key in ('href','src'):
            if key in data:
                self.refs.append(data[key])


def verify():
    problems = []
    pages = {}
    for path in sorted(ROOT.rglob('*.html')):
        parsed = Page()
        parsed.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = parsed
        if parsed.lang != 'pt-BR' or parsed.headings != 1 or not parsed.viewport or not parsed.title:
            problems.append(f'{path.name}: lang, h1, viewport ou título inválido')
        problems.extend(f'{path.name}: {issue}' for issue in parsed.issues)
    references = 0
    for path, parsed in pages.items():
        for ref in parsed.refs:
            url = urlsplit(ref)
            if url.scheme in ('https','http','mailto','data'):
                continue
            if url.scheme or url.netloc or url.path.startswith('/'):
                problems.append(f'{path.name}: referência incompatível com subpasta: {ref}')
                continue
            dest = (path.parent / unquote(url.path)).resolve() if url.path else path
            references += 1
            if not dest.is_relative_to(ROOT.resolve()) or not dest.is_file():
                problems.append(f'{path.name}: arquivo inexistente ou fora do pacote: {ref}')
            if url.fragment and dest in pages and unquote(url.fragment) not in pages[dest].ids:
                problems.append(f'{path.name}: âncora ausente: {ref}')
    projects = json.loads((ROOT / 'conteudo/projetos.json').read_text(encoding='utf-8'))
    if len(projects) != 8 or sum(p['grupo'] == 'implementado' for p in projects) < 4:
        problems.append('Contagem/estados dos estudos incorretos')
    for project in projects:
        if project['grupo'] == 'planejado' and (project['resultados'] or project['evidencia']):
            problems.append(project['slug'] + ': planejamento marcado como resultado')
    proof = {p.stem:json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'evidencias').glob('*.json')}
    if proof['pipeline']['bronze_rows'] != 5000 or proof['qualidade']['integration_passed'] != 24 or proof['boletins']['reports'] != 3:
        problems.append('Resumo das evidências divergente da entrega original')
    if proof['rag']['metrics']['top1_accuracy'] != 14/15 or not proof['rag']['known_failure']:
        problems.append('Benchmark RAG sem métrica/falha esperadas')
    forbidden = [r'dbc-[a-f0-9-]+\.cloud\.databricks\.com', r'/Users/[^/\s]+@', r'Bearer\s+[A-Za-z0-9]', r'dapi[a-f0-9]{24,}', r'C:\\Users\\', r'\.conexao[\\/]', r'api[_-]?key\s*[:=]\s*[\"\'][A-Za-z0-9_-]{16,}']
    # Padrões de busca acima são deliberadamente usados apenas na própria ferramenta.
    for path in ROOT.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or '.git' in path.parts or path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix not in ('.html','.md','.json','.js','.css','.py','.svg'):
            continue
        data = path.read_text(encoding='utf-8')
        for pattern in forbidden:
            if re.search(pattern, data, flags=re.I):
                problems.append(f'{path.relative_to(ROOT)}: identificador privado ou padrão de segredo')
        if path.suffix == '.html' and re.search(r'<(?:script|link(?![^>]*rel="canonical"))[^>]+(?:src|href)=[\"\']https?://', data):
            problems.append(f'{path.name}: recurso de execução externo')
    if not (ROOT / '.nojekyll').is_file():
        problems.append('.nojekyll ausente')
    result = {'passed': not problems, 'html_pages': len(pages), 'local_references_checked': references, 'projects': len(projects), 'public_evidence_files': len(proof), 'issues': problems}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if problems:
        raise SystemExit(1)
    return result


if __name__ == '__main__':
    verify()
