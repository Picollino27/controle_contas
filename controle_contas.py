from decimal import Decimal
from tkcalendar import DateEntry
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from dateutil.relativedelta import relativedelta
from tkinter import messagebox


from arquivo_para_dicionario import arquivo_para_dicionario, salvar_arquivo
import decimal
from datetime import datetime, timedelta

style = None
LARGURA_LABEL = 13
LARGURA_DATE_ENTRY = 11
QT_TRACOS = 50
ARQUIVO = "contas.txt"
num_serie = 0
ESPACOS = " " * 20
FONTE_ARIAL_10 = ("Arial", 10)
FONTE_ARIAL_12 = ("Arial", 12)
FONTE_ARIAL_15 = ("Arial", 15)
FONTE_HELVETICA_10 = ('Helvetica', 10)
PAD_X = 12
PAD_Y = 9
DATA_HOJE = datetime.today()
DATA_ANTERIOR = DATA_HOJE - relativedelta(months=1)

class JanelaMovimentarConta(tk.Toplevel):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.title("Fazer Movimentação")
        self.geometry("400x300+400+50")
        frame_1 = tk.Frame(self)
        frame_1.pack(side='top',
                     expand=tk.YES,
                     fill=tk.BOTH)

        tk.Label(frame_1,
                 text="Nome da Conta",
                 width=LARGURA_LABEL,
                 font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                           fill=tk.BOTH,
                                           side=tk.LEFT,
                                           padx=PAD_X,
                                           pady=PAD_Y)
        lista_contas = ver_contas()
        contas = []
        for conta in lista_contas:
            contas.append(conta)
        self.entry_nm_conta = ttk.Combobox(frame_1, values=contas, font=FONTE_ARIAL_12, width=LARGURA_LABEL)
        self.entry_nm_conta.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT, padx=PAD_X,
                            pady=PAD_Y)

        frame_2 = tk.Frame(self)
        frame_2.pack(side='top',
                     expand=tk.YES,
                     fill=tk.BOTH, )

        tk.Label(frame_2,
                 text="Valor",
                 width=LARGURA_LABEL,
                 font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                           fill=tk.BOTH,
                                           side=tk.LEFT,
                                           padx=PAD_X,
                                           pady=PAD_Y)

        self.entry_valor = tk.Entry(frame_2, font=FONTE_ARIAL_12, width=LARGURA_LABEL)
        self.entry_valor.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT, padx=PAD_X,
                         pady=PAD_Y)
        self.valor_anterior = None

        frame_3 = tk.Frame(self)
        frame_3.pack(side='top',
                     expand=tk.YES,
                     fill=tk.BOTH, )

        tk.Label(frame_3, text="Data",
                 width=LARGURA_LABEL,
                 font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                           fill=tk.BOTH,
                                           side=tk.LEFT,
                                           padx=PAD_X,
                                           pady=PAD_Y)

        self.entry_data = DateEntry(frame_3,
                                    font=FONTE_ARIAL_12,
                                    date_pattern='dd/mm/yyyy',
                                    width=LARGURA_DATE_ENTRY)
        self.entry_data.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT,
                             padx=PAD_X,
                             pady=PAD_Y)

        frame_4 = tk.Frame(self)
        frame_4.pack(side='top',
                     expand=tk.YES,
                     fill=tk.BOTH, )

        tk.Label(frame_4,
                 text="Comentário",
                 width=LARGURA_LABEL,
                 font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                           fill=tk.BOTH,
                                           side=tk.LEFT, padx=PAD_X,
                                           pady=PAD_Y)

        self.entry_comentario = tk.Entry(frame_4, font=FONTE_ARIAL_12, width=LARGURA_LABEL)
        self.entry_comentario.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT, padx=PAD_X,
                              pady=PAD_Y)

        frame_5 = tk.Frame(self)
        frame_5.pack(side='top',
                     expand=tk.YES,
                     fill=tk.BOTH, )

        self.bt_confirmar = tk.Button(frame_5,
                                 text="confirmar",
                                 width=9,
                                 font=FONTE_ARIAL_15,
                                 command=self.capturar_infos)

        self.bt_confirmar.pack(expand=tk.YES,
                          fill=tk.BOTH,
                          side=tk.LEFT,
                          padx=PAD_X,
                          pady=PAD_Y)

        bt_sair = tk.Button(frame_5,
                            text="sair",
                            width=9,
                            font=FONTE_ARIAL_15,
                            command=self.destroy)

        bt_sair.pack(expand=tk.YES,
                     fill=tk.BOTH,
                     side=tk.RIGHT,
                     padx=PAD_X,
                     pady=PAD_Y, )

    def capturar_infos(self):
        nome_conta = self.entry_nm_conta.get()
        nome_conta = nome_conta.replace("\"", "*")
        nome_conta = nome_conta.replace("\'", "*")
        nome_conta = nome_conta.replace(";", ":")

        valor = self.entry_valor.get()
        data = self.entry_data.get()

        comentario = self.entry_comentario.get()
        comentario = comentario.replace("\"", "*")
        comentario = comentario.replace("\'", "*")
        comentario = comentario.replace(";", ":")

        if nome_conta.strip() == "":
            tk.messagebox.showinfo("erro",
                                   "nome da conta invalido",
                                   parent=self)
            return
        try:
            valor = Decimal(valor)
        except decimal.InvalidOperation:
            tk.messagebox.showinfo("erro",
                                   "valor inválido",
                                   parent=self)
            return
        try:
            data = datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            tk.messagebox.showinfo("erro",
                                   "data invalida",
                                   parent=self)
            return
        fazer_movimentação(nome_conta, valor, data, comentario)
        tk.messagebox.showinfo("sucesso",
                                   "movimentação efetuada",
                                   parent=self)
        self.destroy()
    def atualizar_extrato(self,janela_extrato,num_serie):
        saldo_atualizado = janela_extrato.saldo_final + \
                           Decimal(self.entry_valor.get()) - \
                           self.valor_anterior
        janela_extrato.label_saldo_final.config(text=f'o saldo final é {saldo_atualizado}')
        its_selecionados = janela_extrato.tree.selection()

        janela_extrato.tree.item(its_selecionados, values=(num_serie,
                                                           self.entry_nm_conta.get(),
                                                           self.entry_valor.get(),
                                                           self.entry_data.get(),
                                                           self.entry_comentario.get()))
        self.destroy()

