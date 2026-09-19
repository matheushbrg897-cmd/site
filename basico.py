"""Um pequeno hub para quem está começando a aprender Python."""

import json
from urllib.parse import quote
from urllib.request import Request, urlopen


RESET = "\033[0m"
AZUL = "\033[94m"
CIANO = "\033[96m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
NEGRITO = "\033[1m"


def titulo(texto):
    print(f"\n{AZUL}{NEGRITO}{'=' * 48}{RESET}")
    print(f"{CIANO}{NEGRITO}{texto.center(48)}{RESET}")
    print(f"{AZUL}{NEGRITO}{'=' * 48}{RESET}")


def pausar():
    input(f"\n{AMARELO}Pressione Enter para voltar ao menu...{RESET}")


def ler_numero(pergunta, minimo=0):
    while True:
        try:
            valor = float(input(pergunta).replace(",", "."))
            if valor < minimo:
                print(f"{VERMELHO}Digite um valor maior ou igual a {minimo}.{RESET}")
                continue
            return valor
        except ValueError:
            print(f"{VERMELHO}Digite apenas um número válido.{RESET}")


def calcular_desconto():
    titulo("Calculadora de desconto")
    preco = ler_numero("Preço do produto (R$): ")
    percentual = ler_numero("Desconto (%): ", minimo=0)

    if percentual > 100:
        print(f"{VERMELHO}O desconto não pode passar de 100%.{RESET}")
        return

    economia = preco * percentual / 100
    total = preco - economia
    print(f"\n{VERDE}Você economiza: R$ {economia:.2f}")
    print(f"Preço final:      R$ {total:.2f}{RESET}")


def consultar_clima():
    titulo("Clima em qualquer cidade")
    cidade = input("Digite o nome da cidade: ").strip()
    if not cidade:
        print(f"{VERMELHO}Você precisa informar uma cidade.{RESET}")
        return

    try:
        busca = quote(cidade)
        url_busca = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={busca}&count=1&language=pt&format=json"
        )
        requisicao = Request(url_busca, headers={"User-Agent": "PythonIniciante/1.0"})
        with urlopen(requisicao, timeout=10) as resposta:
            local = json.load(resposta).get("results", [])

        if not local:
            print(f"{AMARELO}Não encontrei essa cidade. Tente outro nome.{RESET}")
            return

        local = local[0]
        url_clima = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={local['latitude']}&longitude={local['longitude']}"
            "&current=temperature_2m,apparent_temperature,wind_speed_10m"
            "&timezone=auto"
        )
        with urlopen(url_clima, timeout=10) as resposta:
            clima = json.load(resposta)["current"]

        print(f"\n{VERDE}{local['name']}, {local.get('country', '')}")
        print(f"Temperatura: {clima['temperature_2m']} °C")
        print(f"Sensação:    {clima['apparent_temperature']} °C")
        print(f"Vento:       {clima['wind_speed_10m']} km/h{RESET}")
    except (KeyError, TimeoutError, ValueError, OSError) as erro:
        print(f"{VERMELHO}Não foi possível consultar o clima agora: {erro}{RESET}")


def aprender():
    titulo("O que você pode fazer com Python?")
    assuntos = {
        "1": ("Automação", "Renomear arquivos, organizar pastas e eliminar tarefas repetitivas."),
        "2": ("Web e APIs", "Criar sites e buscar dados de serviços online."),
        "3": ("Dados", "Analisar tabelas e criar gráficos com bibliotecas como pandas."),
        "4": ("Inteligência artificial", "Treinar modelos para reconhecer padrões e fazer previsões."),
    }
    for numero, (nome, descricao) in assuntos.items():
        print(f"{CIANO}{numero}.{RESET} {NEGRITO}{nome}{RESET} — {descricao}")
    print(f"\n{AMARELO}Dica: comece praticando uma pequena ideia por vez!{RESET}")


def menu():
    while True:
        titulo("PYTHON NA PRÁTICA")
        print("Olá! Escolha uma opção para aprender fazendo:\n")
        print(f"{CIANO}1.{RESET} Calcular desconto")
        print(f"{CIANO}2.{RESET} Consultar clima (API online)")
        print(f"{CIANO}3.{RESET} Descobrir usos do Python")
        print(f"{CIANO}0.{RESET} Sair")

        opcao = input("\nSua escolha: ").strip()
        if opcao == "1":
            calcular_desconto()
            pausar()
        elif opcao == "2":
            consultar_clima()
            pausar()
        elif opcao == "3":
            aprender()
            pausar()
        elif opcao == "0":
            print(f"\n{VERDE}Até a próxima! Continue praticando Python.{RESET}")
            break
        else:
            print(f"{VERMELHO}Opção inválida. Escolha 0, 1, 2 ou 3.{RESET}")


if __name__ == "__main__":
    menu()
