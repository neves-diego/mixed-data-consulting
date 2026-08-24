# 01 — Qualidade dos dados

## Objetivo

Antes de iniciar qualquer análise financeira, comercial ou operacional, a primeira etapa da consultoria é avaliar a qualidade das informações recebidas.

O objetivo deste diagnóstico é identificar problemas que possam comprometer os indicadores e as conclusões do projeto.

## Dimensões avaliadas

- Completude: existência de campos vazios ou ausentes;
- Unicidade: identificação de registros duplicados;
- Consistência: compatibilidade entre campos relacionados;
- Padronização: uniformidade de nomes, categorias e formatos;
- Integridade: existência de relacionamentos válidos entre as bases;
- Atualização: adequação das datas ao período analisado.

## Bases avaliadas

| Base | Finalidade |
|---|---|
| Cadastro de clientes | Identificar clientes, segmentos e responsáveis |
| Contratos | Entender serviços e valores recorrentes |
| Faturamento | Analisar receitas e pagamentos |
| Projetos pontuais | Avaliar projetos, horas e valores contratados |
| Horas da equipe | Avaliar utilização da capacidade operacional |
| Comercial | Analisar leads e oportunidades |
| Entregas de comunicação | Relacionar produção, serviços e equipe |

## Procedimento

A análise será realizada inicialmente sobre os dados brutos, sem alteração dos arquivos originais.

Para cada base serão avaliados:

1. quantidade de registros;
2. quantidade e tipo das colunas;
3. valores ausentes;
4. duplicidades;
5. categorias distintas;
6. inconsistências de nomenclatura;
7. tipos de dados e formatos de data;
8. possíveis problemas de relacionamento entre tabelas.

## Registro de achados

Esta seção será preenchida durante a análise. Nenhum problema será considerado confirmado antes de ser identificado nos dados.

| ID | Base | Problema | Impacto potencial | Tratamento |
|---|---|---|---|---|
| Q01 | — | Em análise | — | — |

## Critério para tratamento

Os dados brutos não serão sobrescritos. As correções serão aplicadas em uma camada de dados tratados, permitindo rastrear o que foi alterado e preservar a origem das informações.

## Próxima etapa

Após a conclusão do diagnóstico, os problemas identificados serão documentados e será criada a camada `data/processed/` com os dados padronizados para análise.