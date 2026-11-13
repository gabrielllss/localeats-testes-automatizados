"""Regra de negócio do LocalEats (Atividade 4 - Qualidade de Software).

Trabalho individual — Regra 2: desconto do pedido.
"""

LIMITE_DESCONTO = 100.0
PERCENTUAL_DESCONTO = 0.10


def calcular_desconto(valor_pedido):
    """Regra 2: calcula o desconto do pedido (retorna o valor do desconto).

    - pedidos abaixo de R$ 100,00 não recebem desconto (retorna 0);
    - pedidos de R$ 100,00 ou mais recebem 10% de desconto;
    - valores negativos geram ValueError.
    """
    if valor_pedido < 0:
        raise ValueError("valor do pedido não pode ser negativo")
    if valor_pedido < LIMITE_DESCONTO:
        return 0
    return valor_pedido * PERCENTUAL_DESCONTO
