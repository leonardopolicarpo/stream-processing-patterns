# 🚀 Relatório de Otimização de Performance

Este documento registra a evolução da performance do pipeline de ETL.
Ambiente de Teste: [Sua CPU/RAM aproximada]
Dataset: 10 Milhões de registros (Gerados sinteticamente)

## Histórico de Execuções

| Versão | Mudança Principal | Tempo Total | Tempo (UUID/Str) | Status | Arquivo de Log |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **v1** | Implementação inicial com objetos `uuid.UUID` e `Decimal` | ~546s (9m06s) | ~180s (33%) | ✅ Sucesso | [Link](profile_v1_baseline_uuid_objects.txt) |
| **v2** | Remoção de `uuid.UUID`, tratando IDs como `str` primitiva | ~325s (6m) | **0s** | ✅ Sucesso | [Link](profile_v2_string_optimization.txt) |

## Análise Técnica

### v1 -> v2: O Gargalo da Tipagem Forte
O profile `v1` mostrou que a classe `uuid.UUID` do Python gastava 179s apenas validando strings no `__init__`.
Como confiamos na fonte (gerador) ou validamos via Regex, troquei por `str` simples no Domínio.
Isso removeu completamente o overhead de instanciação de objetos para IDs.