def menu():
    print("-" * QT_TRACOS)
    print("f = fazer movimentação")
    print("e = ver extrato")
    print("s = ver saldo")
    print("a = apagar movimentação")
    print("v = sair")
    print("-" * QT_TRACOS)

def editar_movimentacao(janela_extrato):
    itens_selecionados = janela_extrato.tree.selection()
    flag = len(itens_selecionados)
    if flag > 1:
        tk.messagebox.showinfo("erro","mais de um item selecionado")
        return
    if not itens_selecionados:
        return
    valores = janela_extrato.tree.item(itens_selecionados[0], 'values')
    janela_fazer_movimentação = JanelaMovimentarConta()

    janela_fazer_movimentação.bt_confirmar.config(command=lambda:
        [apagar_movimentação(valores[0]),
        fazer_movimentação(janela_fazer_movimentação.entry_nm_conta.get(),
                        janela_fazer_movimentação.entry_valor.get(),
                        janela_fazer_movimentação.entry_data.get_date(),
                        janela_fazer_movimentação.entry_comentario.get()),
         janela_fazer_movimentação.atualizar_extrato(janela_extrato,valores[0])])

    janela_fazer_movimentação.entry_nm_conta.insert(0, valores[1])
    janela_fazer_movimentação.entry_valor.insert(0, valores[2])
    data = datetime.strptime(valores[3], "%Y-%m-%d").date()
    janela_fazer_movimentação.entry_data.set_date(data)
    janela_fazer_movimentação.entry_comentario.insert(0,valores[4])
    janela_fazer_movimentação.valor_anterior = Decimal(valores[2])

    janela_fazer_movimentação.focus_set()
    # janela_ver_extrato.grab_set()
    janela_fazer_movimentação.wait_window()


def fazer_movimentação(nome_conta, saldo_conta, data, comentario):
    flag = 0
    while flag == 0:
        contas, num_serie = arquivo_para_dicionario()
        if contas:
            flag = 1
        else:
            open(ARQUIVO, "w", encoding='utf-8')
        contas.append([num_serie + 1, nome_conta, saldo_conta, data.strftime("%Y-%m-%d"), comentario])
        salvar_arquivo(contas)
        return 0


