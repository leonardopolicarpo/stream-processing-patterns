# 🚀 Relatório de Otimização de Performance

Este documento registra a evolução da performance do pipeline de ETL.
**Ambiente de Teste:** [Ryzen 5 5600G] / [16GB DDR4]
**Dataset:** 10 Milhões de registros (Gerados sinteticamente)

## Histórico de Execuções

| Versão | Mudança Principal | Tempo Total | Throughput (linhas/s) | Status | Arquivo de Log |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **v1** | Implementação inicial com objetos `uuid.UUID` e `Decimal` | ~546s (9m06s) | ~18.315/s | ✅ Sucesso | [Link](profile_v1_baseline_uuid_objects.txt) |
| **v2** | Remoção de `uuid.UUID` (str primitiva) + Descarte de Fraudes (8M inserts) | ~325s (5m25s) | ~24.615/s | ✅ Sucesso | [Link](profile_v2_string_optimization.txt) |
| **v3** | Persistência Total (10M inserts - incluindo Fraudes) | ~376s (6m16s) | **~26.595/s** | ✅ Sucesso | [Link](profile_v3_full_ingestion_with_frauds.txt) |

## Análise Técnica

### v1 -> v2: O Gargalo da Tipagem Forte
O profile `v1` mostrou que a classe `uuid.UUID` do Python consumia cerca de **33% do tempo total** (~179s) apenas validando strings no construtor.
Como a integridade dos IDs é garantida na origem, migrei para `str` primitiva no Domínio.
**Resultado:** Redução de ~40% no tempo total de execução.

### v2 -> v3: Eficiência de Escala (Batch Processing)
Na versão `v3`, removi o filtro de fraudes, obrigando o sistema a escrever **25% mais dados** no disco (de 8 Milhões para 10 Milhões de registros).
* **Impacto no Tempo:** O tempo subiu apenas ~15% (50 segundos), o que é desproporcionalmente baixo em relação ao aumento de volume.
* **Aumento de Throughput:** A vazão média subiu de 24k/s para **26.5k/s**.

**Conclusão:** O sistema demonstra comportamento **sub-linear**. O uso de *Batch Inserts* (lotes de 100k) amortizou o custo extra de I/O, provando que o pipeline escala de forma eficiente mesmo com aumento de carga de escrita.