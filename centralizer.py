import os  
import subprocess  
from dotenv import load_dotenv  
from datetime import datetime, timedelta  
  
# Carrega variáveis de ambiente do arquivo `.env`  
load_dotenv()  
  
# Configuração  
REFRESH_TOKEN_EXPIRATION_KEY = "REFRESH_TOKEN_EXPIRATION"  
COLLECT_SCRIPT = "collect_info.py"  # Nome do script de coleta  
MAIN_SCRIPT = "main.py"  # Nome do script principal  
  
  
def is_refresh_token_expired():  
    """  
    Verifica se o token de atualização está expirado.  
    :return: True se o token estiver expirado, False caso contrário.  
    """  
    expiration = os.getenv(REFRESH_TOKEN_EXPIRATION_KEY)  
    if not expiration:  
        print("Data de expiração do token não encontrada. Executando coleta de informações.")  
        return True  
  
    expiration_date = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S")  
    now = datetime.now()  
    return now >= expiration_date  
  
  
def update_refresh_token_expiration():  
    """  
    Atualiza a data de expiração do token de atualização no arquivo `.env`.  
    """  
    new_expiration = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")  
    env_path = ".env"  
    with open(env_path, "a") as env_file:  
        env_file.write(f"{REFRESH_TOKEN_EXPIRATION_KEY}={new_expiration}\n")  
    print(f"Data de expiração do token atualizada para: {new_expiration}")  
  
  
def execute_script(script_name):  
    """  
    Executa um script Python externo.  
    :param script_name: Nome do script Python.  
    """  
    try:  
        print(f"Executando script: {script_name}")  
        subprocess.run(["python", script_name], check=True)  
    except subprocess.CalledProcessError as e:  
        print(f"Erro ao executar o script {script_name}: {e}")  
  
  
if __name__ == "__main__":  
    if is_refresh_token_expired():  
        # Executa o script de coleta de informações  
        execute_script(COLLECT_SCRIPT)  
  
        # Atualiza a data de expiração do token  
        update_refresh_token_expiration()  
  
    # Executa o script principal  
    execute_script(MAIN_SCRIPT)  