def ver_saldo(printar_na_tela=True):
    contas = {}
    try:
        arquivo = open(ARQUIVO, "r")
    except FileNotFoundError:
        return contas

    contas, num_serie = arquivo_para_dicionario()

    contas.sort(key=lambda w: w[3])

    saldos = {}
    saldo_final = 0
    for conta in contas:
        saldo_final += conta[2]
        if conta[2] == 0:
            continue
        elif conta[1] not in saldos:
            saldos[conta[1]] = [conta[0], conta[2], conta[3]]
        elif conta[1] in saldos:
            saldos[conta[1]][1] += conta[2]

    if printar_na_tela:
        print(QT_TRACOS * 2 * '-')
        for saldo in saldos:
            if not saldos[saldo][1]:
                continue
            else:
                print(f'o saldo da conta {saldo} é {saldos[saldo][1]}')
    return saldos, saldo_final

def capturar_erro():
    flag = 0
    while not flag:
        saldo_conta = input("digite o valor da movimentação -> ")
        try:
            saldo_conta = Decimal(saldo_conta)
        except decimal.InvalidOperation:
            if saldo_conta == "v":
                saldo_conta = ""
                data = ""
                return saldo_conta, data
            else:
                print("valor invalido")
                continue
        else:
            flag = 0
            while not flag:
                data = input("digite a data -> ")
                try:
                    data = datetime.strptime(data, "%d/%m/%Y").date()
                except ValueError:
                    if data == "v":
                        break
                        return saldo_conta, data
                    else:
                        print("data invalida")
                        continue
                else:
                    return saldo_conta, data


def ver_extrato(data_inicial, data_final):

    data_inicial = data_inicial.strftime("%Y-%m-%d")
    data_final = data_final.strftime("%Y-%m-%d")
    contas, num_serie = arquivo_para_dicionario()

    if not contas:
        return [], Decimal('0.0'), Decimal('0.0')
    if data_inicial > data_final:
        return 2

    contas.sort(key=lambda w: w[3])

    saldo_inicial = [conta[2] for conta in contas if conta[3] < data_inicial]
    saldo_inicial = sum(saldo_inicial)

    saldo_final = [conta[2] for conta in contas if conta[3] <= data_final]
    saldo_final = sum(saldo_final)

    extratos = [extrato for extrato in contas if extrato[3] >= data_inicial and
                extrato[3] <= data_final]
    return extratos, saldo_inicial, saldo_final

