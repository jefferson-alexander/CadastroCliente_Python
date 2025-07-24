from tkinter import*
from tkinter import ttk
from tkinter import messagebox  
from tkcalendar import Calendar, DateEntry
import sqlite3

#Bibliotecas para gerar relatórios em PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4  #saída do PDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()     #criação da janela principal usando as bibliotecas gráficas

class Validadores:      #validador de caracteres
    def validate_entry2(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100    #100 é referente a 2 digitos  

class GradientFrame(Canvas):         
#efeito gradiente no frame que herda do widget canvas
#parent: o widget "pai" (normalmente uma janela ou frame).
#**kwargs: permite passar parâmetros adicionais para o Canvas (como largura, altura, borda etc).
    def __init__(self, parent, color1="#C6CCFF", color2="gray35", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1       #passando parametros
        self._color2 = color2
#Sempre que o Canvas for redimensionado (evento <Configure>), a função _draw_gradient será chamada. 
# Isso garante que o gradiente sempre ocupe todo o espaço do canvas.        
        self.bind("<Configure>", self._draw_gradient)  
    def _draw_gradient(self, event= None):  #função que desenha o gradiente no widget
        self.delete("gradient")             #Remove todas as linhas desenhadas anteriormente com a tag "gradient", para evitar sobreposição.
        width = self.winfo_width()          #Obtém a largura e altura atual do Canvas
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1) #converte cores de string para rgb
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1)/limit                #Calcula a "velocidade" com que os componentes de cor (R, G, B) deve mudar por pixel horizontal para gerar o gradiente.
        g_ratio = float(g2-g1)/limit
        b_ratio = float(b2-b1)/limit

        for i in range(limit):  #Para cada pixel horizontal i, calcula os valores RGB intermediários da cor naquele ponto.
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)   #Formata os valores de cor em hexadecimal no padrão esperado por tkinter
    #Desenha uma linha vertical (do topo até a base do canvas) na posição i, com a cor calculada. A tag "gradient" permite identificá-la depois        
            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)
        self.lower("gradient")    

class Relatorios():
    def printClient(self):      #função que chama o navegador para abrir o pdf
        webbrowser.open("cliente.pdf")      #cria um arquivo PDF

    def gerarRelatorioCliente(self):    #função que gera o relatório de acordo com a digitação do usuário. 
        self.c = canvas.Canvas("cliente.pdf")   
        self.codigoRel   = self.codigoEntry.get()
        self.nomeRel     = self.nomeEntry.get()
        self.telefoneRel = self.telefoneEntry.get()
        self.cidadeRel   = self.cidadeEntry.get()
    #desenhando string na tela largura de espaçamento da esquerda para a direita, cima para baixo
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha de cliente')
    #corpo do relatório
        self.c.setFont("Helvetica-Bold", 16)
        #self.c.drawString(50, 700, 'Código: '   + self.codigoRel)    Essa forma concatena a informação do cliente mas é puxado em negrito
        self.c.drawString(50, 700, 'Código: ')    
        self.c.drawString(50, 670, 'Nome: '  )    
        self.c.drawString(50, 640, 'Telefone: ')    
        self.c.drawString(50, 610, 'Cidade: ' )
        self.c.setFont("Helvetica", 16)     #Trazendo as informações do cliente sem o negrito        
        self.c.drawString(150, 700, self.codigoRel)    
        self.c.drawString(150, 670, self.nomeRel)    
        self.c.drawString(150, 640, self.telefoneRel)    
        self.c.drawString(150, 610, self.cidadeRel)
    #rect cria linhas, espaços, molduras
    #Largura esquerda para direita, abaixo da informação de cidade, comprimento, espeçura da linha, fill é o preenchimento, strock é para aparecer
        self.c.rect(20, 550, 550, 200, fill=False, stroke=True)  
        self.c.showPage()
        self.c.save()
        self.printClient()

