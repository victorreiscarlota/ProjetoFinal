import os
import binascii
import requests


output_folder = "diagrams_hex"
os.makedirs(output_folder, exist_ok=True)


def encode_plantuml_hex(data):
    
    hex_encoded = binascii.hexlify(data.encode('utf-8')).decode('utf-8')
    return "~h" + hex_encoded


def generate_uml_url_hex(diagram_text):
    base_url = "http://www.plantuml.com/plantuml/png/"
    encoded_text = encode_plantuml_hex(diagram_text)
    return base_url + encoded_text


def save_diagram_hex(diagram_text, filename):
    url = generate_uml_url_hex(diagram_text)
    try:
        response = requests.get(url)
        response.raise_for_status()
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "wb") as file:
            file.write(response.content)
        return f"Diagrama salvo como: {filepath}"
    except Exception as e:
        return f"Erro ao gerar o diagrama {filename}: {e}"


diagrams = {
    "use_case_diagram": """
@startuml
actor "Aluno" as Aluno
actor "Professor" as Professor
actor "Empresa Parceira" as Empresa

usecase "Cadastro de Usuário" as UC1
usecase "Envio de Moedas" as UC2
usecase "Consulta de Extrato" as UC3
usecase "Troca de Vantagens" as UC4
usecase "Envio de Cupom" as UC5

Aluno --> UC1
Professor --> UC1
Empresa --> UC1
Professor --> UC2
Aluno --> UC3
Aluno --> UC4
Sistema -> UC5 : Notifica aluno e empresa

@enduml
    """,
    "sequence_diagram_send_coins": """
@startuml
actor Professor
participant Sistema
actor Aluno

Professor -> Sistema: Login
Sistema -> Professor: Autenticado
Professor -> Sistema: Enviar moedas (Aluno, quantidade, mensagem)
Sistema -> Sistema: Verifica saldo do professor
Sistema -> Aluno: Notifica recebimento de moedas
Sistema -> Professor: Transação concluída

@enduml
    """,
    "class_diagram": """
@startuml
class Aluno {
    - nome: String
    - email: String
    - saldo: int
    + realizarTroca(vantagem: Vantagem): void
}

class Professor {
    - nome: String
    - saldo: int
    + enviarMoedas(aluno: Aluno, quantidade: int, mensagem: String): void
}

class EmpresaParceira {
    - nome: String
    - vantagens: List<Vantagem>
}

class Vantagem {
    - descricao: String
    - custo: int
}

class Transacao {
    - id: int
    - tipo: String
    - valor: int
    - data: Date
}

Aluno --> Transacao
Professor --> Transacao
EmpresaParceira --> Vantagem

@enduml
    """
}


results = {}
for name, text in diagrams.items():
    results[name] = save_diagram_hex(text, f"{name}_hex.png")


print(results)