def abrir_janela_extrato(janela_anterior):

    data_inicial = janela_anterior.entry_data_inicial.get()
    data_final = janela_anterior.entry_data_final.get()

    try:
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y").date()
    except ValueError:
        tk.messagebox.showinfo("Erro", "Data Inicial Inválida")
        return

    try:
        data_final = datetime.strptime(data_final, "%d/%m/%Y").date()
    except ValueError:
        tk.messagebox.showinfo("Erro", "Data Inválida")
        return

    if data_inicial > data_final:
        tk.messagebox.showinfo(
            "Erro",
            "Data Final deve ser maior que a Inicial",
            parent=janela_anterior)
        return

    janela_extrato = tk.Toplevel()
    janela_extrato.title("Extrato")
    janela_extrato.geometry("1000x500+400+300")
    
    extratos, \
        saldo_inicial, \
        janela_extrato.saldo_final = ver_extrato(data_inicial, data_final)

    frame_saldo_inicial = tk.Frame(janela_extrato)
    frame_saldo_inicial.pack(side='top', expand=tk.YES, fill=tk.BOTH)

    tk.Label(frame_saldo_inicial,
             text=f'Saldo Inic'
                  f'ial: {saldo_inicial}',
             width=LARGURA_LABEL,
             font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                       fill=tk.BOTH,
                                       side=tk.LEFT)
    frame_tabela = tk.Frame(janela_extrato)
    frame_tabela.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    janela_extrato.tree = ttk.Treeview(frame_tabela,
                                       columns=('Num_série',
                                                'Nome',
                                                'Valor',
                                                "Data",
                                                "Comentário",),
                                       show='headings')

    janela_extrato.tree.heading('Num_série', text='Num série')
    janela_extrato.tree.heading('Nome', text='Nome')
    janela_extrato.tree.heading('Valor', text='Valor')
    janela_extrato.tree.heading('Data', text='Data')
    janela_extrato.tree.heading('Comentário', text='Comentário')

    janela_extrato.tree.column('Num_série', width=30)
    janela_extrato.tree.column('Nome', width=150)
    janela_extrato.tree.column('Valor', width=50)
    janela_extrato.tree.column('Data', width=50)

    for extrato in extratos:
        janela_extrato.tree.column('Comentário', width=150)
        janela_extrato.tree.insert('', tk.END, values=(extrato[0],
                                                       extrato[1],
                                                       extrato[2],
                                                       extrato[3],
                                                       extrato[4]))
    janela_extrato.tree.pack(side=tk.LEFT, expand=True, fill='both', pady=PAD_Y)
    vsb = ttk.Scrollbar(frame_tabela,
                        orient="vertical",
                        command=janela_extrato.tree.yview)


    janela_extrato.tree.configure(yscrollcommand=vsb.set)


    vsb.pack(side=tk.LEFT,
             fill=tk.Y,
             pady=PAD_Y)

    frame_saldo_final = tk.Frame(janela_extrato)
    frame_saldo_final.pack(side='top',
                           expand=tk.YES,
                           fill=tk.BOTH)

    janela_extrato.label_saldo_final = tk.Label(frame_saldo_final,
                                                text=f'Saldo Final:{janela_extrato.saldo_final}',
                                                width=LARGURA_LABEL,
                                                font=FONTE_ARIAL_12)

    janela_extrato.label_saldo_final.pack(expand=tk.YES,
                                          fill=tk.BOTH,
                                          side=tk.LEFT)

    bt_sair = tk.Button(janela_extrato,
                        text="Sair",
                        width=9,
                        font=FONTE_ARIAL_15,
                        command=janela_extrato.destroy)
    bt_sair.pack(expand=tk.YES,
                 fill=tk.BOTH,
                 side=tk.TOP,
                 padx=PAD_X,
                 pady=PAD_Y, )
    frame_bts = tk.Frame(frame_tabela)
    frame_bts.pack(side=tk.RIGHT,
                           expand=tk.YES,
                           fill=tk.BOTH)
    bt_editar = tk.Button(frame_bts,
                          text="editar",
                          font=FONTE_ARIAL_15,
                          command=lambda: editar_movimentacao(janela_extrato))
    bt_editar.pack(expand=tk.YES,
                 fill=tk.BOTH,
                 side=tk.TOP,
                 padx=PAD_X,
                 pady=PAD_Y, )
    bt_apagar = tk.Button(frame_bts,
                          text="Apagar",
                          width=15,
                          height=5,
                          font=FONTE_ARIAL_15,
                          command=lambda:
                          apagar_movimentacao_extrato(janela_extrato))
    bt_apagar.pack(
        fill=tk.BOTH,
        side=tk.TOP,
        padx=PAD_X,
        pady=PAD_Y, )

    janela_extrato.focus_set()
    # janela_extrato.grab_set()
    janela_extrato.wait_window()


def apagar_movimentacao_extrato(janela_extrato):
    itens_selecionados = janela_extrato.tree.selection()
    if not itens_selecionados:
        return
    resposta = messagebox.askyesno(parent=janela_extrato,
                                   title="Confirma",
                                   message="Quer mesmo apagar essa conta?", )
    if resposta:

        for item in itens_selecionados:
            valores = janela_extrato.tree.item(item, 'values')
            apagar_movimentação(valores[0])
            saldo = valores[2]
            janela_extrato.tree.delete(item)
            janela_extrato.saldo_final -= Decimal(saldo)
        janela_extrato.label_saldo_final.config(
            text=f'Saldo Final:{janela_extrato.saldo_final}')
    else:
        return


def apagar_movimentação(num_serie):
    contas, num = arquivo_para_dicionario()
    if not contas:
        return 0
    conta_apgada = [conta for conta in contas if conta[0] == num_serie]
    if conta_apgada:
        posicao = contas.index(conta_apgada[0])
        del contas[posicao]
    else:
        return 1
    salvar_arquivo(contas)
    return 2


def ver_contas():
    contas, num_serie = arquivo_para_dicionario()
    lista_contas = {}
    print(f'{("n°" + " " * 4)[:5]}\t|{("conta" + ESPACOS)[:20]}')
    for conta in contas:
        lista_contas.setdefault(conta[1], str(conta[2]))
    return lista_contas
    for conta in lista_contas:
        print(f'{(conta + " " * 20)[:20]}\t|{(lista_contas[conta][0] + ESPACOS)[:20]}')

        def conferir_valores():
            pass


