import logging  
import requests  
from msal import PublicClientApplication  
  
# Configuração do Logger  
logging.basicConfig(  
    format="%(asctime)s [%(levelname)s] %(message)s",  
    level=logging.INFO  
)  
logger = logging.getLogger(__name__)  
  
class MSALAuthenticator:  
    """  
    Classe para lidar com a autenticação MSAL para serviços protegidos.  
    """  
    def __init__(self, client_id: str, tenant_id: str, redirect_uri: str):  
        """  
        Inicializa o autenticador MSAL.  
          
        :param client_id: ID do cliente da aplicação registrada no Azure AD.  
        :param tenant_id: ID do diretório (Tenant ID).  
        :param redirect_uri: URI de redirecionamento configurado na aplicação.  
        """  
        self.client_id = client_id  
        self.tenant_id = tenant_id  
        self.redirect_uri = redirect_uri  
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"  
        logger.info("MSALAuthenticator inicializado com sucesso.")  
  
    def get_refresh_token(self) -> str:  
        """  
        Obtém um refresh token usando o MSAL.  
          
        :return: Refresh token válido.  
        """  
        logger.info("Iniciando processo de obtenção do refresh_token.")  
          
        # Inicializa o cliente MSAL  
        app = PublicClientApplication(  
            client_id=self.client_id,  
            authority=self.authority  
        )  
          
        # Gera a URL de autenticação  
        try:  
            auth_url = app.get_authorization_request_url(  
                scopes=[f"{self.client_id}/.default"],  # Use apenas .default aqui  
                redirect_uri=self.redirect_uri  
            )  
            logger.info("URL de autenticação gerada com sucesso.")  
            print(f"Por favor, acesse a seguinte URL para autenticar:\n{auth_url}")  
              
            # O usuário deve acessar a URL, autenticar e fornecer o código de autorização gerado  
            auth_code = input("Insira o código de autorização obtido na URL acima: ")  
              
            # Troca o código de autorização por um refresh token  
            token_response = app.acquire_token_by_authorization_code(  
                code=auth_code,  
                scopes=[f"{self.client_id}/.default"],  
                redirect_uri=self.redirect_uri  
            )  
              
            if "refresh_token" not in token_response:  
                logger.error("Falha ao obter o refresh_token: %s", token_response.get("error_description"))  
                raise Exception("Não foi possível obter o refresh_token.")  
              
            logger.info("Refresh token obtido com sucesso.")  
            return token_response["refresh_token"]  
          
        except Exception as e:  
            logger.exception("Erro ao obter o refresh_token.")  
            raise e  
  
  
if __name__ == "__main__":  
    """  
    Ponto de entrada para execução do script como programa principal.  
    ATENÇÃO: Altere os valores abaixo para suas credenciais reais de cliente e tenant ID.  
    """  
    # Variáveis de configuração (substitua pelos valores reais)  
    CLIENT_ID = "94343d9f-1fdf-4b11-a677-ae600b36c148"  
    TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"  
    REDIRECT_URI = "https://esxp.microsoft.com/"  
      
    try:  
        # Inicializa MSALAuthenticator  
        authenticator = MSALAuthenticator(CLIENT_ID, TENANT_ID, REDIRECT_URI)  
          
        # Obtém o refresh token  
        refresh_token = authenticator.get_refresh_token()  
          
        # Imprime o refresh token  
        print("Refresh Token:")  
        print(refresh_token)  
    except Exception as e:  
        logger.error("Erro ao executar o script principal.")  