class Funcao():
    def variaveis(self):
        self.codigo   = self.codigoEntry.get()
        self.nome     = self.nomeEntry.get()
        self.telefone = self.telefoneEntry.get()
        self.cidade   = self.cidadeEntry.get()

    def limpa_tela(self):       #irá limpar as informações de entrada do usuário
        self.codigoEntry.delete(0, END)
        self.nomeEntry.delete(0, END)
        self.telefoneEntry.delete(0, END)
        self.cidadeEntry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")  #criando e conectando ao banco clientes.bd
        self.cursor = self.conn.cursor()            #cursor faz a execução da query e os parametros

    def desconecta_bd(self):
        self.conn.close()    

    def tabelas(self):
        self.conecta_bd()        #funçao que conecta ao BD e cria a tabela clientes   
        print("Conectando ao Banco de Dados")
    #função para executar o SQL  
    # para funcionar o autoincrement INTEGER e AUTOINCREMENT deve ser exatamente descrito dessa forma      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS clientes
                             (cod INTEGER PRIMARY KEY AUTOINCREMENT, nome_cliente varchar(40) not null, telefone int(12), cidade varchar(40));""")
        self.conn.commit()   #salvando e validando a criação da tabela
        print("Banco de dados criado com sucesso")    

    def insert(self):
        self.variaveis()     #chamando a função de variáveis  
    #tratando condição se caso o usuário não digitar
        if self.nomeEntry.get()  == "": #caso o campo esteja vazio
            messagebox.showinfo("Aviso", "Para cadastrar um novo cliente é preciso digitar o nome!" )
        elif self.telefoneEntry.get() == "":
            messagebox.showinfo("Aviso", "Para cadastrar um novo cliente é preciso digitar o telefone!" )
        elif self.cidadeEntry.get() == "":  
            messagebox.showinfo("Aviso", "Para cadastrar um novo cliente é preciso digitar a cidade!" )
        else:              
            self.conecta_bd()    #chamando a função conecta_db para conectar ao BD
            self.cursor.execute("""INSERT INTO clientes (nome_cliente, telefone, cidade)
                                VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
            self.conn.commit()
            self.desconecta_bd()           
            self.select_lista()  #depois de inserir um novo registro irá realizar o select da lista
            self.limpa_tela()    #limpa os dados digitados

    def select_lista(self): 
    #Caso tenha algo na lista vai deletar, depois *self get irá exibir novamente
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()          
        lista = self.cursor.execute("SELECT * FROM clientes ORDER BY cod;")    
        for i in lista:
            self.listaCli.insert("", END, values=i)
            
        self.desconecta_bd()    #A conexão é fechada depois de realizar o for loop

    def OnDoubleClick(self, event):  #função para coletar as informações do Treeview usando o duplo clique. Realiza o evento de doubleclick
        self.limpa_tela()
        self.listaCli.selection()   #selecionando as informações da lista
        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')    #seleciona os itens que receberem o dublo clique
            self.codigoEntry.insert(END, col1)                          #pega as informações que o Entry receberá
            self.nomeEntry.insert(END, col2)
            self.telefoneEntry.insert(END, col3)
            self.cidadeEntry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()     #chamando a função de variáveis   
        self.conecta_bd()
        self.cursor.execute("DELETE FROM clientes WHERE cod = ?", (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista() 

    def altera_cliente(self):
        self.variaveis()    #chamando função de variáveis
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade =? 
                            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo,))   #codigo deve ficar por último
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())      #limpando a lista    
        self.nomeEntry.insert(END, '%')  #porcentagem busca tudo que estiver digitado, como se fosse um complemento
        nome = self.nomeEntry.get()
    #Like faz a pesquisa onde tem a informação no cliente ordenado ascedente por nome
    #porcentagem é o código usado para não precisar digitar toda informação a ser buscada
        self.cursor.execute("SELECT * FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY  nome_cliente ASC" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:  #insere a busca dentro da lista
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()    
        self.desconecta_bd()

    def calendario(self):
        self.calendario1 = Calendar(self.aba2, fg="gray75", bg="blue", font=("Times", '9', 'bold'), locale='pt_br') #locale configura a data pela regiao
        self.calendario1.place(relx=0.5, rely=0.15)
        self.calData = Button(self.aba2, text="Inserir Data", command=self.print_cal)
        self.calData.place(relx=0.56, rely=0.02, height=25, width=100) 

    def print_cal(self): #inserindo a data na entry
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()              #fecha a janela
        self.dataEntry.delete(0, END)           #deleta o que tiver escrito para não sobrescrever
        self.dataEntry.insert(END, dataIni)     #insert, joga a informação do calendario1 para o dataIni
        self.calData.destroy()                  #destroi o botão que insere a data

class Aplication(Funcao, Relatorios, Validadores):   #informar que a classe aplication pode usar a classe Funcao
    def __init__(self):
        self.root = root        #equivalência para a classe root, é preciso nomeá-la
        self.tela()             #chamando a função tela
        self.validaEntradas()   #chamando função de validar entradas do código digitado pelo usuário
        self.frameTela()        #chamando a função frame
        self.janelaFrame1()     #chamando as funções do frame1
        self.janelaFrame2()     #chamando as funções do frame2
        self.tabelas()          #irá criar a tabela caso não exista
        self.select_lista()     #exibe a lista atualizada ao abrir o sistema        
        self.Menus()            #tela de menu
        root.mainloop()         #responsável por abrir a janela             

    def tela(self):         #configuração de tela    
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#1e3743')
        self.root.geometry("788x588")    #dimensão da janela horizontal x vertical
        self.root.resizable(True, False)              #aumenta ou diminua, horizontal x vertical
        self.root.maxsize(width=900, height=700)      #tamanho máximo da tela
        self.root.minsize(width=500, height=300)      #tamanho mínimo da tela

    def validaEntradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry2), "%P")   #abstração para usar a função dentro da entry 
    #validate="key", validatecommand="self.vcmd2" são introduzidos no Entry.       

