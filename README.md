# Beatriz Helena — portfólio para GitHub Pages

Site estático com currículo, oito estudos de caso, planejamentos técnicos e evidências resumidas. O pacote já contém as páginas prontas. Não exige npm, bibliotecas externas, conta Databricks ou chaves de API para o visitante.

## Visualizar agora

Abra `index.html` em um navegador. A navegação e os filtros funcionam sem servidor e sem requisições de dados. Para uma prévia HTTP opcional, execute na raiz do pacote:

```text
python -m http.server 8000 --bind 127.0.0.1
```

Depois abra `http://127.0.0.1:8000/`. O Python serve apenas para desenvolvimento; não faz parte do site publicado.

## Publicar depois no GitHub Pages

1. Extraia o ZIP e coloque o **conteúdo da pasta `site`** na raiz do repositório escolhido, deixando `index.html` na raiz. Inclua `.nojekyll`, inclusive se o explorador ocultar arquivos que começam com ponto.
2. Para o endereço pessoal `SEU_USUARIO.github.io`, o repositório deve se chamar `SEU_USUARIO.github.io`. Para um repositório de projeto, o endereço será `SEU_USUARIO.github.io/NOME_DO_REPO/`.
3. Faça o upload dos arquivos no repositório quando decidir publicá-los.
4. Em **Settings → Pages → Build and deployment**, selecione **Deploy from a branch**, a branch que contém os arquivos e **/(root)**. Salve.
5. Confira a conclusão da publicação em Actions e abra a URL indicada pelo GitHub.

Todos os caminhos do conteúdo são relativos, compatíveis com o domínio pessoal e com uma subpasta de projeto. Não é necessário configurar um domínio, criar `CNAME`, adotar Jekyll nem instalar um framework. `404.html` é uma página básica de recuperação; em URLs inválidas aninhadas, o comportamento de caminhos relativos pode variar, por isso os links normais usam arquivos `.html` explícitos.

Nenhum repositório, conexão Git ou site hospedado foi criado durante esta preparação. A publicação futura é uma decisão da autora.

Referências oficiais consultadas em 05/11/2026: [configurar a origem de publicação](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [criar um site e usar .nojekyll](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Editar sem framework

- `conteudo/perfil.json`: nome, apresentação, habilidades, experiência, formação e contatos públicos. Os cargos, períodos e descrições foram preservados conforme o material fornecido. Não foi inventada uma descrição para DGB Tecnologia, nem datas de formação.
- `conteudo/projetos.json`: oito estudos, tecnologias, estados, métricas e próximos passos.
- `documentacao/fontes/*.md`: planejamentos e exemplos de prompts. Arquivos públicos, sem caminhos ou identificadores do workspace pessoal.
- `assets/styles.css`: cores, layout responsivo e impressão.
- `assets/site.js`: busca/filtros locais e botão de impressão do currículo.
- `tools/build.py`: gera todas as páginas com a biblioteca padrão do Python 3.
- `tools/verify.py`: verifica links locais, estados, evidências e ausência de identificadores privados conhecidos.

Após editar os arquivos de conteúdo:

```text
python tools/build.py
python tools/verify.py
```

As páginas acompanham o pacote para publicação direta; o GitHub Pages não precisa executar esses comandos. Não edite apenas o HTML se pretender regenerar: o build substitui as páginas a partir do JSON e dos Markdown.

## Nome, contatos e SEO

O nome de exibição é **Beatriz Helena**, conforme o ambiente de estudo. Revise se preferir incluir um sobrenome. Os links GitHub, LinkedIn e e-mail estão vazios; campos vazios não geram botões ou links fictícios. Preencha apenas os contatos que desejar tornar públicos e execute o build.

O campo `site_url` deve ficar vazio até você saber a URL final. Depois, pode ser preenchido com `https://SEU_USUARIO.github.io` ou `https://SEU_USUARIO.github.io/NOME_DO_REPO`, sem barra final. O build gera URLs canônicas com esse valor. Os metadados de descrição e Open Graph já estão nas páginas. Não há analytics, cookies, formulários, fontes remotas ou chamadas ao Databricks no navegador.

## Resultados e autoria

Os estudos são autorais em domínios fictícios ou com fontes públicas planejadas. Os arquivos públicos foram preparados a partir dos planos e resumos das execuções de 28/10/2026. Não incluem código corporativo, dados internos, logs de autenticação, segredos ou links para a conta pessoal.

Há três MVPs validados (dados, qualidade e boletins) e um projeto com recuperação RAG lexical/vetorial validada. Geração LLM, multiagentes, treino do projeto ML e execução do BEM não foram demonstrados. Bibliotecas das trilhas planejadas são candidatas, não dependências já instaladas. Os exemplos na página são excertos conceituais; o pacote entrega o **código do site**, os planos e evidências resumidas, e não um instalador dos recursos Databricks.

As métricas não são telemetria em tempo real. No RAG, o resultado foi 14/15 perguntas com documento esperado em top-1 e top-2, com um erro de paráfrase preservado. Os 16 testes lexicais usam outro conjunto, sem provar superioridade entre métodos.

O currículo foi criado para impressão pelo navegador em `curriculo.html` → **Imprimir / salvar como PDF**. Nenhum arquivo PDF é pré-gerado.
