import pandas as pd
import sys
import os

# Set predefined variables
headers = ["Classic","Grøn", "Guld", "Cider", "Cocio", "Soda"]
top_bot_margin = 3 #cm
out_file = "Stregliste.tex"
filename = "participants.csv"
clean_TeX_output = True
columns = ["First name", "Last name"]


for i in range(1,len(sys.argv)):
    if sys.argv[i] == "-f":
        filename = sys.argv[i+1]
    if sys.argv[i] == "-h":
        headers = sys.argv[i+1].split(";")
    if sys.argv[i] == "-m":
        top_bot_margin = int(sys.argv[i+1])
    if sys.argv[i] == "-o":
        out_file = sys.argv[i+1]
    if sys.argv[i] == "--debug":
        clean_TeX_output = False
    if sys.argv[i] == "--names":
        columns = sys.argv[i+1].split(";")
    if sys.argv[i] == "--help":
        print("Stregliste.py -f <filename> -h <headers> -m <top_bot_margin> -o <out_file> [--debug] [--names <names>]")
        print("<filename> - Name of csv file with participants")
        print("\tMust contain columns 'First name' and 'Last name'")
        print("<headers> - Names of headers separated by semicolon")
        print("<names> - Names of columns containing names separated by semicolon")
        sys.exit()

try:
    participants = pd.read_csv(filename).sort_values(by=columns[0])[columns]
except (FileNotFoundError, KeyError):
    print("Error:")
    print("No csv file with names of participants found.")
    print("Or the csv file does not contain columns: " + ", ".join(columns))
    sys.exit()

no_cols = len(headers)
row_height = 1.5 #cm
no_rows=10

def add_to_file(string):
    with open(out_file, "a", encoding="utf-8") as TeXfile:
        TeXfile.write(string+"\n")

def clean_file():
    with open(out_file, "w", encoding="utf-8") as TeXfile:
        TeXfile.write("")

def print_participant(row):
    names = [str(name) for name in row[columns].tolist()]
    add_to_file("\\newline ".join(names)+f"\\vspace*{{{row_height} cm}}" + "&"*(no_cols) + "\\\\ \\hline")


def print_table(headers,participants,ind):
    global no_rows, no_cols
    add_to_file("\\begin{tabular}{" + "|" + f"p{{\\mycolwidth}}|"*(no_cols + 1) + "}")
    add_to_file("\\hline")
    add_to_file("Name & " + " & ".join(headers) + " \\\\ \\hline")
    for i in range(ind,min(ind+no_rows,len(participants))):
        print_participant(participants.iloc[i])
    add_to_file("\\hline")
    add_to_file("\\end{tabular}")
    add_to_file(r"\newpage")
    add_to_file("")


def main():
    clean_file()
    add_to_file(r"""
\documentclass[a4paper]{article}

\usepackage[T1]{fontenc}
\usepackage{booktabs}
\usepackage[margin=0.5in]{geometry}

\begin{document}
\pagestyle{empty}
\newlength{\mycolwidth}
   """) 

    add_to_file(r"\setlength{\mycolwidth}{\dimexpr"+f"{1/(no_cols+1)}"+r"\textwidth-2\tabcolsep-2\arrayrulewidth\relax}")

    for i in range(0,len(participants),no_rows):
        print_table(headers,participants,i)

    add_to_file(r"""
    \end{document}
    """)

    #Run latex
    if clean_TeX_output:
        os.system("pdflatex -interaction=batchmode " + out_file)
        os.remove(out_file.replace(".tex",".log"))
        os.remove(out_file.replace(".tex",".aux"))
        os.remove(out_file)
    else:
        os.system("pdflatex " + out_file)
    print("Stregliste created at " + out_file.replace(".tex",".pdf"))

if __name__ == "__main__":
    main()
