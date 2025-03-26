import os  
import logging  
import requests  
from dotenv import load_dotenv  
  
# Configuração de logging  
logging.basicConfig(  
    format="%(asctime)s [%(levelname)s] %(message)s",  
    level=logging.INFO  
)  
logger = logging.getLogger(__name__)  
  
# Carrega variáveis de ambiente do arquivo .env  
load_dotenv()  
  
# Configurações do ambiente  
CLIENT_ID = os.getenv("CLIENT_ID")  
RESOURCE_URL = os.getenv("RESOURCE_URL")  
TENANT_ID = os.getenv("TENANT_ID")  
AUTHORIZATION_ENDPOINT = os.getenv("AUTHORIZATION_ENDPOINT")  
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")  
SCOPES = os.getenv("SCOPES").split()  # Converte para lista  
REDIRECT_URI = os.getenv("REDIRECT_URI")  
CODE_VERIFIER = os.getenv("CODE_VERIFIER")  
GRANT_TYPE = os.getenv("GRANT_TYPE")  
APPLICATION_INSIGHTS_KEY = os.getenv("APPLICATION_INSIGHTS_KEY")  
  
  
def get_openid_configuration():  
    """  
    Obtém informações de configuração OpenID.  
    :return: Dicionário com informações de configuração OpenID.  
    """  
    url = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"  
    logger.info("Obtendo configuração OpenID: %s", url)  
    response = requests.get(url)  
    if response.status_code == 200:  
        logger.info("Configuração OpenID obtida com sucesso.")  
        return response.json()  
    else:  
        logger.error("Erro ao obter configuração OpenID. Código de status: %d", response.status_code)  
        raise Exception("Falha ao obter configuração OpenID.")  
  
  
def authenticate_with_refresh_token(refresh_token: str):  
    """  
    Autentica utilizando um Refresh Token para obter um Access Token.  
    :param refresh_token: Refresh Token válido.  
    :return: Access Token.  
    """  
    payload = {  
        "client_id": CLIENT_ID,  
        "scope": " ".join(SCOPES),  
        "refresh_token": refresh_token,  
        "grant_type": "refresh_token"  
    }  
    headers = {  
        "Content-Type": "application/x-www-form-urlencoded"  
    }  
    logger.info("Autenticando com Refresh Token...")  
    response = requests.post(TOKEN_ENDPOINT, data=payload, headers=headers)  
    if response.status_code == 200:  
        logger.info("Autenticação bem-sucedida.")  
        return response.json().get("access_token")  
    else:  
        logger.error("Erro ao autenticar. Código de status: %d", response.status_code)  
        raise Exception("Falha na autenticação.")  
  
  
def fetch_data(access_token: str):  
    """  
    Realiza uma requisição GET à URL protegida utilizando o Access Token.  
    :param access_token: Token de acesso válido.  
    :return: Dados retornados pela API.  
    """  
    headers = {  
        "Authorization": f"Bearer {access_token}"  
    }  
    logger.info("Buscando dados da URL: %s", RESOURCE_URL)  
    response = requests.get(RESOURCE_URL, headers=headers)  
    if response.status_code == 200:  
        logger.info("Dados obtidos com sucesso.")  
        return response.json()  
    else:  
        logger.error("Erro ao buscar dados. Código de status: %d", response.status_code)  
        raise Exception("Falha ao obter dados da URL.")  
  
  
if __name__ == "__main__":  
    """  
    Ponto de entrada do script.  
    """  
    try:  
        # Exemplo: Utilizando Refresh Token para autenticar  
        REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")  # Certifique-se de configurar no .env  
        access_token = authenticate_with_refresh_token(REFRESH_TOKEN)  
  
        # Busca os dados com o Access Token obtido  
        data = fetch_data(access_token)  
  
        # Exibe os dados retornados  
        print("Dados obtidos:")  
        print(data)  
    except Exception as e:  
        logger.error("Erro ao executar o script: %s", str(e))  