def abrir_janela_principal(menu):

    global style
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    font=FONTE_ARIAL_12,
                    rowheight=25)
    style.configure("Treeview.Heading",
                    font=('Arial', 12, 'bold'))

    menu.title("controle de contas")
    menu.geometry("300x300+50+50")

    bt_fazer_movimentacao = tk.Button(menu,
                                      text="Fazer Movimentação",
                                      font=FONTE_ARIAL_15,
                                      command=abrir_janela_movimentar_conta)

    bt_fazer_movimentacao.pack(expand=tk.YES,
                               fill=tk.BOTH,
                               side=tk.TOP,
                               padx=PAD_X,
                               pady=PAD_Y)

    bt_ver_extrato = tk.Button(menu,
                               text="Ver Extrato",
                               font=FONTE_ARIAL_15,
                               command=abrir_janela_pesquisar_extrato)

    bt_ver_extrato.pack(expand=tk.YES,
                        fill=tk.BOTH,
                        side='top',
                        padx=PAD_X,
                        pady=PAD_Y)

    bt_ver_saldo = tk.Button(menu, text="Ver Saldo", font=FONTE_ARIAL_15, command=abrir_janela_ver_saldos)
    bt_ver_saldo.pack(expand=tk.YES,
                      fill=tk.BOTH,
                      side='top',
                      padx=PAD_X,
                      pady=PAD_Y)

    # bt_apagar_conta = tk.Button(menu, text="Apagar Conta", font=FONTE_ARIAL_15)
    # bt_apagar_conta.pack(expand=tk.YES,
    #                      fill=tk.BOTH,
    #                      side='top',
    #                      padx=PAD_X,
    #                      pady=PAD_Y)

    bt_sair = tk.Button(menu, text="Sair", font=FONTE_ARIAL_15, command=exit)
    bt_sair.pack(expand=tk.YES,
                 fill=tk.BOTH,
                 side='top',
                 padx=PAD_X,
                 pady=PAD_Y)

    menu.mainloop()


