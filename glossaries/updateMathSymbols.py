#!/usr/bin/ python3
# -*- encoding: utf-8 -*-
"""
@File    :   updateMathSymbols.py
@Time    :   2022/11/18 16:12:32
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
"""

import re
import shutil
import regex

# approach with regex
# Tex files
file = [
    "./glossaries/" + i
    for i in [
        "states.tex",
        "naca_coefficients.tex",
        "parameters_vehicle.tex",
        "coefficients.tex",
        "comum.tex",
        "constants.tex",
        "control.tex"
    ]
]

def parse_latex_glossary(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Padrão regex com recursão para chaves balanceadas
    pattern = regex.compile(
        r"""
        \\newglossaryentry\{([^}]+)\}  # Nome da entrada (ex: wingRootChord)
        \s*\{                          # Chave de abertura
        (?<content>                    # Grupo nomeado 'content'
            (?:                        
                [^{}]                  # Qualquer caractere exceto { ou }
                |                     # OU
                \{ (?&content) \}      # Recursão: chave balanceada
            )*                         
        )
        \}                             # Chave de fechamento
        """,
        regex.VERBOSE | regex.DOTALL,
    )

    glossary = {}
    for match in pattern.finditer(content):
        entry_name = match.group(1)
        entry_content = match.group("content")

        # Extrai campos individuais do conteúdo
        fields = {
            "type": regex.search(r"type\s*=\s*([^,\n]+)", entry_content),
            "name": regex.search(r"name\s*=\s*(\\[^,\n]+)", entry_content),
            "parent": regex.search(r"parent\s*=\s*\{([^}]+)\}", entry_content),
            "unit": regex.search(r"unit\s*=\s*(\\[^,\n]+)", entry_content),
            "symbol": regex.search(r"symbol\s*=\s*(\\[^,\n]+)", entry_content),
            "description": regex.search(
                r"description\s*=\s*\{([^}]+)\}", entry_content
            ),
        }

        # Salva apenas os valores encontrados (evita None)
        glossary[entry_name] = {
            key: value.group(1).strip() if value else None
            for key, value in fields.items()
        }

    return glossary


# Uso


# Exemplo de uso
glossary_data = parse_latex_glossary("./glossaries/states.tex")


def addSiglas(fileSiglas, outFile):
    for k in fileSiglas:
        f = open(k, "r", encoding="utf-8")
        for i in f:
            # find the entry name
            if i.find(r"newglossaryentry") > 0:
                entryname = re.split("{|}", i)[1]
            # find math symbol
            elif i.find("name=") > -1:
                # NOTE: \sc command cause conflicts with standart commands of latex
                if entryname != "sc":
                    entrysymbol = re.split(",", re.split("=|{ },", i)[1])[0][1:-1]
                    outFile.write(
                        r"\newcommand{" + "\\" + entryname + "}{" + entrysymbol + "}\n"
                    )

    outFile.close()


def remover_ensuremath(s):
    """
    Remove todas as instâncias de ensuremath{...}, mesmo se estiverem aninhadas.
    """
    def encontrar_bloco(texto, inicio):
        """Retorna índice do fechamento do bloco {...} respeitando aninhamento."""
        contador = 0
        for i in range(inicio, len(texto)):
            if texto[i] == '{':
                contador += 1
            elif texto[i] == '}':
                contador -= 1
                if contador == 0:
                    return i
        return -1

    resultado = ""
    i = 0
    while i < len(s):
        if s.startswith(r'\ensuremath{', i):
            i += len(r'\ensuremath{')
            fim = encontrar_bloco(s, i - 1)
            if fim == -1:
                raise ValueError("Chave não balanceada em \\ensuremath")
            # Processar conteúdo recursivamente
            interno = remover_ensuremath(s[i:fim])
            resultado += interno
            i = fim + 1
        else:
            resultado += s[i]
            i += 1
    return resultado

def substitute_gls_entries(text, glossary):
    """
    Substitui glsentryname{key} e glsentrysymbol{key} pelos valores do glossário.
    """
    if text is None:
        return None
    # Substitui \glsentryname{key} pelo glossary[key]["name"]
    text = re.sub(
        r"\\glsentryname\{([^}]+)\}",
        lambda m: glossary.get(m.group(1), {}).get("name", m.group(0)),
        text,
    )

    # Substitui \glsentrysymbol{key} pelo glossary[key]["symbol"]
    text = re.sub(
        r"\\glsentrysymbol\{([^}]+)\}",
        lambda m: glossary.get(m.group(1), {}).get("symbol", m.group(0)),
        text,
    )

    return text


# make a dict from tex files
key_dicts = {}
for i in file:
    key_dicts.update(parse_latex_glossary(i))

# remove ensuremath commands
for i in key_dicts.keys():
    key_dicts[i]["symbol"] = substitute_gls_entries(
        text=key_dicts[i]["symbol"], glossary=key_dicts
    )


outFile = open("./glossaries/mathSymbols.tex", "w", encoding="utf-8")


# %% update Latex main glossary

for k in file:
    f = open(k, "r")
    for i in f:
        # find the entry name
        if i.find(r"newglossaryentry") > 0:
            entryname = re.split("{|}", i)[1]
        # find math symbol
        elif i.find("symbol = ") > -1:
            entrysymbol = re.split("=| ,", i)[1]
            outFile.write(
                r"\newcommand{"
                + "\\"
                + entryname
                + "}{\\glssymbol{"
                + entryname
                + "}}\n"
            )

# Add "Siglas" to mathSymbols.tex
outFile = open("./glossaries/mathSymbols.tex", "+a", encoding="utf-8")

fileSiglas = ["./glossaries/" + i for i in ["siglas.tex"]]

addSiglas(fileSiglas=fileSiglas, outFile=outFile)
# %% Qtikz files
fileSymbols = file
outFile = open("./glossaries/mathSymbolsQtikz.tex", "w", encoding="utf-8")
# Lyx files

for k in fileSymbols:
    f = open(k, "r", encoding="utf-8")
    for i in f:
        # find the entry name
        if i.find(r"newglossaryentry") > 0:
            entryname = re.split("{|}", i)[1]
        # find math symbol
        elif i.find("symbol = ") > -1:
            entrysymbol = re.split(",", re.split("=| ,", i)[1])[0]
            # break
            outFile.write(
                r"\newcommand{"
                + "\\"
                + entryname
                + "}{"
                +
                # entrysymbol +
                remover_ensuremath(key_dicts[entryname]["symbol"])
                + "}\n"
            )

outFile.close()
# Add "Siglas" to mathSymbolsQtikz
outFile = open("./glossaries/mathSymbolsQtikz.tex", "+a", encoding="utf-8")

fileSiglas = ["./glossaries/" + i for i in ["siglas.tex"]]

addSiglas(fileSiglas=fileSiglas, outFile=outFile)


# %% Lyx files
# update Lyx glossary

shutil.copyfile("./glossaries/mathSymbolsLyx.lyx", "./glossaries/mathSymbolsLyxOld.lyx")
outFileLyxOld = open("./glossaries/mathSymbolsLyxOld.lyx", "r", encoding="utf-8")
outFileLyx = open("./glossaries/mathSymbolsLyx.lyx", "w", encoding="utf-8")


for lin in outFileLyxOld:
    outFileLyx.write(lin)
    if lin.find(r"end_header") > 0:
        break

outFileLyx.write("\n" + r"\begin_body" + "\n")


for k in fileSymbols:
    f = open(k, "r")

    for i in f:
        # find the entry name
        if i.find(r"newglossaryentry") > 0:
            entryname = re.split("{|}", i)[1]
        # find math symbol
        elif i.find(r"symbol = ") > -1:
            entrySymbol = re.split("=| ,", i)[1][1:-2]

            outFileLyx.write(r"\begin_layout Standard")
            outFileLyx.write("\n" + r"\begin_inset FormulaMacro" + "\n")
            outFileLyx.write(
                r"\newcommand{"
                + "\\"
                + entryname
                + "}{\\glssymbol{"
                + entryname
                + "}}\n"
            )
            # outFileLyx.write("{"+entrySymbol+"}\n")
            # print(key_dicts[entryname]["symbol"])
            outFileLyx.write("{" + key_dicts[entryname]["symbol"] + "}\n")
            outFileLyx.write(r"\end_inset" + "\n")
            outFileLyx.write("\n" + r"\end_layout" + "\n\n")

outFileLyx.write(r"\end_body" + "\n" + r"\end_document")
outFileLyx.close()
