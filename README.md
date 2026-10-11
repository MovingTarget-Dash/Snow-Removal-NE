# New England Snow Removal — site (snowremoval-ne.com)

Site estático (HTML/CSS/JS), 15 páginas, pronto para publicar na Vercel.

## Estrutura
- `site/` — o que vai para o ar (páginas, `assets/`, `api/lead.js`, `vercel.json`, `sitemap.xml`, `robots.txt`)
- `build/build.py` — gerador: todos os textos, contatos e imagens estão neste arquivo. Para mudar algo, edite e rode `python build/build.py`.

## Antes de publicar
1. **Formulário:** crie conta no Resend, verifique o domínio e defina na Vercel: `RESEND_API_KEY`, `LEAD_FROM` (ex.: `New England Snow Removal <leads@snowremoval-ne.com>`) e, se quiser, `LEAD_TO` (padrão: deck@newenglandcarpenters.com). A função `site/api/lead.js` não pôde ser testada neste ambiente (sem Node): teste o envio no primeiro deploy.
2. **Domínio:** apontar `snowremoval-ne.com` para o projeto na Vercel.
3. **Conteúdo pendente (ainda de exemplo):** depoimentos (marcados "example"), fotos (provisórias, algumas de banco de imagens/terceiros), artigos do blog, legendas da galeria, textos legais (revisão jurídica).
4. **Rastreamento:** não há Google Analytics/Meta Pixel; incluir os IDs quando existirem (e na página `/thank-you/` para conversão).

## Rodar localmente
`cd site && python -m http.server 8780` e abrir http://127.0.0.1:8780/ (o formulário só envia de verdade na Vercel).
