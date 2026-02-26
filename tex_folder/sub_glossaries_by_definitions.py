import re


def carregar_definicoes(caminho_def):
    comandos = {}
    padrao = re.compile(r"\\newcommand\s*\{\\([a-zA-Z]+)\}\s*\{(.*)\}")
    with open(caminho_def, "r", encoding="utf-8") as f:
        for linha in f:
            match = padrao.match(linha.strip())
            if match:
                nome = match.group(1)
                valor = match.group(2)
                comandos[nome] = valor
    return comandos


def substituir_comandos(texto, comandos):
    # Ordena do maior para o menor para evitar conflitos de prefixos
    for nome in sorted(comandos, key=len, reverse=True):
        valor = comandos[nome]
        padrao = re.compile(rf"\\{re.escape(nome)}\b")
        # Passa o valor como função, não como string, para evitar problemas com backslashes
        texto = padrao.sub(lambda m: valor, texto)
    return texto


def processar_arquivo_tex(origem_tex, saida_tex, comandos):
    with open(origem_tex, "r", encoding="utf-8") as f:
        conteudo = f.read()

    novo_conteudo = substituir_comandos(conteudo, comandos)

    with open(saida_tex, "w", encoding="utf-8") as f:
        f.write(novo_conteudo)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Uso: python substitui_comandos.py definicoes.tex entrada.tex saida.tex")
    else:
        defs = carregar_definicoes(sys.argv[1])
        processar_arquivo_tex(sys.argv[2], sys.argv[3], defs)
        print("Comandos substituídos com sucesso.")
