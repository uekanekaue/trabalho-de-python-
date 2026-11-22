#!/usr/bin/env python3
"""
RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)
Desenvolvido aplicando Pensamento Algorítmico e Programação Orientada a Objetos.
"""

from abc import ABC, abstractmethod
import csv
from pathlib import Path
from typing import Dict, List


class Imovel(ABC):
    """Classe base abstrata que representa um imóvel disponível para locação."""

    def __init__(self, categoria: str, valor_base: float) -> None:
        self.categoria = categoria
        self.valor_base = valor_base

    @abstractmethod
    def calcular_adicional_quartos(self) -> float:
        """Retorna o valor adicional referente à configuração de quartos."""

    @abstractmethod
    def calcular_adicional_garagem(self) -> float:
        """Retorna o valor adicional referente às vagas de garagem."""

    def calcular_subtotal(self) -> float:
        """Calcula o valor do aluguel antes da aplicação de descontos."""
        return (
            self.valor_base
            + self.calcular_adicional_quartos()
            + self.calcular_adicional_garagem()
        )

    def calcular_desconto(self) -> float:
        """Retorna o valor do desconto comercial aplicável ao imóvel."""
        return 0.0

    def calcular_aluguel_mensal(self) -> float:
        """Calcula o valor líquido final do aluguel mensal."""
        return self.calcular_subtotal() - self.calcular_desconto()

    @abstractmethod
    def descrever_caracteristicas(self) -> str:
        """Retorna uma descrição legível das configurações escolhidas."""


class Apartamento(Imovel):
    """Representa um apartamento para locação na R.M Imóveis."""

    VALOR_BASE = 700.00
    ADICIONAL_DOIS_QUARTOS = 200.00
    ADICIONAL_GARAGEM = 300.00
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = 0.05

    def __init__(
        self, quartos: int, possui_garagem: bool, possui_criancas: bool
    ) -> None:
        if quartos not in (1, 2):
            raise ValueError("Apartamentos devem ter 1 ou 2 quartos.")
        super().__init__(categoria="Apartamento", valor_base=self.VALOR_BASE)
        self.quartos = quartos
        self.possui_garagem = possui_garagem
        self.possui_criancas = possui_criancas

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_DOIS_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_garagem(self) -> float:
        return self.ADICIONAL_GARAGEM if self.possui_garagem else 0.0

    def calcular_desconto(self) -> float:
        if not self.possui_criancas:
            return round(
                self.calcular_subtotal() * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS, 2
            )
        return 0.0

    def descrever_caracteristicas(self) -> str:
        vaga_txt = "Com 1 vaga de garagem" if self.possui_garagem else "Sem garagem"
        criancas_txt = "Com crianças" if self.possui_criancas else "Sem crianças (5% desc.)"
        return f"{self.categoria} ({self.quartos} quarto(s) | {vaga_txt} | {criancas_txt})"


class Casa(Imovel):
    """Representa uma casa para locação na R.M Imóveis."""

    VALOR_BASE = 900.00
    ADICIONAL_DOIS_QUARTOS = 250.00
    ADICIONAL_GARAGEM = 300.00

    def __init__(self, quartos: int, possui_garagem: bool) -> None:
        if quartos not in (1, 2):
            raise ValueError("Casas devem ter 1 ou 2 quartos.")
        super().__init__(categoria="Casa", valor_base=self.VALOR_BASE)
        self.quartos = quartos
        self.possui_garagem = possui_garagem

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_DOIS_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_garagem(self) -> float:
        return self.ADICIONAL_GARAGEM if self.possui_garagem else 0.0

    def descrever_caracteristicas(self) -> str:
        vaga_txt = "Com 1 vaga de garagem" if self.possui_garagem else "Sem garagem"
        return f"{self.categoria} ({self.quartos} quarto(s) | {vaga_txt})"


