"""Testes unitários da Regra 2 do LocalEats (pytest).

Trabalho individual — Regra 2: calcular_desconto.
Responsável: Gabriel Lopes Soares.
"""

import pytest

from src.regras_localeats import calcular_desconto


def test_pedido_sem_desconto_abaixo_de_100():
    # TU01 — comportamento válido/esperado: abaixo de R$ 100 não há desconto
    # Responsável: Gabriel Lopes Soares
    assert calcular_desconto(80) == 0


@pytest.mark.parametrize(
    "valor, esperado",
    [(100, 10), (150, 15), (200, 20)],
)
def test_pedido_com_desconto_dez_porcento(valor, esperado):
    # TU02 — limite/comportamento alternativo: a partir de R$ 100, 10% de desconto
    # (parametrização: diferencial). Responsável: Gabriel Lopes Soares
    assert calcular_desconto(valor) == pytest.approx(esperado)


def test_desconto_valor_negativo_gera_erro():
    # TU03 — situação inválida: valor negativo gera ValueError (diferencial)
    # Responsável: Gabriel Lopes Soares
    with pytest.raises(ValueError):
        calcular_desconto(-1)
