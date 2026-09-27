# Arquitetura

## Visão geral

O sistema recolhe potenciais clientes B2B (pastelarias, cafés, bares e
restaurantes) através da Google Places API, processa e pontua esses leads,
gera rascunhos de email de outreach personalizados com IA, submete-os a
revisão humana e envia-os através de um serviço transacional. As métricas de
todo o processo alimentam um dashboard.

## Componentes

1. **Agendador** — dispara o pipeline periodicamente (diário/semanal),
   implementado com APScheduler dentro da própria aplicação FastAPI.
2. **Ingestão (Google Places API)** — pesquisa negócios do segmento
   HORECA numa região configurável. Implementado como um adaptador
   (padrão *strategy*) para permitir trocar de fonte de dados (ex.
   OpenStreetMap/Overpass) sem alterar o resto do pipeline.
3. **Processamento & scoring** — limpeza de dados, deduplicação e
   atribuição de uma pontuação de qualificação a cada lead.
4. **PostgreSQL** — armazenamento central: leads, histórico de contactos,
   estado de campanhas. Alimenta tanto a geração de emails como o
   dashboard.
5. **Geração de email (IA)** — usa a API da Anthropic para gerar um
   rascunho de email personalizado por lead, com base nos dados
   recolhidos.
6. **Revisão humana & envio** — os rascunhos ficam pendentes de aprovação
   antes de serem enviados via Resend. Cada email inclui um mecanismo de
   opt-out, em conformidade com o RGPD para outreach B2B na UE.
7. **Dashboard (React)** — visualização das métricas (leads encontrados,
   taxa de aprovação, respostas) e um resumo semanal enviado por email.

## Decisões e justificações

- **Revisão humana antes do envio**: protege a reputação do domínio de
  email e reduz o risco de reclamações; pode evoluir para envio
  semi-automático para leads com pontuação muito alta.
- **Adaptador de ingestão**: a Google Places API tem custos acima do
  crédito gratuito mensal; o adaptador permite testar/demonstrar o
  sistema com uma fonte gratuita sem alterar o pipeline.
- **APScheduler em vez de Celery+Redis**: suficiente para a cadência
  necessária (diária/semanal) sem introduzir infraestrutura adicional;
  documentado como caminho de escala caso o volume cresça.
- **Frontend separado do backend**: API FastAPI expõe apenas endpoints
  REST/JSON; o React consome-os via TanStack Query. Isto demonstra uma
  arquitetura desacoplada, mais fácil de escalar e de apresentar como
  case study.

## Âmbito geográfico (configurável)

Ponto de partida: região Minho / Norte de Portugal. Configurável via
variável de ambiente para outras regiões sem alterar código.