class Estudio(Imovel):
    """Representa um estúdio para locação na R.M Imóveis."""

    VALOR_BASE = 1200.00
    PACOTE_DUAS_VAGAS = 250.00
    VALOR_VAGA_ADICIONAL = 60.00

    def __init__(self, quantidade_vagas: int) -> None:
        if quantidade_vagas < 0 or quantidade_vagas == 1:
            raise ValueError(
                "Para estúdios, informe 0 vagas ou o pacote inicial de 2 ou mais vagas."
            )
        super().__init__(categoria="Estúdio", valor_base=self.VALOR_BASE)
        self.quantidade_vagas = quantidade_vagas

    def calcular_adicional_quartos(self) -> float:
        return 0.0

    def calcular_adicional_garagem(self) -> float:
        if self.quantidade_vagas == 0:
            return 0.0
        vagas_extras = max(0, self.quantidade_vagas - 2)
        return self.PACOTE_DUAS_VAGAS + (vagas_extras * self.VALOR_VAGA_ADICIONAL)

    def descrever_caracteristicas(self) -> str:
        if self.quantidade_vagas == 0:
            vaga_txt = "Sem vagas de estacionamento"
        else:
            extras = self.quantidade_vagas - 2
            vaga_txt = f"{self.quantidade_vagas} vagas (pacote 2 vagas + {extras} extra(s))"
        return f"{self.categoria} ({vaga_txt})"


