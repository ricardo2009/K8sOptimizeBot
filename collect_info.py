import os  
import time  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from dotenv import set_key  
  
# Configuração do webdrive (referenciando o Windows diretamente)  
WINDOWS_EDGE_DRIVER_PATH = "/mnt/c/webdrive/msedgedriver.exe"  
  
# URL a ser acessada  
TARGET_URL = "https://applens.trafficmanager.net/"  
  
def update_env_variable(key, value):  
    """  
    Atualiza uma variável no arquivo `.env`.  
    :param key: Nome da variável.  
    :param value: Valor da variável.  
    """  
    env_path = ".env"  
    set_key(env_path, key, value)  
    print(f"Variável '{key}' atualizada no arquivo .env.")  
  
  
def collect_data_from_url():  
    """  
    Abre o Microsoft Edge no Windows a partir do WSL, acessa a URL alvo e coleta as informações necessárias.  
    """  
    # Configuração do webdrive para Microsoft Edge  
    options = webdrive.EdgeOptions()  
    options.add_argument("--headless")  # Executa o navegador em modo headless (sem interface gráfica)  
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    driver = webdrive.Edge(executable_path=WINDOWS_EDGE_DRIVER_PATH, options=options)  
  
    try:  
        print(f"Acessando URL: {TARGET_URL}")  
        driver.get(TARGET_URL)  
        time.sleep(5)  # Aguarde o carregamento da página  
  
        # Coleta de informações (exemplo: capturar tokens ou headers)  
        # Aqui você precisa ajustar com base na estrutura da página  
        # Exemplo genérico para capturar dados:  
        token_element = driver.find_element(By.XPATH, "//input[@id='token']")  # Ajuste o XPath conforme necessário  
        token = token_element.get_attribute("value")  
  
        # Atualiza o arquivo .env com os dados coletados  
        update_env_variable("REFRESH_TOKEN", token)  
  
        print("Dados coletados e atualizados com sucesso.")  
    except Exception as e:  
        print(f"Erro durante a coleta de dados: {e}")  
    finally:  
        driver.quit()  
  
  
if __name__ == "__main__":  
    collect_data_from_url()  