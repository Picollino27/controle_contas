from decimal import  Decimal
from datetime import datetime

import decimal
from controle_contas import menu, fazer_movimentação, ver_saldo,capturar_erro,ver_extrato,apagar_movimentação,ver_contas


if __name__ == '__main__':
    opcao = ""
    while opcao.lower() != "v":
        menu()
        opcao = input("digite a opção -> ").lower()
        if opcao not in ["f", "e", "v", "s","a"]:
            print("ação invalida")
        elif opcao == "f":
            ver_contas()
            nome_conta = input("digite o nome da conta -> ")
            saldo_conta,data = capturar_erro()
            if not (saldo_conta or data):
                continue
            else:
                comentario = input("faça seu comentário -> ")
                comentario = comentario.replace(";", '')
                retorno = fazer_movimentação(nome_conta, saldo_conta,data,comentario)
                if retorno:
                    print("conta ja existente")
                else:
                    print("conta criada com sucesso")
        elif opcao == "e":
            flag = 0
            while not flag:
                data_inicial = input("digite a data inicial -> ")
                try:
                    data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y").date()
                except ValueError:
                    if data_inicial == "v":
                        break
                        continue
                    else:
                        print("data invalida")
                        continue
                else:
                    flag = 0
                    while not flag:
                        data_final = input("digite a data final -> ")
                        try:
                            data_final = datetime.strptime(data_final, "%d/%m/%Y").date()
                        except ValueError:
                            if data_final == "v":
                                break
                                continue
                            else:
                                print("data invalida")
                                continue
                        else:
                            flag = 1
                            retorno = ver_extrato(data_inicial,data_final)
                            if not retorno:
                                print("o arquivo não existe")
                                continue
                            elif retorno == 1:
                                continue
                            elif retorno == 2:
                                print("data inicial maior que data final")
                                continue


        elif opcao == "s":
            if not ver_saldo():
                print("o arquivo não existe")
            else:
                continue
        elif opcao == "a":
            flag = 0
            while flag == 0:
                num_serie = input("digite o número de série -> ")
                try:
                    int(num_serie)
                except ValueError:
                    if num_serie == "v":
                        flag = 1
                        continue
                    else:
                        print("valor invalido")
                        continue
                else:
                    flag = 1
                    retorno = apagar_movimentação(num_serie)
                    if retorno == 0:
                        print("o arquivo não existe")
                    elif retorno == 1:
                        print("a conta não existe")
                    elif retorno == 2:
                        print("conta apagada com sucesso")








    # primeira_acao = input("c = criar uma nova conta;m = movimentar;e = ver o extrato")
    # primeira_acao.strip()
    # if primeira_acao.lower() == "c":
    #     # arquivo = open("nome do arquivo","w")
    #     nova_conta = input("digite o nome da sua nova conta")
    #     novo_saldo = float(input("digite o saldo da nova conta"))
    #     conta = {nova_conta : novo_saldo}
    #     # colocar conta em uma nova linha
    #     # arquivo.close()
    # elif primeira_acao.lower() == "m":
    #     # contas = open("nome do arquivo","w")
    #     contas = []
    #     conta_movimentada = input("qual conta vc quer movimentar?")
    #     conta_movimentada = conta_movimentada.capitalize()
    #
    #                # contas.readlines
    #         if conta != conta_movimentada:
    #             pass
    #         elif conta == conta_movimentada:
    #             movimentação = input("c = creditar; d = debitar")
    #             if movimentação == "c":
    #                 conta += input("digite o valor creditado")
    #             elif movimentação == "d":
    #                 conta -= input("digite o valor debitado")
    #     # arquivo.close()
    # elif primeira_acao.lower() == "e":
    #     # arquivo = open("nome do arquivo","r")
    #
    #     extrato_conta = input("digite o nome da conta")
    #     # arquivo.close