class OrcamentoLocacao:
    """Gerencia o cálculo contratual, a exibição do orçamento e a projeção anual em CSV."""

    TAXA_CONTRATUAL = 2000.00
    MAX_PARCELAS_TAXA = 5
    MESES_PROJECAO = 12

    def __init__(self, imovel: Imovel, parcelas_taxa: int) -> None:
        if not (1 <= parcelas_taxa <= self.MAX_PARCELAS_TAXA):
            raise ValueError(
                f"O parcelamento da taxa contratual deve ser entre 1 e {self.MAX_PARCELAS_TAXA}x."
            )
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_valor_parcela_taxa(self) -> float:
        return round(self.TAXA_CONTRATUAL / self.parcelas_taxa, 2)

    def gerar_projecao_anual(self) -> List[Dict[str, object]]:
        """Gera a lista de dicionários com a previsão financeira dos 12 primeiros meses."""
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        valor_parcela_taxa = self.calcular_valor_parcela_taxa()
        projecao: List[Dict[str, object]] = []

        for mes in range(1, self.MESES_PROJECAO + 1):
            parcela_vigente = valor_parcela_taxa if mes <= self.parcelas_taxa else 0.0
            total_mes = round(aluguel_mensal + parcela_vigente, 2)
            projecao.append(
                {
                    "Mes": mes,
                    "Categoria_Imovel": self.imovel.categoria,
                    "Aluguel_Mensal_BRL": f"{aluguel_mensal:.2f}",
                    "Parcela_Taxa_Contratual_BRL": f"{parcela_vigente:.2f}",
                    "Total_Mensal_BRL": f"{total_mes:.2f}",
                }
            )
        return projecao

    def exibir_resumo(self) -> None:
        """Exibe no console o demonstrativo completo e transparente do orçamento."""
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        valor_parcela_taxa = self.calcular_valor_parcela_taxa()
        total_primeiro_ano = (aluguel_mensal * self.MESES_PROJECAO) + self.TAXA_CONTRATUAL

        print("\n" + "=" * 62)
        print("           RENTSMART — ORÇAMENTO OFICIAL R.M IMÓVEIS")
        print("=" * 62)
        print(f"Imóvel Selecionado : {self.imovel.descrever_caracteristicas()}")
        print("-" * 62)
        print("1. COMPOSIÇÃO DO ALUGUEL MENSAL (CUSTO RECORRENTE)")
        print(f"   Aluguel-base                : R$ {self.imovel.valor_base:>9.2f}")
        print(f"   Adicional de quartos        : R$ {self.imovel.calcular_adicional_quartos():>9.2f}")
        print(f"   Adicional de garagem/vagas  : R$ {self.imovel.calcular_adicional_garagem():>9.2f}")
        print(f"   Subtotal mensal             : R$ {self.imovel.calcular_subtotal():>9.2f}")
        print(f"   Desconto comercial          : -R${self.imovel.calcular_desconto():>9.2f}")
        print(f"   >> ALUGUEL MENSAL LÍQUIDO   : R$ {aluguel_mensal:>9.2f}")
        print("-" * 62)
        print("2. TAXA CONTRATUAL (CUSTO ADMINISTRATIVO SEPARADO)")
        print(f"   Valor total da taxa         : R$ {self.TAXA_CONTRATUAL:>9.2f}")
        print(
            f"   Condição escolhida          : {self.parcelas_taxa}x de R$ {valor_parcela_taxa:.2f} "
            f"(nos {self.parcelas_taxa} primeiro(s) mês(es))"
        )
        print("-" * 62)
        print("3. RESUMO DO PRIMEIRO ANO (12 MESES)")
        print(
            f"   Meses 1 a {self.parcelas_taxa:<2} (Aluguel + Taxa): "
            f"R$ {aluguel_mensal + valor_parcela_taxa:>9.2f} / mês"
        )
        if self.parcelas_taxa < self.MESES_PROJECAO:
            print(
                f"   Meses {self.parcelas_taxa + 1} a 12 (Somente Aluguel): "
                f"R$ {aluguel_mensal:>9.2f} / mês"
            )
        print(f"   Total previsto em 12 meses  : R$ {total_primeiro_ano:>9.2f}")
        print("=" * 62)

    def exportar_csv(self, caminho_arquivo: str = "projecao_locacao_12_meses.csv") -> Path:
        """Exporta a projeção de 12 meses para um arquivo CSV formatado."""
        destino = Path(caminho_arquivo)
        dados = self.gerar_projecao_anual()
        colunas = [
            "Mes",
            "Categoria_Imovel",
            "Aluguel_Mensal_BRL",
            "Parcela_Taxa_Contratual_BRL",
            "Total_Mensal_BRL",
        ]

        with destino.open(mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
            escritor.writeheader()
            escritor.writerows(dados)

        return destino.resolve()


# ==============================================================================
# Funções auxiliares de entrada e validação de interface de linha de comando
# ==============================================================================


def ler_opcao_inteira(mensagem: str, opcoes_validas: tuple[int, ...]) -> int:
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit() and int(entrada) in opcoes_validas:
            return int(entrada)
        print(f"Entrada inválida. Escolha uma das opções: {opcoes_validas}.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        entrada = input(mensagem).strip().upper()
        if entrada in ("S", "SIM"):
            return True
        if entrada in ("N", "NAO", "NÃO"):
            return False
        print("Entrada inválida. Digite 'S' para Sim ou 'N' para Não.")


def ler_vagas_estudio() -> int:
    while True:
        entrada = input(
            "Deseja quantas vagas de estacionamento? (0 = nenhuma | mínimo 2 para pacote): "
        ).strip()
        if entrada.isdigit():
            vagas = int(entrada)
            if vagas == 0 or vagas >= 2:
                return vagas
        print("Entrada inválida. Informe 0 (sem vagas) ou 2 ou mais vagas.")


def executar_aplicacao() -> None:
    print("==============================================================")
    print("       BEM-VINDO AO RENTSMART — R.M IMÓVEIS")
    print("==============================================================")
    print("Selecione a categoria do imóvel desejado:")
    print("  [1] Apartamento (Base: R$ 700,00)")
    print("  [2] Casa        (Base: R$ 900,00)")
    print("  [3] Estúdio     (Base: R$ 1.200,00)")

    tipo = ler_opcao_inteira("Opção (1, 2 ou 3): ", (1, 2, 3))

    imovel: Imovel
    if tipo == 1:
        quartos = ler_opcao_inteira("Quantidade de quartos (1 ou 2): ", (1, 2))
        garagem = ler_sim_nao("Deseja incluir 1 vaga de garagem (+R$ 300,00)? [S/N]: ")
        criancas = ler_sim_nao("O locatário possui crianças residindo no imóvel? [S/N]: ")
        imovel = Apartamento(quartos=quartos, possui_garagem=garagem, possui_criancas=criancas)
    elif tipo == 2:
        quartos = ler_opcao_inteira("Quantidade de quartos (1 ou 2): ", (1, 2))
        garagem = ler_sim_nao("Deseja incluir 1 vaga de garagem (+R$ 300,00)? [S/N]: ")
        imovel = Casa(quartos=quartos, possui_garagem=garagem)
    else:
        vagas = ler_vagas_estudio()
        imovel = Estudio(quantidade_vagas=vagas)

    parcelas_taxa = ler_opcao_inteira(
        "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
        (1, 2, 3, 4, 5),
    )

    orcamento = OrcamentoLocacao(imovel=imovel, parcelas_taxa=parcelas_taxa)
    orcamento.exibir_resumo()

    nome_arquivo = input(
        "\nNome do arquivo CSV para salvar a projeção [Enter para 'projecao_locacao_12_meses.csv']: "
    ).strip()
    if not nome_arquivo:
        nome_arquivo = "projecao_locacao_12_meses.csv"
    elif not nome_arquivo.lower().endswith(".csv"):
        nome_arquivo += ".csv"

    caminho_salvo = orcamento.exportar_csv(nome_arquivo)
    print(f"\n[OK] Projeção de 12 meses exportada com sucesso para:\n     {caminho_salvo}")


if __name__ == "__main__":
    executar_aplicacao()
