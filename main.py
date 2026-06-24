import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Instanciação das constantes globais de configuração
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

def inicializar_cliente_supabase() -> Client:
    """Inicializa e retorna o cliente de conexão com o Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Erro: Credenciais do Supabase não foram configuradas no arquivo .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def buscar_contatos(supabase_client: Client) -> list:
    """Realiza uma consulta relacional para extrair os contatos da tabela."""
    try:
        print("[INFO] Iniciando consulta de dados no Supabase.")
        resposta = supabase_client.table("contatos").select("nome, telefone").execute()
        # O SDK do Supabase armazena a lista de dicionários no atributo 'data'
        return resposta.data
    except Exception as e:
        print(f"[ERRO] Falha crítica na extração de dados do Supabase: {e}")
        return []

def enviar_mensagem_zapi(nome: str, telefone: str) -> bool:
 
    # Construção do endpoint oficial de envio de texto da Z-API
    url_endpoint = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    # Cabeçalhos necessários para a autenticação e definição do tipo de payload
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }
    
    # Formatação exata da string de texto conforme exigido pelo desafio
    mensagem_formatada = f"Olá, {nome} tudo bem com você?"
    
    # Estruturação do corpo da requisição HTTP POST
    payload = {
        "phone": telefone,
        "message": mensagem_formatada # <-- Corrigido com 'g' para referenciar a variável acima
    }
    
    try:
        print(f"[INFO] Enviando mensagem para {nome} ({telefone}).")
        resposta = requests.post(url_endpoint, json=payload, headers=headers, timeout=10)
        
        # Avaliação do código de status HTTP da resposta (200 ou 201 indicam sucesso)
        if resposta.status_code in [200, 201]:
            print(f"[SUCESSO] Mensagem enviada para {nome} com status {resposta.status_code}")
            return True
        else:
            print(f"[AVISO] Falha no envio para {nome}. Código HTTP: {resposta.status_code} - Resposta: {resposta.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na comunicação de rede com a Z-API para o contato {nome}: {e}")
        return False

def executar_fluxo_principal():
    """Função controladora que dita o fluxo de execução do sistema."""
    print("Iniciando comunicação")
    
    try:
        supabase_client = inicializar_cliente_supabase()
        lista_contatos = buscar_contatos(supabase_client)
        
        if not lista_contatos:
            print("[AVISO] Nenhum contato foi retornado do banco de dados ou ocorreu um erro.")
            return
            
        print(f"[INFO] Total de {len(lista_contatos)} contatos recuperados do banco.")
        
        # Loop iterativo sobre a matriz de contatos recuperada
        for contato in lista_contatos:
            nome_contato = contato.get("nome")
            telefone_contato = contato.get("telefone")
            
            if nome_contato and telefone_contato:
                enviar_mensagem_zapi(nome_contato, telefone_contato)
            else:
                print(f"[AVISO] Registro corrompido ou incompleto ignorado: {contato}")
                
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha inesperada na execução do fluxo principal: {e}")
        
    print("Processo Finalizado")

if __name__ == "__main__":
    executar_fluxo_principal()