def abrir_janela_movimentar_conta():

    janela_fazer_movimentação = JanelaMovimentarConta()
    janela_fazer_movimentação.focus_set()
    janela_fazer_movimentação.wait_window()

    # janela_fazer_movimentação = tk.Toplevel()
    # janela_fazer_movimentação.title("Fazer Movimentação")
    # janela_fazer_movimentação.geometry("400x300+400+50")
    #
    # def capturar_infos():
    #     nome_conta = entry_nm_conta.get()
    #     nome_conta = nome_conta.replace("\"", "*")
    #     nome_conta = nome_conta.replace("\'", "*")
    #     nome_conta = nome_conta.replace(";", ":")
    #
    #     valor = entry_valor.get()
    #     data = entry_data.get()
    #
    #     comentario = entry_comentario.get()
    #     comentario = comentario.replace("\"", "*")
    #     comentario = comentario.replace("\'", "*")
    #     comentario = comentario.replace(";", ":")
    #
    #     if nome_conta.strip() == "":
    #         tk.messagebox.showinfo("erro",
    #                                "nome da conta invalido",
    #                                parent=janela_fazer_movimentação)
    #         return
    #     try:
    #         valor = Decimal(valor)
    #     except decimal.InvalidOperation:
    #         tk.messagebox.showinfo("erro",
    #                                "valor inválido",
    #                                parent=janela_fazer_movimentação)
    #         return
    #     try:
    #         data = datetime.strptime(data, "%d/%m/%Y").date()
    #     except ValueError:
    #         tk.messagebox.showinfo("erro",
    #                                "data invalida",
    #                                parent=janela_fazer_movimentação)
    #         return
    #     fazer_movimentação(nome_conta, valor, data, comentario)
    #     tk.messagebox.showinfo("sucesso",
    #                            "movimentação efetuada",
    #                            parent=janela_fazer_movimentação)
    #     janela_fazer_movimentação.destroy()
    #
    # frame_1 = tk.Frame(janela_fazer_movimentação)
    # frame_1.pack(side='top',
    #              expand=tk.YES,
    #              fill=tk.BOTH)
    #
    # tk.Label(frame_1,
    #          text="Nome da Conta",
    #          width=LARGURA_LABEL,
    #          font=FONTE_ARIAL_12).pack(expand=tk.YES,
    #                                    fill=tk.BOTH,
    #                                    side=tk.LEFT,
    #                                    padx=PAD_X,
    #                                    pady=PAD_Y)
    # lista_contas = ver_contas()
    # contas = []
    # for conta in lista_contas:
    #     contas.append(conta)
    # entry_nm_conta = ttk.Combobox(frame_1,values=contas, font=FONTE_ARIAL_12, width=LARGURA_LABEL)
    # entry_nm_conta.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT,padx=PAD_X,
    #              pady=PAD_Y)
    #
    #
    # frame_2 = tk.Frame(janela_fazer_movimentação)
    # frame_2.pack(side='top',
    #              expand=tk.YES,
    #              fill=tk.BOTH,)
    #
    # tk.Label(frame_2,
    #          text="Valor",
    #          width=LARGURA_LABEL,
    #          font=FONTE_ARIAL_12).pack(expand=tk.YES,
    #                                    fill=tk.BOTH,
    #                                    side=tk.LEFT,
    #                                    padx=PAD_X,
    #                                    pady=PAD_Y)
    #
    # entry_valor = tk.Entry(frame_2, font=FONTE_ARIAL_12, width=LARGURA_LABEL)
    # entry_valor.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT,padx=PAD_X,
    #              pady=PAD_Y)
    #
    # frame_3 = tk.Frame(janela_fazer_movimentação)
    # frame_3.pack(side='top',
    #              expand=tk.YES,
    #              fill=tk.BOTH,)
    #
    # tk.Label(frame_3, text="Data",
    #          width=LARGURA_LABEL,
    #          font=FONTE_ARIAL_12).pack(expand=tk.YES,
    #                                    fill=tk.BOTH,
    #                                    side=tk.LEFT,
    #                                    padx=PAD_X,
    #                                    pady=PAD_Y)
    #
    # entry_data = DateEntry(frame_3, font=FONTE_ARIAL_12, date_pattern='dd/mm/yyyy', width=LARGURA_DATE_ENTRY)
    # entry_data.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT,padx=PAD_X,
    #              pady=PAD_Y)
    #
    # frame_4 = tk.Frame(janela_fazer_movimentação)
    # frame_4.pack(side='top',
    #              expand=tk.YES,
    #              fill=tk.BOTH,)
    #
    # tk.Label(frame_4,
    #          text="Comentário",
    #          width=LARGURA_LABEL,
    #          font=FONTE_ARIAL_12).pack(expand=tk.YES,
    #                                    fill=tk.BOTH,
    #                                    side=tk.LEFT,padx=PAD_X,
    #              pady=PAD_Y)
    #
    # entry_comentario = tk.Entry(frame_4, font=FONTE_ARIAL_12, width=LARGURA_LABEL)
    # entry_comentario.pack(expand=tk.YES, fill=tk.BOTH, side=tk.RIGHT,padx=PAD_X,
    #              pady=PAD_Y )
    #
    # frame_5 = tk.Frame(janela_fazer_movimentação)
    # frame_5.pack(side='top',
    #              expand=tk.YES,
    #              fill=tk.BOTH,)
    #
    # bt_confirmar = tk.Button(frame_5,
    #                          text="confirmar",
    #                          width=9,
    #                          font=FONTE_ARIAL_15,
    #                          command=capturar_infos)
    #
    # bt_confirmar.pack(expand=tk.YES,
    #                   fill=tk.BOTH,
    #                   side=tk.LEFT,
    #                   padx=PAD_X,
    #                   pady=PAD_Y)
    #
    # bt_sair = tk.Button(frame_5,
    #                     text="sair",
    #                     width=9,
    #                     font=FONTE_ARIAL_15,
    #                     command=janela_fazer_movimentação.destroy)
    #
    # bt_sair.pack(expand=tk.YES,
    #              fill=tk.BOTH,
    #              side=tk.RIGHT,
    #              padx=PAD_X,
    #              pady=PAD_Y, )

    # janela_fazer_movimentação.focus_set()
    # # janela_fazer_movimentação.grab_set()
    # janela_fazer_movimentação.wait_window()


