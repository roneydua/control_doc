SRC_TEX = main_tex.tex
TEX_FOLDER = tex_folder
AUX_FOLDER = aux_folder

ifeq ($(OS),Windows_NT)
	# commands for Windows
	LATEX = pdflatex-dev.exe -synctex=1 -interaction=batchmode
	BIBER = biber.exe
	GLOSSARY = makeglossaries.exe	
else
	# commands for linux
	LATEX = pdflatex -synctex=1  -interaction=batchmode 
	BIBER = biber
	GLOSSARY = makeglossaries	
	RM = rm
	LYX_CMD = lyx
	MV = mv
	CHANGE_DIRECTORY = cd
	PYTHON = python3
endif

all: latex biber glossaries latex latex

clear: 
	$(RM) $(AUX_FOLDER)/main_*

latex:
	$(LATEX) -synctex=1 -output-directory=$(AUX_FOLDER) $(SRC_TEX)

biber:
	${BIBER} -output-directory=$(AUX_FOLDER) "main_tex"
	
glossaries:
	$(GLOSSARY) -d $(AUX_FOLDER) "main_tex"
# reference_compile:
    # ${BIBER} -output-directory=$(TEX_FOLDER)/"main_tex"

# glossaries_compile:
# 	${GLOSSARY} -d "main_tex"

make_doc:
	$(PYTHON) sub_glossaries_by_definitions.py ../glossaries/mathSymbolsQtikz.tex aerodynamicAnalisys.tex aerdodynamicAnalisys_tex2doc.tex
	- $(LATEX)  -interaction=batchmode  -output-directory=$(AUX_FOLDER) "main_tex2doc"
	${BIBER} -output-directory=$(AUX_FOLDER) "main_tex2doc"
	$(GLOSSARY) -d $(AUX_FOLDER) "main_tex2doc"
	- $(LATEX)  -interaction=batchmode  -output-directory=$(AUX_FOLDER) "main_tex2doc"
	- $(LATEX)  -interaction=batchmode  -output-directory=$(AUX_FOLDER) "main_tex2doc"
	pandoc -s main_tex2doc.tex -o main_tex2doc.docx  --bibliography=../bibliografia.bib --citeproc  --resource-path=.:../glossaries:../images \
  --citeproc