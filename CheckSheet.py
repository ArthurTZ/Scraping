import pandas as pd
from business_scraper import BusinessScraper
import random
import json
import os

class CheckSheet:
    def __init__(self, input_file, output_file, scraper: BusinessScraper):
        self.input_file = input_file
        self.output_file = output_file
        self.scraper = scraper
        self.request_count = 0
        self.daily_limit = random.randint(30, 45)

    def process_cnpj(self, email: str, password: str):
        """Processa os CNPJs listados no arquivo de entrada."""
        df = pd.read_excel(self.input_file, dtype={"CNPJ": str})
        results = []
        
        self.scraper.login(email, password)
        
        for idx, row in df.iterrows():
            if self.request_count >= self.daily_limit:
                print(f"🎯 Limite diário de {self.daily_limit} consultas atingido. Encerrando...")
                break
            
            self.request_count += 1
            cnpj = row['CNPJ/Código do cliente']
            print(f"🔍 Consultando CNPJ: {cnpj}")
            
            self.scraper.search_cnpj(cnpj)
            
            results.append({"CNPJ": cnpj, "Status": "Processado"})
        
        pd.DataFrame(results).to_excel(self.output_file, index=False)
        print(f"✅ Empresas salvas em {self.output_file}")
        return self.output_file

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        scraper = BusinessScraper(browser)
        check_sheet = CheckSheet("empresas.xlsx", "resultado.xlsx", scraper)
        check_sheet.process_cnpj("seu_email", "sua_senha")
        browser.close()
