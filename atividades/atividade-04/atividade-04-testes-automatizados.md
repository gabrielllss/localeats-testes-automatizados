# Atividade 4 — Testes Automatizados do LocalEats

- **Unidade Curricular:** Qualidade de Software — Projeto LocalEats
- **Aluno:** Gabriel Lopes Soares (trabalho individual)
- **Sistema testado:** https://local-eats-unisenac.vercel.app/ (`/static/index.html` e `/static/login.html`)
- **Execução:** `pytest` (unitários + funcional com Playwright)

## Estrutura entregue

```text
atividades/atividade-04/
├── atividade-04-testes-automatizados.md   # este arquivo
├── relatorio-pytest.txt                   # relatório gerado com python -m pytest -v
├── requirements.txt                       # pytest + playwright
├── src/
│   ├── __init__.py
│   └── regras_localeats.py                # Regra 2: calcular_desconto
└── tests/
    ├── __init__.py
    ├── test_regras_localeats.py           # testes unitários (TU01–TU03)
    └── test_localeats.py                  # teste funcional Playwright (TF01)
└── evidencias/
    ├── TF01-filtro-italiana.png           # screenshot gerado pelo TF01 (diferencial)
    └── TF02-pesquisa-centro.png            # screenshot gerado pelo TF02 (diferencial)
```

## Como executar

