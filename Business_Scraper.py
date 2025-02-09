from playwright.sync_api import sync_playwright
import time
import random
from faker import Faker
import re

class BusinessScraper:
    def __init__(self, browser):
        self.browser = browser
        self.fake = Faker('pt_BR')
        self.context = browser.new_context(
            user_agent=self.fake.user_agent(),
            viewport={'width': random.randint(1366, 1920), 'height': random.randint(768, 1080)},
            locale='pt-BR',
            timezone_id='America/Sao_Paulo',
            permissions=['geolocation']
        )
        self.page = self.context.new_page()
        self._disable_automation_flags()
        
    def _disable_automation_flags(self):
        """Remove indicadores de automação do navegador"""
        self.page.add_init_script("""
            delete Object.getPrototypeOf(navigator).webdriver;
            window.navigator.chrome = { runtime: {}, };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

    def _human_delay(self, min=1, max=3):
        """Atraso humano com variação aleatória"""
        time.sleep(random.uniform(min, max) * (1 + random.random()))

    def _human_mouse_move(self, element):
        """Movimento de mouse humano"""
        box = element.bounding_box()
        self.page.mouse.move(
            box['x'] + random.randint(0, int(box['width'])),
            box['y'] + random.randint(0, int(box['height'])),
            steps=random.randint(10, 30)
        )
        self._human_delay(0.1, 0.3)

    def login(self, email: str, senha: str):
        """Realiza o login na plataforma de consulta"""
        self.page.goto("https://example.com/login")
        self.page.get_by_label("E-mail *").fill(email)
        self.page.wait_for_timeout(3000)
        self.page.get_by_label("Senha *").fill(senha)
        self.page.wait_for_timeout(3000)
        self.page.get_by_role("button", name="ENTRAR").click()
        self.page.wait_for_load_state("networkidle")

    def search_cnpj(self, cnpj: str):
        """Preenche o CNPJ no campo de busca e realiza a pesquisa"""
        try:
            self._human_delay(2, 5)
            input_field = self.page.get_by_placeholder("Digite o CNPJ")
            self._human_mouse_move(input_field)
            input_field.click()
            self._human_delay(3, 7)
            
            for char in cnpj:
                input_field.type(char, delay=random.randint(80, 150))
                if random.random() < 0.05:
                    input_field.type('Backspace', delay=random.randint(50, 100))
                    input_field.type(char, delay=random.randint(80, 150))
            
            self._human_delay(2, 4)
            print(f"✅ CNPJ {cnpj} pesquisado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao pesquisar CNPJ: {e}")

    def close(self):
        """Fecha o contexto do navegador"""
        self.context.close()
        self.browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        scraper = BusinessScraper(browser)
        scraper.login("seu_email", "sua_senha")
        scraper.search_cnpj("12345678000195")
        scraper.close()
