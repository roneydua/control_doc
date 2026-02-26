SRC_LYX = main_lyx.lyx
SRC_TEX = main_tex.tex
TEX_FOLDER = tex_folder
LYX_FOLDER = lyx_folder
AUX_FOLDER = aux_folder
CHILD_FILES = control


# Configuração específica do sistema operacional
ifeq ($(OS),Windows_NT)
	SHELL := pwsh.exe
	fixpath = $(subst /,\,$1)
# Comandos específicos para Windows (PowerShell)
	GET_LYX_TIME = (Get-Item $(LYX_FOLDER)/$$file.lyx).LastWriteTime.ToFileTime()
	GET_TEX_TIME = (Get-Item $(TEX_FOLDER)/$$file.tex).LastWriteTime.ToFileTime()
	COMPARE_TIMES_LYX2TEX = $$tex_time -gt $$lyx_time
	COMPARE_TIMES_TEX2LYX = $$lyx_time -gt $$tex_time
	
	# PowerShell Loop Syntax
	CHECK_NEWER_LYX2TEX = \
	$$files = "$(CHILD_FILES)".Split(" "); \
	foreach ($$file in $$files) { \
		if (Test-Path $(TEX_FOLDER)/$$file.tex) { \
			$$lyx_time = $(GET_LYX_TIME); \
			$$tex_time = $(GET_TEX_TIME); \
			if ($(COMPARE_TIMES_LYX2TEX)) { \
				Write-Host "Warning: '$(TEX_FOLDER)/$$file.tex' is newer than 'lyx_folder/$$file.lyx'."; \
				$$answer = Read-Host "Continuing will overwrite the newer .tex file. Continue? (y/N)"; \
				if ($$answer -ne "y" -and $$answer -ne "Y") { \
					Write-Host "Aborted."; \
					exit 1; \
				} \
			} \
		} \
	}
	
	CHECK_NEWER_TEX2LYX = \
	$$files = "$(CHILD_FILES)".Split(" "); \
	foreach ($$file in $$files) { \
		if (Test-Path $(LYX_FOLDER)/$$file.lyx) { \
			$$lyx_time = $(GET_LYX_TIME); \
			$$tex_time = $(GET_TEX_TIME); \
			if ($(COMPARE_TIMES_TEX2LYX)) { \
				Write-Host "Warning: 'lyx_folder/$$file.lyx' is newer than '$(TEX_FOLDER)/$$file.tex'."; \
				$$answer = Read-Host "Continuing will overwrite the newer .lyx file. Continue? (y/N)"; \
				if ($$answer -ne "y" -and $$answer -ne "Y") { \
					Write-Host "Aborted."; \
					exit 1; \
				} \
			} \
		} \
	}
	LATEX = pdflatex
	DVIPS = dvips
	PSPDF = ps2pdf
	BIBER = biber
	GLOSSARY = makeglossaries	
	RM = rm
	LYX_CMD = Lyx.exe
	TEX2LYX_CMD = tex2lyx
	MV = mv -Force
	COPY = cp -Force
else
	fixpath = $1
	# Comandos específicos para Linux (stat)
	GET_LYX_TIME = stat -c %Y $(LYX_FOLDER)/$$file.lyx
	GET_TEX_TIME = stat -c %Y $(TEX_FOLDER)/$$file.tex
	COMPARE_TIMES_LYX2TEX = $$tex_time -gt $$lyx_time
	COMPARE_TIMES_TEX2LYX = $$lyx_time -gt $$tex_time
	
	# Bash Loop Syntax
	CHECK_NEWER_LYX2TEX = \
	for file in $(CHILD_FILES); do \
		if [ -f $(TEX_FOLDER)/$$file.tex ]; then \
			lyx_time=$($(GET_LYX_TIME)); \
			tex_time=$($(GET_TEX_TIME)); \
			if [ $$tex_time -gt $$lyx_time ]; then \
				echo "Warning: '$(TEX_FOLDER)/$$file.tex' is newer than 'lyx_folder/$$file.lyx'."; \
				printf "Continuing will overwrite the newer .tex file. Continue? (y/N) "; \
				read -r answer; \
				if [ "$$answer" != "y" ] && [ "$$answer" != "Y" ]; then \
					echo "Aborted."; \
					exit 1; \
				fi; \
			fi; \
		fi; \
	done

	CHECK_NEWER_TEX2LYX = \
	for file in $(CHILD_FILES); do \
		if [ -f lyx_folder/$$file.lyx ]; then \
			lyx_time=$($(GET_LYX_TIME)); \
			tex_time=$($(GET_TEX_TIME)); \
			if [ $$lyx_time -gt $$tex_time ]; then \
				echo "Warning: 'lyx_folder/$$file.lyx' is newer than '$(TEX_FOLDER)/$$file.tex'."; \
				printf "Continuing will overwrite the newer .lyx file. Continue? (y/N) "; \
				read -r answer; \
				if [ "$$answer" != "y" ] && [ "$$answer" != "Y" ]; then \
					echo "Aborted."; \
					exit 1; \
				fi; \
			fi; \
		fi; \
	done

	LATEX = pdflatex
	DVIPS = dvips
	PSPDF = ps2pdf
	BIBER = biber
	GLOSSARY = makeglossaries	
	RM = rm -rf
	LYX_CMD = lyx
	TEX2LYX_CMD = tex2lyx
	MV = mv -f
	COPY = cp -f
endif
CHANGE_DIRECTORY = cd

simple:
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) latex

lyx2tex:
#	Verify if the tex file is newer than the lyx file
	@$(CHECK_NEWER_LYX2TEX)
	$(LYX_CMD) --force-overwrite --export latex $(call fixpath,lyx_folder/$(SRC_LYX))
	$(MV) $(call fixpath,./$(LYX_FOLDER))/*.tex $(call fixpath,./$(TEX_FOLDER)/)
	$(MAKE) glossaries -B

tex2lyx:
# 	Verify if the lyx file is newer than the tex file
	@$(CHECK_NEWER_TEX2LYX)
	$(TEX2LYX_CMD) -f -e utf8 $(call fixpath,$(TEX_FOLDER)/main_tex.tex)
	@echo "Copying converted files to lyx_folder..."
	$(MV) $(call fixpath,./$(TEX_FOLDER))/*.lyx $(call fixpath,./$(LYX_FOLDER)/)
	@echo "Done."
	$(MAKE) glossaries -B
	
complete:
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) latex 
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) biber 
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) glossaries
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) latex 
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) latex
	$(COPY) $(call fixpath,$(TEX_FOLDER)/$(AUX_FOLDER)/main_tex.pdf) ./control.pdf
	

glossaries:
	python glossaries/updateMathSymbols.py


biber:
	$(CHANGE_DIRECTORY) $(TEX_FOLDER) && $(MAKE) biber

clear:
	$(CHANGE_DIRECTORY)  $(TEX_FOLDER) && $(RM) $(AUX_FOLDER)/main_*