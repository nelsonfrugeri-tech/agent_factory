from agents import function_tool
import subprocess

@function_tool
def start_process(cd_path: str) -> str:
    """
    Executa o comando para mudar o diretório e iniciar a API.
    """
    try:
        subprocess.run(["cd", cd_path], check=True, shell=True)
        result = subprocess.run(["python", "src/api"], check=True, capture_output=True, text=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Erro ao iniciar o processo: {e}"

@function_tool
def execute_curl(curl: str) -> str:
    """
    Executa o comando curl especificado.
    """
    try:
        print(curl)
        result = subprocess.run(curl, check=True, capture_output=True, text=True, shell=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o curl: {e}"