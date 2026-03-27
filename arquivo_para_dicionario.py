from decimal import  Decimal
ARQUIVO = "contas.txt"

def arquivo_para_dicionario():
    contas = []
    num_serie = []
    try:
        arquivo = open(ARQUIVO, "r", encoding='utf-8')
    except FileNotFoundError:
        return contas
    linhas = arquivo.readlines()
    if not linhas:
        arquivo.close()
        return [], 0
    for linha in linhas:
        linha = linha.strip()
        # nm_conta, num_serie, sl_conta, dt_conta = linha.split(";")
        # sl_conta = Decimal(sl_conta)
        conta = linha.split(";")
        num_serie.append(int(conta[0]))
        conta[2] = Decimal(conta[2])
        contas.append(conta)
    arquivo.close()
    return contas, max(num_serie)

def salvar_arquivo(contas):
    contas.sort(key=lambda w: w[3])
    linhas = []
    for conta in contas:
        linhas.append(f'{conta[0]};{conta[1]};{conta[2]};{conta[3]};{conta[4]}\n')
    arquivo = open(ARQUIVO, "w", encoding='utf-8')
    arquivo.writelines(linhas)
    arquivo.close()