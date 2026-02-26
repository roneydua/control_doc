#!/bin/sh

# pdflatex -shell-escape -interaction=nonstopmode ./reportExperimentalSetup.tex
# # biber ./reportExperimentalSetup.bcf
# # makeglossaries ./reportExperimentalSetup
# pdflatex -shell-escape -interaction=nonstopmode ./reportExperimentalSetup.tex
# pdflatex -shell-escape -interaction=nonstopmode ./reportExperimentalSetup.tex

auxFolder="auxFolder/"
python3 ../glossaries/updateMathSymbols.py
# Copy the last bibliografia.bib file on "Arquivos" HDD.
cp /media/Arquivos/mega/biblioteca/bibliografia.bib ./


# Convert the main_lyx.lyx file to latex and save it to main.tex
lyx2tex(){
    lyx --force-overwrite --export latex "main_lyx.lyx"
}

Xelatex() {
    xelatex -output-driver="xdvipdfmx -i dvipdfmx-unsafe.cfg -q -E" -interaction=batchmode -output-directory=$auxFolder "main.tex"

}

Lualatex() {
    lualatex --shell-escape -output-directory=$auxFolder "main.tex"
    # exit
}
Latex() {
    latex -shell-escape -interaction=batchmode -output-directory=$auxFolder "main.tex"
#    latex  -output-directory=$auxFolder "main.tex"
}
PdfLatex(){
    pdflatex --shell-escape -interaction=batchmode -output-directory=$auxFolder "main.tex"
}

MainCompiler(){
    PdfLatex
}

Fast() {
    lyx2tex
    echo "Fast compile. Do not run bibliographies and glossaries updates"
    # pdflatex -interaction=batchmode --shell-escape -output-directory=$auxFolder "main.tex"
    # latex -dALLOWPSTRANSPARENCY -interaction=batchmode -output-directory=$auxFolder "main.tex"
    # Xelatex
    MainCompiler
    # dvipdf -dNOSAFER -dALLOWPSTRANSPARENCY $auxFolder"main.dvi" "main.pdf"
    # dvips $auxFolder"main.dvi" -o  $auxFolder"main.ps"
    # ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY $auxFolder"main.ps" $auxFolder"main.pdf"
    cp $auxFolder\main.pdf RelatorioSemestral_3Periodo.pdf
    # exit
}
Complete() {
    lyx2tex

    echo "ESTAGE 1"

    rm $auxFolder\main.*

    MainCompiler
    # xetex -output-driver="xdvipdfmx -i dvipdfmx-unsafe.cfg -q -E" -interaction=batchmode -output-directory=$auxFolder "main.tex"
    makeglossaries -d $auxFolder "main"
    biber -output-directory=$auxFolder "main"
    # latex --shell-escape -interaction=batchmode -output-directory=$auxFolder "main"
    # pst2pdf
    MainCompiler
    # latex -interaction=batchmode -output-directory=$auxFolder "main"
    # echo "ESTAGE 2 dvi-> ps"
    # # dvips $auxFolder"main.dvi" -o $auxFolder"main.ps"
    # dvipdf -dALLOWPSTRANSPARENCY $auxFolder"main.dvi" $auxFolder"main.pdf"
    # Fast
    exit
}
while getopts "fc" opt; do
    case $opt in
    f)
        echo "fast compile option"
        Fast
        exit
        ;;
    c)
        echo "Complete compilation"
        Complete
        exit
        ;;

    esac
done

# remove files
