## Web Scraper Automatizado

Este projeto contém um scraper automatizado para interagir com uma plataforma de consulta empresarial, realizando buscas por CNPJ e coletando informações relevantes. Ele simula o comportamento humano para evitar detecção, garantindo a eficiência das consultas.

## 📌 Visão Geral

O projeto utiliza o Playwright para automatizar a navegação em um portal de consulta, permitindo:

Login automático

Pesquisa de CNPJ

Extração de dados empresariais (quantidade de funcionários, telefone, data de abertura, etc.)

Armazenamento de resultados em Excel, JSON ou TXT

Rotação de User-Agent para evitar bloqueios

Simulação de movimento humano do mouse

## 🚀 Tecnologias Utilizadas

Python 3.9+

Playwright

Pandas

Faker

Random

## 📦 Instalação

Antes de começar, instale as dependências:
```sh
pip install playwright pandas faker openpyxl
playwright install
```

## 🛠️ Como Usar

Configuração Inicial:

Certifique-se de ter um arquivo Excel contendo CNPJs na coluna CNPJ.

Configure seu e-mail e senha para login na plataforma de consulta.

Executando a Automação:
```python
from playwright.sync_api import sync_playwright
from business_scraper import BusinessScraper
from check_sheet import CheckSheet

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    scraper = BusinessScraper(browser)
    check_sheet = CheckSheet("empresas.xlsx", "resultado.xlsx", scraper)
    check_sheet.process_cnpj("seu_email", "sua_senha")
    browser.close()
```

## 🔄 Rotação de User-Agent

Para evitar detecção, o scraper possui um método para alterar dinamicamente o User-Agent a cada conjunto de consultas. Esse método simula diferentes navegadores e dispositivos, reduzindo a chance de bloqueios:

```python
def _rotate_user_agent(self):
    """Rotaciona o User-Agent periodicamente"""
    if self.request_count % 5 == 0:
        self.scraper.context.set_extra_http_headers({
            'User-Agent': self.scraper.fake.user_agent()
        })
```

Essa rotação ocorre a cada 5 consultas realizadas.

## 🏁 Simulação de Comportamento Humano

Para tornar a automação mais realista e evitar detecção, o scraper simula ações humanas como:

Atrasos aleatórios entre interações para imitar tempos de reação naturais.

Movimentação aleatória do mouse antes de clicar em botões e campos de entrada.

Digitação simulada com variações de velocidade, incluindo pequenas pausas e correções.

```python
Exemplo de movimentação simulada do mouse:
def _human_mouse_move(self, element):
    """Movimenta o mouse de forma realista até o elemento alvo"""
    box = element.bounding_box()
    self.page.mouse.move(
        box['x'] + random.randint(0, int(box['width'])),
        box['y'] + random.randint(0, int(box['height'])),
        steps=random.randint(10, 30)
    )
```

### Essa abordagem reduz a possibilidade de bloqueios por detecção automatizada.

## 📊 Formatos de Saída

Os dados extraídos podem ser salvos nos seguintes formatos:

Excel (.xlsx) - Com informações detalhadas das empresas

JSON (.json) - Estruturado para consumo programático

TXT (.txt) - Listas simples de CNPJs aprovados e reprovados

## ⚠️ Observações

O uso desta ferramenta deve respeitar os termos de serviço da plataforma de consulta.

Caso um CAPTCHA seja detectado, o processo solicitará intervenção manual.

Há um limite diário de consultas para evitar bloqueios.

Os métodos de automação incluem delays aleatórios e movimentação simulada do mouse para evitar detecção.

## 📜 Licença

Este projeto está sob a licença MIT.