def abrir_janela_pesquisar_extrato():
    janela_ver_extrato = tk.Toplevel()
    janela_ver_extrato.title("Ver Extrato")
    janela_ver_extrato.geometry("400x190+400+50")

    LARGURA_LABEL = 13

    frame_1 = tk.Frame(janela_ver_extrato)
    frame_1.pack(side='top',
                 expand=tk.YES,
                 fill=tk.BOTH,
                 padx=PAD_X,
                 pady=PAD_Y)

    tk.Label(frame_1,
             text="Data Inicial",
             width=LARGURA_LABEL,
             font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                       fill=tk.BOTH,
                                       side=tk.LEFT)
    janela_ver_extrato.entry_data_inicial = DateEntry(frame_1,
                                                      date_pattern='dd/mm/yyyy',
                                                      font=FONTE_ARIAL_12)
    janela_ver_extrato.entry_data_inicial.set_date(date=DATA_ANTERIOR)
    janela_ver_extrato.entry_data_inicial.pack(expand=tk.YES,
                                               fill=tk.BOTH,
                                               side=tk.RIGHT,
                                               padx=PAD_X,
                                               pady=PAD_Y)

    frame_2 = tk.Frame(janela_ver_extrato)
    frame_2.pack(side='top',
                 expand=tk.YES,
                 fill=tk.BOTH,
                 padx=PAD_X,
                 pady=PAD_Y)

    tk.Label(frame_2,
             text="Data Final",
             width=LARGURA_LABEL,
             font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                       fill=tk.BOTH,
                                       side=tk.LEFT)

    janela_ver_extrato.entry_data_final = DateEntry(frame_2,
                                                    date_pattern='dd/mm/yyyy',
                                                    font=FONTE_ARIAL_12)
    janela_ver_extrato.entry_data_final.pack(expand=tk.YES,
                                             fill=tk.BOTH,
                                             side=tk.RIGHT,
                                             padx=PAD_X,
                                             pady=PAD_Y)

    frame_5 = tk.Frame(janela_ver_extrato)
    frame_5.pack(side='top',
                 expand=tk.YES,
                 fill=tk.BOTH,
                 padx=PAD_X,
                 pady=PAD_Y)

    bt_confirmar = tk.Button(frame_5,
                             text="Confirmar",
                             width=9,
                             font=FONTE_ARIAL_15,
                             command=lambda: abrir_janela_extrato(janela_ver_extrato))
    bt_confirmar.pack(expand=tk.YES,
                      fill=tk.BOTH,
                      side=tk.LEFT,
                      padx=PAD_X,
                      pady=PAD_Y)

    bt_sair = tk.Button(frame_5, text="Sair", width=9, font=FONTE_ARIAL_15,
                        command=janela_ver_extrato.destroy)
    bt_sair.pack(expand=tk.YES,
                 fill=tk.BOTH,
                 side=tk.RIGHT,
                 padx=PAD_X,
                 pady=PAD_Y)

    janela_ver_extrato.focus_set()
    # janela_ver_extrato.grab_set()
    janela_ver_extrato.wait_window()

def abrir_janela_ver_saldos():
    
    janela_ver_contas = tk.Toplevel()
    janela_ver_contas.title("ver saldo")
    janela_ver_contas.geometry("1000x500+400+300")

    saldos, saldo_final = ver_saldo(printar_na_tela=False)

    tree = ttk.Treeview(janela_ver_contas, columns=('Conta', 'Saldo'), show='headings')
    tree.heading('Conta', text='Nome')
    tree.heading('Saldo', text='Valor')
    tree.column('Conta', width=150)
    tree.column('Saldo', width=50)
    for saldo in saldos:
        if not saldos[saldo][1]:
            continue
        else:
            tree.insert('', tk.END, values=(saldo, saldos[saldo][1]))
            tree.pack(expand=True, fill='both', pady=20)

    tk.Label(janela_ver_contas, text=f'o saldo final é {saldo_final}',
             width=LARGURA_LABEL,
             font=FONTE_ARIAL_12).pack(expand=tk.YES,
                                       fill=tk.BOTH,
                                       side=tk.TOP)
    bt_sair = tk.Button(janela_ver_contas, text="sair", width=9, font=FONTE_ARIAL_15,
                           command=janela_ver_contas.destroy)
    bt_sair.pack(expand=tk.YES, fill=tk.BOTH, side=tk.BOTTOM, padx=PAD_X,
                    pady=PAD_Y, )
    janela_ver_contas.focus_set()
    # janela_ver_contas.grab_set()
    janela_ver_contas.wait_window()