#posicionamento do frame dentro da tela horizontal x vertical. Valor entre 0 a 1. 
#relx é o valor da esquerda para a direita e rely é valor de cima para baixo       
#relwidth é Largura da direita para esquerda e relheight é o valor de baixo para cima.
#place faz com que o tamanho se torne relativo dentro da tela    
    def frameTela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#a4a8aa", highlightbackground='green', highlightthickness=4)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)          

        self.frame_2 = Frame(self.root, bd=4, bg='#a4a8aa', highlightbackground='green', highlightthickness=4)  
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def janelaFrame1(self):    #botão dentro do frame_1. bd é uma sombra para o botão 
    #Adicionando abas no frame1
        self.abas = ttk.Notebook(self.frame_1)        
        self.aba1 = Frame(self.abas)
        self.aba2 = GradientFrame(self.abas)
        self.aba1.configure(background='#a4a8aa')
        self.aba2.configure(background="lightgray")
        self.abas.add(self.aba1, text="Aba 1")
        self.abas.add(self.aba2, text="Aba 2")
        self.abas.place(relx=0, rely=0, relheight=0.96, relwidth=0.98)          
    #molduras nos botões
        self.canvas_bt = Canvas(self.aba1, bd=0, bg='black', highlightbackground='gray', highlightthickness=3) 
        self.canvas_bt.place(relx=0.19, rely=0.08, relheight=0.14, relwidth=0.23)  
    #efeito do botão é activeforeground e activeforeground        
        self.btnLimpar = Button(self.aba1, text='Limpar', bd=3, bg="#6d6e9c", activebackground='#108ecb', activeforeground="white", fg='white', font=('verdana', 8, 'bold'), command=self.limpa_tela )
        self.btnLimpar.place(relx=0.2 ,rely=0.1, relheight=0.1, relwidth=0.1) 
        self.btnBuscar = Button(self.aba1, text='Buscar', bd=3, bg="#6d6e9c", activebackground='#108ecb', activeforeground="white", fg='white', font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.btnBuscar.place(relx=0.31 ,rely=0.1, relheight=0.1, relwidth=0.1)   
        self.btnNovo = Button(self.aba1, text='Cadastrar', bd=3, bg="#6d6e9c",fg='white', font=('verdana', 8, 'bold'), command=self.insert)
        self.btnNovo.place(relx=0.62 ,rely=0.1, relheight=0.1, relwidth=0.1) 
        self.btnAlterar = Button(self.aba1, text='Alterar', bd=3, bg="#6d6e9c",fg='white', font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.btnAlterar.place(relx=0.73 ,rely=0.1, relheight=0.1, relwidth=0.1) 
        self.btnApagar = Button(self.aba1, text='Apagar', bd=3, bg="#6d6e9c",fg='white', font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.btnApagar.place(relx=0.84 ,rely=0.1, relheight=0.1, relwidth=0.1) 
    #label e entrada do código
        self.lblCodigo = Label(self.aba1, text='Código', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblCodigo.place(relx=0.05, rely=0.02)
        self.codigoEntry = Entry(self.aba1, validate="key", validatecommand=self.vcmd2, bg="#84878b", font=('verdana', 8, 'bold'))      #Chamando o txt para o usuário digitar
        self.codigoEntry.place(relx=0.05, rely=0.1, relheight=0.1, relwidth=0.08)                #relwidth determina o tamanho do label
        #self.codigoEntry.config(state="disabled")                                                # Desabilita o campo (o usuário não pode digitar)
    #label e entrada do nome
        self.lblNome = Label(self.aba1, text='Nome', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblNome.place(relx=0.05, rely=0.30)
        self.nomeEntry = Entry(self.aba1, font=('verdana', 8, 'bold'))
        self.nomeEntry.place(relx=0.05, rely=0.38, relheight=0.1, relwidth=0.89)
    #label e entrada do telefone
        self.lblTelefone = Label(self.aba1, text='Telefone', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblTelefone.place(relx=0.05, rely=0.60)
        self.telefoneEntry = Entry(self.aba1, font=('verdana', 8, 'bold'))
        self.telefoneEntry.place(relx=0.05, rely=0.68, relheight=0.1, relwidth=0.30)    
    #label e entrada do nome de cidade
        self.lblCidade = Label(self.aba1, text='Cidade', bg='#a4a8aa', font=('verdana', 8, 'bold'))
        self.lblCidade.place(relx=0.36, rely=0.60)
        self.cidadeEntry = Entry(self.aba1, font=('verdana', 8, 'bold'))
        self.cidadeEntry.place(relx=0.36, rely=0.68, relheight=0.1, relwidth=0.58)
     #dropdown
        self.Tipvar = StringVar(self.aba2)
        self.TipV = ("Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)")
        self.Tipvar.set("Solteiro(a)")    #Opção padrão que sempre aparece na caixa
        self.popupMenu = OptionMenu(self.aba2, self.Tipvar, *self.TipV) #variável para option menu em que chama a lista
        self.popupMenu.place(relx=0.1, rely=0.2, relheight=0.2, relwidth=0.2)
        self.estado_civil = self.Tipvar.get()   #Coletando a informação que o usuário escolheu  

        self.btnJanela2 = Button(self.aba2,text="Janela 2", bd=3, bg="#6d6e9c", activebackground='#108ecb', activeforeground="white", fg='white', font=('verdana', 8, 'bold'), command=self.janela2)        
        self.btnJanela2.place(relx=0.1 ,rely=0.5)

    #calendário
        self.bt_calendario = Button(self.aba2, text="Data", command=self.calendario)    
        self.bt_calendario.place(relx=0.5, rely=0.02)
        self.dataEntry = Entry(self.aba2, width=10)
        self.dataEntry.place(relx=0.5,rely=0.17)

    def janelaFrame2(self): 
    #criando tabela. Height configura a posição verticalmente e columns especifica as colunas        
        self.listaCli = ttk.Treeview(self.frame_2, columns=("col1", "col2", "col3","col4"), show='headings')
    #especificando o cabeçalho de cada coluna criada. É iniciada com valor Zero    
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
    #especificando o tamanho em relação das colunas
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)    
        self.listaCli.place(relx=0.01, rely=0.01, relheight=0.95, relwidth=0.95)  
        
    #barra de rolagem    
        self.scroolList = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolList.set)    #barra de rolagem (yscroll) pertence a scroolList
        self.scroolList.place(relx=0.95, rely=0.01, relheight=0.95, relwidth=0.04) 
    #chamando a função double click. Bind é a interação com a lista. Double-1 significa double click    
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)     

    def Menus(self):    #menu de opções
        menubar = Menu(self.root)           
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)    #Variável para cada Menubar
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()     #função para fechar o sistema

        menubar.add_cascade(label= "Opções", menu= filemenu)    #Criando nomes para cada menu
        menubar.add_cascade(label= "Relatórios", menu= filemenu2)

        filemenu.add_command(label="Sair", command=Quit)    #chamando a função que fecha a janela
        filemenu.add_command(label="Limpa Cliente", command= self.limpa_tela)
        filemenu2.add_command(label="Ficha do cliente", command= self.gerarRelatorioCliente)

    def janela2(self): 
        self.root2 = Toplevel() #Toplevel é uma classe do Tkinter que cria uma nova janela (uma "janela filha") independente da janela principal.
        self.root2.title("Javela 2")
        self.root2.configure(background="lightblue")
        self.root2.geometry("400x200")
        self.root2.resizable(False, False)   #janela estática, tamanho fixo
        self.root2.transient(self.root)      #janela 2 está dentro da janela principal
        self.root2.focus_force               #forçando o foco para que a janela 2 fique a frente
        self.root2.grab_set()                #impede que seja digitando algo na primeira janela
                       
Aplication()    #chamando a classe para exibir a janela