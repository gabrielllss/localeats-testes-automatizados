"""Testes funcionais do LocalEats com Playwright (pytest).

Trabalho individual — dois fluxos (o segundo é diferencial):
- TF01: filtrar restaurantes por categoria;
- TF02: pesquisar restaurante por localização.
Responsável: Gabriel Lopes Soares.

O teste usa locators do Playwright, possui três assertions, não usa
esperas fixas e é independente (cria seu próprio usuário quando precisa
de autenticação).
"""

import re
import uuid
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE_URL = "https://local-eats-unisenac.vercel.app/static/"
BROWSER_ARGS = ["--no-sandbox"]
EVIDENCIAS_DIR = Path(__file__).resolve().parent.parent / "evidencias"


def _email_unico():
    return f"qa{uuid.uuid4().hex[:8]}@teste.com"


def _registrar_usuario(page):
    """Preenche o formulário 'Criar Conta' e conclui o cadastro.

    Retorna ao chamar com a página já em login.html. Ao final, a página
    deve estar em index.html (usuário autenticado).
    """
    page.goto(BASE_URL + "login.html")
    page.locator("#showRegisterBtn").click()
    page.locator("#regName").fill("Aluno Teste")
    page.locator("#regEmail").fill(_email_unico())
    page.locator("#regPassword").fill("Senha123")
    page.locator("#registerForm button[type='submit']").click()
    expect(page).to_have_url(re.compile(r"index\.html"), timeout=20000)


def test_filtrar_restaurantes_por_categoria_italiana():
    # TF01 — selecionar uma categoria e verificar os restaurantes filtrados
    # Responsável: Gabriel Lopes Soares
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
        context = browser.new_context()
        page = context.new_page()
        try:
            _registrar_usuario(page)

            # Assertion 1: após o cadastro, chegou à página inicial.
            expect(page).to_have_url(re.compile(r"index\.html"), timeout=20000)
            expect(page.locator("#restaurantGrid")).to_be_visible(timeout=20000)
            # Garante que o JavaScript da página terminou de carregar antes
            # de interagir (evita clicar antes dos listeners serem anexados).
            page.wait_for_load_state("domcontentloaded")

            # Interação: filtra pela categoria Italiana. Em carregamentos
            # lentos o clique pode ocorrer antes dos listeners, então tenta
            # até 3 vezes até o filtro ficar marcado como ativo.
            filtro_italiana = page.locator('.filter-btn[data-cuisine="Italiana"]')
            expect(filtro_italiana).to_be_visible(timeout=20000)
            filtro_ativado = False
            for _ in range(3):
                filtro_italiana.click()
                try:
                    # Assertion 2: o filtro ficou marcado como ativo.
                    expect(filtro_italiana).to_have_class(
                        re.compile(r"active"), timeout=5000
                    )
                    filtro_ativado = True
                    break
                except AssertionError:
                    continue
            assert filtro_ativado, "filtro Italiana não ficou ativo após 3 cliques"

            # Assertion 3: o grid mostra resultado observável do filtro.
            expect(page.locator("#restaurantGrid")).to_contain_text(
                re.compile(r"Italiana|Nenhum restaurante encontrado"),
                timeout=20000,
            )

            # Evidência da execução (diferencial): captura de tela do
            # resultado do filtro aplicado.
            EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(EVIDENCIAS_DIR / "TF01-filtro-italiana.png"))
        finally:
            context.close()
            browser.close()


def test_pesquisar_restaurante_por_localizacao():
    # TF02 — pesquisar um restaurante pela localização (diferencial:
    # segundo teste funcional pelo mesmo integrante)
    # Responsável: Gabriel Lopes Soares
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
        context = browser.new_context()
        page = context.new_page()
        try:
            _registrar_usuario(page)

            # Assertion 1: página inicial carregada com a barra de pesquisa.
            expect(page).to_have_url(re.compile(r"index\.html"), timeout=20000)
            expect(page.locator("#searchInput")).to_be_visible(timeout=20000)
            page.wait_for_load_state("domcontentloaded")

            # Interação: pesquisa por "Centro".
            page.locator("#searchInput").fill("Centro")
            page.locator("#searchBtn").click()

            # Assertion 2: o termo digitado permanece no campo de busca.
            expect(page.locator("#searchInput")).to_have_value("Centro")

            # Assertion 3: o grid mostra resultado observável da pesquisa.
            expect(page.locator("#restaurantGrid")).to_contain_text(
                re.compile(r"Centro|Nenhum restaurante encontrado"),
                timeout=20000,
            )

            # Evidência da execução (diferencial): captura de tela do
            # resultado da pesquisa.
            EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(EVIDENCIAS_DIR / "TF02-pesquisa-centro.png"))
        finally:
            context.close()
            browser.close()