```powershell
cd atividades/atividade-04
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

No Linux/macOS, troque a última linha por:

```bash
python3 -m pytest -v | tee relatorio-pytest.txt
```

## Parte 1 — Regra implementada (`src/regras_localeats.py`)

**Regra 2 — `calcular_desconto(valor_pedido)`** (retorna o valor do desconto, não o total):

- pedidos abaixo de R$ 100,00 não recebem desconto (retorna `0`);
- pedidos de R$ 100,00 ou mais recebem 10% de desconto (`valor_pedido * 0.10`);
- valores negativos geram `ValueError`.

Exemplos: `calcular_desconto(80)` → `0`; `calcular_desconto(150)` → `15`.

## Identificação das responsabilidades

| ID | Integrante | Tipo | Comportamento verificado | Arquivo e função |
|----|------------|------|--------------------------|------------------|
| TU01 | Gabriel Lopes Soares | Unitário | Sem desconto abaixo de R$ 100 (80 → 0) | tests/test_regras_localeats.py::test_pedido_sem_desconto_abaixo_de_100 |
| TU02 | Gabriel Lopes Soares | Unitário | Desconto de 10% a partir de R$ 100 (100/150/200) | tests/test_regras_localeats.py::test_pedido_com_desconto_dez_porcento |
| TU03 | Gabriel Lopes Soares | Unitário | Valor negativo gera ValueError | tests/test_regras_localeats.py::test_desconto_valor_negativo_gera_erro |
| TF01 | Gabriel Lopes Soares | Funcional | Filtrar restaurantes por categoria (Italiana) | tests/test_localeats.py::test_filtrar_restaurantes_por_categoria_italiana |
| TF02 | Gabriel Lopes Soares | Funcional (diferencial) | Pesquisar restaurante por localização (Centro) | tests/test_localeats.py::test_pesquisar_restaurante_por_localizacao |

Observação: o TU02 é parametrizado (roda com 100/150/200), então aparece como três
itens no relatório (`[100-10]`, `[150-15]`, `[200-20]`) — é **um** teste da tabela com
dados diferentes, não testes duplicados.

## Aplicação simplificada do TDD

### TDD de Gabriel Lopes Soares

- **Regra escolhida:** Regra 2 — `calcular_desconto` (10% de desconto a partir de R$ 100,00; retorna o valor do desconto).
- **Primeiro teste escrito:** `test_pedido_sem_desconto_abaixo_de_100` (80 → `0`).
- **Por que o teste falhou inicialmente:** a função ainda não existia (`ImportError`/`NameError` ao importar de `src.regras_localeats`).
- **Implementação mínima realizada:** criada a função retornando `0` para valores abaixo de 100.
- **Segundo teste escrito:** `test_pedido_com_desconto_dez_porcento`, parametrizado (100 → 10; 150 → 15; 200 → 20), que quebrou a implementação mínima e exigiu o cálculo de 10%.
- **Melhoria ou refatoração realizada:** extraídas as constantes `LIMITE_DESCONTO` e `PERCENTUAL_DESCONTO`, cálculo como `valor_pedido * 0.10`, guarda `ValueError` para negativos e uso de `pytest.approx` nas comparações de ponto flutuante, sem mudar o comportamento dos casos válidos.

## Parte 2 — Teste funcional com Playwright (`tests/test_localeats.py`)

**TF01 — Filtrar restaurantes por categoria (Italiana).** Padrão exigido: acessa o
LocalEats, realiza uma interação pela interface, usa locators do Playwright
(`page.locator(...)`), verifica resultados observáveis com `expect` (sem
`time.sleep`) e roda com `pytest`.

Descoberta da exploração: **sem sessão o `index.html` redireciona para o
`login.html`** (`auth.js` → `checkAuth(true)`). Por isso o próprio teste cria uma
conta com e-mail único via “Criar Conta” e só então testa o filtro — o teste é
independente e não depende de massa de dados prévia.

| ID | Fluxo automatizado | Interação | Assertions (resumo) |
|----|--------------------|-----------|---------------------|
| TF01 | Filtrar por categoria | Cadastra usuário; clica no filtro `Italiana` | Chegou ao `index.html`; filtro com classe `active`; grid contém “Italiana” ou “Nenhum restaurante encontrado” |
| TF02 | Pesquisar por localização (diferencial) | Cadastra usuário; digita “Centro” e clica em Buscar | Barra de pesquisa visível; campo mantém “Centro”; grid contém “Centro” ou “Nenhum restaurante encontrado” |

## Explicação individual

### Explicação — Gabriel Lopes Soares (TF01 + Regra 2)

O teste `test_filtrar_restaurantes_por_categoria_italiana` reproduz o uso mais comum
da vitrine: filtrar por culinária. Explorando o site, descobri que sem sessão o
`index.html` redireciona para o `login.html`; por isso o próprio teste cria uma
conta com e-mail único e só então clica no botão
`.filter-btn[data-cuisine="Italiana"]`. As assertions conferem (1) a chegada ao
`index.html`, (2) o estado ativo do botão (com nova tentativa de clique em
carregamentos lentos) e (3) um resultado observável no grid — aceitando tanto a
lista filtrada (“Italiana”) quanto a mensagem de lista vazia, para não ficar frágil
à massa de dados. Ao final, o teste salva um screenshot em `evidencias/` como
prova da execução. Na Regra 2, o detalhe central é que a função retorna **o valor
do desconto** (150 → 15), não o total do pedido; por isso parametrizei 100/150/200
e usei `pytest.approx` contra erros de ponto flutuante. O terceiro teste
(negativo → `ValueError`) separa “sem desconto” (caso de negócio válido, retorna
`0`) de “valor inválido” (erro de programação, exceção).

## Relatório da execução

Arquivo: `relatorio-pytest.txt` (gerado com `python -m pytest -v`).

Resumo da última execução: **7 testes coletados, 7 aprovados, 0 reprovados.**

- 5 itens unitários (3 funções de teste, sendo 1 parametrizada com 3 casos) em `tests/test_regras_localeats.py`.
- 2 testes funcionais em `tests/test_localeats.py` (navegador Chromium headless via Playwright).

Antes da entrega, conferi que todos os IDs da tabela acima aparecem no relatório
(o TU02 parametrizado aparece com sufixos `[100-10]`, `[150-15]`, `[200-20]`).

## Diferenciais implementados

- [x] Terceiro teste unitário para caso de borda (TU03 — `ValueError`).
- [x] `pytest.raises(ValueError)` para a exceção.
- [x] Parametrização com `pytest.mark.parametrize` (TU02).
- [ ] Cenário BDD em Gherkin / automação com `pytest-bdd` (não implementado).
- [ ] Page Object Model (não implementado — optou-se por um helper simples para manter o teste curto e legível).
- [x] Segundo teste funcional pelo mesmo integrante (TF02 — pesquisa por localização).
- [ ] Execução em mais de um navegador (somente Chromium).
- [x] Screenshots da execução (`evidencias/TF01-filtro-italiana.png` e `evidencias/TF02-pesquisa-centro.png`, gerados pelos próprios testes).
- [x] Registro de comportamento observado: redirecionamento sem sessão (`index.html` → `login.html`) documentado na seção do teste funcional.

## Uso de inteligência artificial

- **Ferramenta utilizada:** assistente de IA (Muse Spark) para apoio na escrita dos testes e deste relatório.
- **Como a ferramenta foi utilizada:** exploração guiada do LocalEats (mapeamento de telas, redirecionamentos e seletores), rascunho da Regra 2 e dos testes unitário/funcional e estrutura deste Markdown.
- **Uma sugestão que precisou ser alterada ou rejeitada:** a primeira versão do teste funcional acessava o `index.html` diretamente sem tratar o redirecionamento para o login — o teste quebraria em contexto limpo. A sugestão foi corrigida: o teste passou a criar um usuário único dentro dele antes de aplicar o filtro.
- **Como o código sugerido foi verificado:** execução real com `python -m pytest -v` (7 passed), leitura dos seletores contra o HTML verdadeiro do site e conferência de que o teste não usa `time.sleep` e usa `expect` com timeout explícito.

## Envio (Blackboard)

Enviar **o link direto para este arquivo no GitHub**, ex.:

`https://github.com/<usuario>/<repositorio>/blob/main/atividade-04/atividade-04-testes-automatizados.md`

O link deve estar acessível ao professor.
