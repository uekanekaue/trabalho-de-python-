# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação em Python orientada a objetos para calcular orçamentos de locação da **R.M Imóveis**, apresentar o detalhamento separando aluguel mensal e taxa contratual e gerar a projeção de 12 meses em CSV.

## Estrutura de Classes
- `Imovel`: classe base abstrata que define a interface e o cálculo base do aluguel.
- `Apartamento`, `Casa`, `Estudio`: subclasses com regras específicas de valor base, adicionais de quartos e garagem/vagas, além do desconto de 5% para apartamentos sem crianças.
- `OrcamentoLocacao`: calcula o parcelamento da taxa contratual (R$ 2.000,00 em até 5x), exibe o resumo no console e exporta a projeção de 12 meses para `.csv`.

## Regras de Negócio
- **Aluguel base:** Apartamento 1 quarto (R$ 700,00), Casa 1 quarto (R$ 900,00) e Estúdio (R$ 1.200,00).
- **Adicionais:** 2º quarto (+R$ 200,00 no apartamento; +R$ 250,00 na casa); garagem em casa/apartamento (+R$ 300,00); estacionamento em estúdio (R$ 250,00 para pacote inicial de 2 vagas + R$ 60,00 por vaga adicional).
- **Desconto:** 5% sobre o aluguel mensal de apartamentos quando não há crianças.
- **Taxa contratual:** R$ 2.000,00, parcelável de 1x a 5x, exibida separadamente do aluguel mensal.

## Como Executar
1. Tenha o **Python 3** instalado.
2. Abra o terminal na pasta do projeto e execute:

```bash
python rentsmart.py
